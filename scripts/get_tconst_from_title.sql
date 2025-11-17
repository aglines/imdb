-- Convert movie titles to tconst IDs for recommendation query
SELECT tconst, primaryTitle, startYear, titleType
FROM "title.basics"
WHERE titleType = 'movie'
  AND LOWER(primaryTitle) LIKE LOWER('%Shawshank%')  -- Replace with your title
  -- Add more titles:
  -- OR LOWER(primaryTitle) LIKE LOWER('%Godfather%')
  -- OR LOWER(primaryTitle) LIKE LOWER('%Dark Knight%')
ORDER BY primaryTitle;