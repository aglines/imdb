-- Recommend movie based on genres, year, actors from your favorites
WITH my_movies AS (
  -- Replace these with your movie IDs
  SELECT 'tt0111161' AS tconst  -- Shawshank Redemption
  UNION SELECT 'tt0068646'      -- The Godfather
  UNION SELECT 'tt0468569'      -- The Dark Knight
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
  WHERE startYear != '\N'
),
my_actors AS (
  SELECT p.nconst, COUNT(*) AS cnt
  FROM my_movies m
  JOIN "title.principals" p ON m.tconst = p.tconst
  WHERE p.category IN ('actor', 'actress')
  GROUP BY p.nconst
)
SELECT 
  b.tconst,
  b.primaryTitle,
  b.startYear,
  b.genres,
  -- Score: 3x genre match + year proximity + actor overlap
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
  AND b.startYear != '\N'
  AND b.genres != '\N'
ORDER BY score DESC
LIMIT 1;