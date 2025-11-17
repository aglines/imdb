import pandas as pd
import sqlite3

# Load TSV, create DB
df = pd.read_csv('title.basics.tsv.gz', sep='\t', na_values='\\N')
conn = sqlite3.connect('imdb.db')
df.to_sql('title_basics', conn, if_exists='replace', index=False)
conn.close()

# Query
conn = sqlite3.connect('imdb.db')
results = pd.read_sql("SELECT * FROM title_basics WHERE titleType='movie' LIMIT 10", conn)
conn.close()


