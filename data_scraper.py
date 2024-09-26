import requests
from bs4 import BeautifulSoup
import os
import re
import pandas as pd

# Load the CSV file
csv_file = 'list_of_links.csv' 
url_column = 'links'  
df = pd.read_csv(csv_file)


if url_column not in df.columns:
    raise ValueError(f"Column '{url_column}' not found in the CSV file.")


urls = df[url_column].dropna().tolist() 


session = requests.Session()

# Set headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}


def clean_title(title):
    # Remove illegal characters for filenames and limit length
    return re.sub(r'[\/:*?"<>|]', '', title)[:50]


for url in urls:
    # Send a GET request to the website with headers
    response = session.get(url, headers=headers)
    

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'no_title'
        cleaned_title = clean_title(title)
        print(f"Title: {cleaned_title}")
        content = soup.find_all('p') 
        page_content = "\n\n".join([paragraph.text for paragraph in content])       
        file_name = f"{cleaned_title}.txt"
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n{page_content}")
        print(f"Saved content to {file_name}")
    else:
        print(f"Failed to retrieve the page at {url}. Status code: {response.status_code}")
