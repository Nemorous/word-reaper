

def print_stats(word_list):
    print("\nWordlist Stats:")
    print(f"•Total words: {len(word_list)}")
    lengths = [len(word) for word in word_list]
    if lengths:
        print(f"•Shortest word: {min(lengths)} chars")
        print(f"•Longest word: {max(lengths)} chars")
    else:
        print("No words to analyze.")

def save_to_file(word_list, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for word in word_list:
                f.write(f"{word}\n")
        print(f"•Scraped {len(word_list)}/{len(word_list)} words")
    except Exception as e:
        print(f"Error saving to file: {e}")

