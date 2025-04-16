import itertools
import string
import re
from tqdm import tqdm

MASK_CHARSETS = {
    '?a': string.ascii_letters + string.digits + string.punctuation,
    '?d': string.digits,
    '?s': string.punctuation,
    '?l': string.ascii_lowercase,
    '?u': string.ascii_uppercase,
}

def leetspeak(word):
    table = str.maketrans({
        'a': '@', 'e': '3', 'i': '1', 'o': '0',
        's': '$', 't': '7', 'l': '1'
    })
    return word.translate(table)

def toggle_case(word):
    toggles = set()
    for i in range(1, 2 ** len(word)):
        combo = ''.join(
            c.upper() if (i >> j) & 1 else c.lower()
            for j, c in enumerate(word)
        )
        toggles.add(combo)
    return list(toggles)

def insert_variants(word, sep):
    variants = []
    for i in range(1, len(word)):
        variants.append(word[:i] + sep + word[i:])
    return variants

def parse_mask(mask):
    if not mask:
        return []

    if not re.match(r'^(?:\?[asdlu])+$', mask):
        raise ValueError(f"Invalid mask format: {mask}. Must contain only ?a, ?d, ?s, ?l, ?u sequences.")

    charset_ids = [mask[i:i+2] for i in range(0, len(mask), 2)]

    charsets = []
    for charset_id in charset_ids:
        if charset_id in MASK_CHARSETS:
            charsets.append(MASK_CHARSETS[charset_id])
        else:
            raise ValueError(f"Unknown character set: {charset_id}")

    return charsets

def generate_mask_combinations(charsets, increment=False):
    if not charsets:
        return []

    combinations = []
    max_length = len(charsets)
    start_length = 1 if increment else max_length

    for length in range(start_length, max_length + 1):
        for charset_combo in itertools.combinations(range(max_length), length):
            if increment and list(charset_combo) != list(range(length)):
                continue

            current_charsets = [charsets[i] for i in range(length)]
            total_combinations = 1
            for charset in current_charsets:
                total_combinations *= len(charset)

            if total_combinations > 1000000:
                print(f"Warning: Generating {total_combinations:,} combinations for mask length {length}...")

            combinations.extend([''.join(combo) for combo in itertools.product(*current_charsets)])

    return combinations

def apply_masks(words, append_mask=None, prepend_mask=None, synchronize=False, increment=False):
    if not words:
        return []

    append_charsets = parse_mask(append_mask) if append_mask else []
    prepend_charsets = parse_mask(prepend_mask) if prepend_mask else []

    result = set(words)

    if synchronize and increment and append_charsets and prepend_charsets:
        print("Applying synchronized incremental masks...")
        prepend_max_length = len(prepend_charsets)
        append_max_length = len(append_charsets)

        for prepend_length in range(1, prepend_max_length + 1):
            current_prepend_charsets = prepend_charsets[:prepend_length]
            prepend_combinations = list(itertools.product(*current_prepend_charsets))

            for append_length in range(1, append_max_length + 1):
                current_append_charsets = append_charsets[:append_length]
                append_combinations = list(itertools.product(*current_append_charsets))

                total_combinations = len(prepend_combinations) * len(append_combinations)
                if total_combinations > 1000000:
                    print(f"Warning: Generating {total_combinations:,} synchronized combinations...")

                for word in words:
                    for prepend_combo in prepend_combinations:
                        prepend_str = ''.join(prepend_combo)
                        for append_combo in append_combinations:
                            append_str = ''.join(append_combo)
                            result.add(prepend_str + word + append_str)

    elif synchronize and append_charsets and prepend_charsets:
        print("Applying synchronized masks...")
        append_combinations = list(itertools.product(*append_charsets))
        prepend_combinations = list(itertools.product(*prepend_charsets))

        total_combinations = len(append_combinations) * len(prepend_combinations)
        if total_combinations > 1000000:
            print(f"Warning: Generating {total_combinations:,} synchronized combinations...")

        for word in words:
            for prepend_combo in prepend_combinations:
                prepend_str = ''.join(prepend_combo)
                for append_combo in append_combinations:
                    append_str = ''.join(append_combo)
                    result.add(prepend_str + word + append_str)

    elif increment:
        append_combinations = []
        prepend_combinations = []

        if append_charsets:
            print(f"Applying incremental append masks (1 to {len(append_charsets)} characters)...")
            for length in range(1, len(append_charsets) + 1):
                for combo in itertools.product(*append_charsets[:length]):
                    append_combinations.append(''.join(combo))

        if prepend_charsets:
            print(f"Applying incremental prepend masks (1 to {len(prepend_charsets)} characters)...")
            for length in range(1, len(prepend_charsets) + 1):
                for combo in itertools.product(*prepend_charsets[:length]):
                    prepend_combinations.append(''.join(combo))

        if append_combinations:
            print(f"Applying {len(append_combinations):,} append combinations...")
            for word in words:
                for combo in append_combinations:
                    result.add(word + combo)

        if prepend_combinations:
            print(f"Applying {len(prepend_combinations):,} prepend combinations...")
            for word in words:
                for combo in prepend_combinations:
                    result.add(combo + word)

    else:
        append_combinations = generate_mask_combinations(append_charsets) if append_charsets else []
        prepend_combinations = generate_mask_combinations(prepend_charsets) if prepend_charsets else []

        if append_combinations:
            print(f"Applying {len(append_combinations):,} append combinations...")
            for word in words:
                for combo in append_combinations:
                    result.add(word + combo)

        if prepend_combinations:
            print(f"Applying {len(prepend_combinations):,} prepend combinations...")
            for word in words:
                for combo in prepend_combinations:
                    result.add(combo + word)

    return sorted(result)

def mentalize(words, leet=False, toggle=False, underscores=False, spaces=False, hyphens=False,
              append_mask=None, prepend_mask=None, synchronize=False, increment=False):
    mutated = set()
    for word in tqdm(words, desc="Mentalizing", unit="word"):
        word = word.strip().lower()
        variants = {word}

        if leet:
            variants.update({leetspeak(w) for w in variants})

        if toggle:
            toggled = set()
            for v in variants:
                toggled.update(toggle_case(v))
            variants.update(toggled)

        if underscores:
            underscore_variants = set()
            for v in variants:
                underscore_variants.update(insert_variants(v, '_'))
            variants.update(underscore_variants)

        if spaces:
            space_variants = set()
            for v in variants:
                space_variants.update(insert_variants(v, ' '))
            variants.update(space_variants)

        if hyphens:
            hyphen_variants = set()
            for v in variants:
                hyphen_variants.update(insert_variants(v, '-'))
            variants.update(hyphen_variants)

        mutated.update(variants)

    if append_mask or prepend_mask:
        mutated = apply_masks(list(mutated), append_mask, prepend_mask, synchronize, increment)

    return sorted(mutated)

def merge_files(file_list):
    merged = set()
    for file in tqdm(file_list, desc="Merging files", unit="file"):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                merged.add(line.strip().lower())
    return sorted(merged)
