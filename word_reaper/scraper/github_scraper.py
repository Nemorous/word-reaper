import requests
from tqdm import tqdm

def scrape(url):
    print(f"Scraping GitHub source: \n{url}")
    
    words = []

    if "raw.githubusercontent.com" in url or "gist.githubusercontent.com" in url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            lines = content.splitlines()
            for line in tqdm(lines, desc="Parsing GitHub lines", unit="line"):
                words.extend(line.strip().split())
        except requests.RequestException as e:
            print(f"Failed to fetch raw GitHub file: {e}")
    else:
        print("Non-raw URLs are not fully supported yet. Try linking to raw.githubusercontent.com or gist.githubusercontent.com.")
    
    return words
