

import requests

def scrape(url):
    print(f"Scraping GitHub source: \n{url}")
    
    words = []

    # Raw file support (ideal use case)
    if "raw.githubusercontent.com" in url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            for line in content.splitlines():
                words.extend(line.strip().split())
        except requests.RequestException as e:
            print(f"Failed to fetch raw GitHub file: {e}")
    else:
        print("Non-raw URLs are not fully supported yet. Try linking to raw.githubusercontent.com.")
    
    return words

