import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
data_folder = os.getenv('LOCAL_DATA_FOLDER')
csv_path = os.path.join(data_folder, 'seen_movies.csv')

# Load seen movies from CSV
seen = pd.read_csv(csv_path)  # Assumes column 'title'
conn = sqlite3.connect('imdb.db')

# Get tconst values for seen movies
tconsts = []
for title in seen['title']:
    query = f"""
    SELECT tconst FROM "title.basics" 
    WHERE titleType='movie' AND LOWER(primaryTitle) LIKE LOWER('%{title}%')
    LIMIT 1
    """
    result = pd.read_sql(query, conn)
    if not result.empty:
        tconsts.append(result['tconst'][0])

# Build recommendation query
my_movies_cte = " UNION SELECT ".join([f"'{tc}'" for tc in tconsts])

recommend_query = f"""
WITH my_movies AS (
  SELECT {my_movies_cte} AS tconst
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