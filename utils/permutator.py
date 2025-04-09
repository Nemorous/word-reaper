import itertools
import random

def leetspeak(word):
    table = str.maketrans({
        'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7', 'l': '1'
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

def append_patterns(word, token):
    patterns = []
    for i in range(1, 5):
        pattern = token * i
        patterns.append(word + pattern)
        patterns.append(pattern + word)
    return patterns

def mentalize(words, leet=False, toggle=False, underscores=False, spaces=False, hyphens=False):
    mutated = set()

    for word in words:
        word = word.strip().lower()
        variants = {word}

        # Apply leetspeak
        if leet:
            variants.update({leetspeak(w) for w in variants})

        # Apply case toggles
        if toggle:
            toggled = set()
            for v in variants:
                toggled.update(toggle_case(v))
            variants.update(toggled)

        # Insert underscores
        if underscores:
            underscore_variants = set()
            for v in variants:
                underscore_variants.update(insert_variants(v, '_'))
            variants.update(underscore_variants)

        # Insert spaces
        if spaces:
            space_variants = set()
            for v in variants:
                space_variants.update(insert_variants(v, ' '))
            variants.update(space_variants)

        # Insert hyphens
        if hyphens:
            hyphen_variants = set()
            for v in variants:
                hyphen_variants.update(insert_variants(v, '-'))
            variants.update(hyphen_variants)

        # Append ?a, ?s, ?d tokens left/right
        for v in list(variants):
            for token in ['?a', '?s', '?d']:
                variants.update(append_patterns(v, token))

        mutated.update(variants)

    return sorted(mutated)

def merge_files(file_list):
    merged = set()
    for file in file_list:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                merged.add(line.strip().lower())
    return sorted(merged)

def combinatorize(words1, words2):
    combined = set()
    for w1 in words1:
        for w2 in words2:
            combined.add(w1 + w2)
            combined.add(w2 + w1)
    return sorted(combined)
