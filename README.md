# imdb
- record and categorize the movies and TV i have watched recently
- build a simple recommendation engine to find additional media

# NOTES
- This project uses IMDb's non-commercial datasets (7 TSV files) imported into a local SQLite database (imdb.db) for SQL-based analysis. The ETL pipeline loads title metadata, ratings, crew, episodes, and name data into normalized tables, enabling efficient querying of ~10M+ records without external dependencies or cloud services.


# DATA SOURCE
- https://datasets.imdbws.com/ : local download of imdb data updated daily

# SCOPE
- local storage for fine-tuned control of data
- one day project, will not ingest data more than once
 
# TODO
- build sql to ingest a list of movies, produce a recommendation


# DONE
- local copy of imdb daily data stored in sqlite3


