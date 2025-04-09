import itertools

def combinatorize(words1, words2):
    combos = set()
    for w1 in words1:
        for w2 in words2:
            combos.add(w1 + w2)
            combos.add(w2 + w1)
    return sorted(combos)
