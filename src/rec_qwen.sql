WITH watched_genres AS (
  SELECT DISTINCT unnest(string_to_array(genres, ',')) as genre
  FROM title_basics 
  WHERE tconst IN ('tt0111161', 'tt0133093') -- Replace with your watched movie IDs
),
recommended_movies AS (
  SELECT 
    tb.tconst,
    tb.primaryTitle,
    tb.startYear,
    tb.genres,
    COUNT(wg.genre) as genre_match_count,
    AVG(ABS(tb.startYear - (SELECT AVG(startYear) FROM title_basics WHERE tconst IN ('tt0111161', 'tt0133093')))) as year_diff
  FROM title_basics tb
  CROSS JOIN watched_genres wg
  WHERE tb.tconst NOT IN ('tt0111161', 'tt0133093') -- Exclude already watched movies
    AND tb.titleType = 'movie'
    AND tb.genres IS NOT NULL
    AND tb.genres != '\N'
  GROUP BY tb.tconst, tb.primaryTitle, tb.startYear, tb.genres
)
SELECT 
  tconst,
  primaryTitle,
  startYear,
  genres
FROM recommended_movies
ORDER BY genre_match_count DESC, year_diff ASC
LIMIT 1;