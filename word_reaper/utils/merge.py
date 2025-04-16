from tqdm import tqdm

def merge_files(file_list):
    all_words = set()

    for filename in tqdm(file_list, desc="Merging files", unit="file"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    cleaned = line.strip()
                    if cleaned:
                        all_words.add(cleaned)
        except FileNotFoundError:
            print(f"[!] File not found: {filename}")

    return sorted(all_words)
