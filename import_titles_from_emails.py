import os
import re
from dotenv import load_dotenv
import csv

# Load environment variables
load_dotenv()

# Get the folder path from environment variable
data_folder = os.getenv('MOVIE_RENTAL_RECEIPTS')

def extract_movie_title(eml_content):
    # Pattern for Google emails
    google_pattern = r'<span dir=3Dltr>(.*?)<br>'
    
    # Pattern for Apple emails
    apple_pattern = r'<span class=3D"title" dir=3D"auto" style=3D"font-weight:600;">(.*?)<br>'
    
    # Try Google pattern first
    google_match = re.search(google_pattern, eml_content, re.DOTALL)
    if google_match:
        return google_match.group(1).strip()
    
    # Try Apple pattern
    apple_match = re.search(apple_pattern, eml_content, re.DOTALL)
    if apple_match:
        return apple_match.group(1).strip()
    
    return None

def process_eml_files(folder_path):
    movie_titles = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.eml'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                title = extract_movie_title(content)
                if title:
                    movie_titles.append(title)
    
    return movie_titles

# Process all .eml files and save to CSV
titles = process_eml_files(data_folder)

# Write to CSV file in the data folder
output_file = os.path.join(data_folder, 'rented_movies.csv')
with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write header if file is empty
    if os.path.getsize(output_file) == 0:
        writer.writerow(['Movie Title'])
    
    for title in titles:
        writer.writerow([title])

print(f"Extracted {len(titles)} movie titles to {output_file}")