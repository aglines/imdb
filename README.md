# IMDb Movie Recommender

Simple movie recommendation system using IMDb's non-commercial datasets.

## Setup

1. **Download data** from https://datasets.imdbws.com/
2. **Import to SQLite:**
```python
   import pandas as pd
   import sqlite3
   
   conn = sqlite3.connect('imdb.db')
   for file in ['title.basics', 'title.ratings', 'title.principals', 
                'title.crew', 'title.episode', 'title.akas', 'name.basics']:
       df = pd.read_csv(f'{file}.tsv.gz', sep='\t', na_values='\\N')
       df.to_sql(file, conn, if_exists='replace', index=False)
   conn.close()
```

3. **Configure:**
   - Create `.env` with `LOCAL_DATA_FOLDER=/path/to/data`
   - Create `seen_movies.csv` in that folder with your watched movies

## Usage
```bash
python recommend.py
```

Outputs top 10 movie recommendations based on:
- **Genre match** (3x weight)
- **Year proximity** (1x weight)  
- **Shared actors** (1x weight)

## Data Format

`seen_movies.csv`:
```csv
title
Blade Runner
The Matrix
Interstellar
```

## Tech Stack

- Python 3
- SQLite3 (local storage)
- pandas (data processing)
- IMDb datasets (~10M titles, 7 TSV files)


