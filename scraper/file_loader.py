

def load(file_path):
    print(f"Loading words from file: \n{file_path}")
    words = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                words.extend(line.strip().split())
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

    return words

