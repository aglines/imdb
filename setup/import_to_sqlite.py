import pandas as pd
import sqlite3
import glob
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get data folder from environment
LOCAL_DATA_FOLDER = os.getenv('LOCAL_DATA_FOLDER')
if not LOCAL_DATA_FOLDER:
    raise ValueError("LOCAL_DATA_FOLDER not set in .env file")

# Connect to database
conn = sqlite3.connect('imdb.db')
conn.execute('PRAGMA journal_mode=WAL')

# Get all TSV files
tsv_files = glob.glob(os.path.join(LOCAL_DATA_FOLDER, '*.tsv'))


for file_path in tsv_files:
    filename = os.path.basename(file_path)
    table_name = filename.replace('.tsv', '')
    
    # Process in chunks for low memory
    chunk_size = 10000
    chunks = pd.read_csv(file_path, sep='\t', chunksize=chunk_size, low_memory=False)
    
    for i, chunk in enumerate(chunks):
        if i == 0:
            chunk.to_sql(table_name, conn, if_exists='replace', index=False)
        else:
            chunk.to_sql(table_name, conn, if_exists='append', index=False)
    
    print(f"Loaded {filename}")

conn.close()
