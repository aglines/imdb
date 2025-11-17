-- Verify all IMDb tables imported
SELECT 'title.akas' AS tbl, COUNT(*) AS rows FROM "title.akas"
UNION ALL
SELECT 'title.basics', COUNT(*) FROM "title.basics"
UNION ALL
SELECT 'title.crew', COUNT(*) FROM "title.crew"
UNION ALL
SELECT 'title.episode', COUNT(*) FROM "title.episode"
UNION ALL
SELECT 'title.principals', COUNT(*) FROM "title.principals"
UNION ALL
SELECT 'title.ratings', COUNT(*) FROM "title.ratings"
UNION ALL
SELECT 'name.basics', COUNT(*) FROM "name.basics";
