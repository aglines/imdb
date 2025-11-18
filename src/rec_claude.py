import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
# data_folder = os.getenv('LOCAL_DATA_FOLDER')
# csv_path = os.path.join(data_folder, 'seen_movies.csv')
data_folder = os.getenv('MOVIE_RENTAL_RECEIPTS')
csv_path = os.path.join(data_folder, 'rented_movies.csv')


# Load seen movies from CSV
seen = pd.read_csv(csv_path)  # Assumes column 'title'
conn = sqlite3.connect('imdb.db')

# Get tconst values for seen movies
tconsts = []
for title in seen['title']:

    title = title.strip()
    # Remove surrounding quotes if present
    if (title.startswith('"') and title.endswith('"')) or (title.startswith("'") and title.endswith("'")):
       title = title[1:-1]

    # Escape single quotes for SQL query
    escaped_title = title.replace("'", "''")
    
    # Try exact match first
    query = f"""
    SELECT tconst FROM "title.basics" 
    WHERE titleType='movie' AND LOWER(primaryTitle) = LOWER('{escaped_title}')
    LIMIT 1
    """
    try:
        result = pd.read_sql(query, conn)
        
        # Fall back to fuzzy if no exact match
        if result.empty:
            query = f"""
            SELECT tconst FROM "title.basics" 
            WHERE titleType='movie' AND LOWER(primaryTitle) LIKE LOWER('%{escaped_title}%')
            LIMIT 1
            """
            result = pd.read_sql(query, conn)
        
        if not result.empty:
            tconsts.append(result['tconst'][0])
            # print(f"Found: '{title}'")
        else:
            print(f"Warning: No match for '{title}'. Skipping...")
    except Exception as e:
        print(f"Error processing '{title}': {e}. Skipping...")

# Check if any matches found
if not tconsts:
    print("No matching movies found in database")
    conn.close()
    exit()

# Build recommendation query
my_movies_cte = " UNION ALL SELECT ".join([f"'{tc}' AS tconst" for tc in tconsts])

recommend_query = f"""
WITH my_movies AS (
  SELECT {my_movies_cte}
),
my_genres AS (
  SELECT TRIM(value) AS genre, COUNT(*) AS cnt
  FROM my_movies m
  JOIN "title.basics" b ON m.tconst = b.tconst,
  json_each('["' || REPLACE(b.genres, ',', '","') || '"]')
  GROUP BY genre
),
my_years AS (
  SELECT AVG(CAST(startYear AS INT)) AS avg_year
  FROM my_movies m
  JOIN "title.basics" b ON m.tconst = b.tconst
  WHERE startYear != '\\N'
),
my_actors AS (
  SELECT p.nconst, COUNT(*) AS cnt
  FROM my_movies m
  JOIN "title.principals" p ON m.tconst = p.tconst
  WHERE p.category IN ('actor', 'actress')
  GROUP BY p.nconst
)
SELECT 
  b.tconst, b.primaryTitle, b.startYear, b.genres,
  (SELECT SUM(mg.cnt) * 3 
   FROM my_genres mg, json_each('["' || REPLACE(b.genres, ',', '","') || '"]')
   WHERE TRIM(value) = mg.genre) +
  (10 - ABS(CAST(b.startYear AS INT) - (SELECT avg_year FROM my_years))) +
  (SELECT COUNT(*) FROM my_actors ma 
   JOIN "title.principals" p ON ma.nconst = p.nconst 
   WHERE p.tconst = b.tconst AND p.category IN ('actor','actress')) AS score
FROM "title.basics" b
WHERE b.titleType = 'movie'
  AND b.tconst NOT IN (SELECT tconst FROM my_movies)
  AND b.startYear != '\\N' AND b.genres != '\\N'
ORDER BY score DESC LIMIT 10
"""

# Get recommendations
recs = pd.read_sql(recommend_query, conn)
print(recs)
conn.close()