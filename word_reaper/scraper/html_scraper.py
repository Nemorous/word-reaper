import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def scrape(url, tag, class_name=None, id_name=None):
    print(f"Scraping HTML from: \n{url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    if not tag:
        print("No HTML tag specified. Exiting.")
        return []

    if class_name:
        elements = soup.find_all(tag, class_=class_name)
    elif id_name:
        elements = soup.find_all(tag, id=id_name)
    else:
        elements = soup.find_all(tag)

    words = []
    for elem in tqdm(elements, desc=f"Extracting <{tag}> elements", unit="tag"):
        text = elem.get_text(separator=' ', strip=True)
        words.extend(text.split())

    return words
