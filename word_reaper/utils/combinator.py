from tqdm import tqdm

def combinatorize(file1_path, file2_path, output_path=None, max_word_length=32, buffer_size=1000):
    with open(file1_path, "r", encoding="utf-8", errors="ignore") as f1:
        words1 = [line.strip().replace('\r', '') for line in f1 if len(line.strip()) <= max_word_length]

    total_lines = len(words1)
    progress = tqdm(total=total_lines, desc="Combining", unit="word1")

    buffer = []
    out_file = open(output_path, "w", encoding="utf-8") if output_path else None

    try:
        for word1 in words1:
            with open(file2_path, "r", encoding="utf-8", errors="ignore") as f2:
                for line2 in f2:
                    word2 = line2.strip().replace('\r', '')
                    if len(word2) > max_word_length:
                        continue

                    combo = word1 + word2
                    buffer.append(combo)

                    if len(buffer) >= buffer_size:
                        flush_buffer(buffer, out_file)

            progress.update(1)

        flush_buffer(buffer, out_file)

    finally:
        if out_file:
            out_file.close()
        progress.close()

def flush_buffer(buffer, out_file):
    if out_file:
        out_file.write('\n'.join(buffer) + '\n')
    else:
        for line in buffer:
            print(line)
    buffer.clear()
