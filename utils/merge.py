def merge_files(file_list):
    all_words = set()
    for filename in file_list:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    cleaned = line.strip()
                    if cleaned:
                        all_words.add(cleaned)
        except FileNotFoundError:
            print(f"[!] File not found: {filename}")
    return sorted(all_words)
