import itertools
import string
import re

# Character set definitions for mask processing
MASK_CHARSETS = {
    '?a': string.ascii_letters + string.digits + string.punctuation,  # All ASCII chars (upper+lower+digits+special)
    '?d': string.digits,                                              # Digits only (0-9)
    '?s': string.punctuation,                                         # Special chars only
    '?l': string.ascii_lowercase,                                     # Lowercase only
    '?u': string.ascii_uppercase,                                     # Uppercase only
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
    """Parse a hashcat-style mask like ?d?s?a into a list of character sets."""
    if not mask:
        return []
    
    # Validate mask format
    if not re.match(r'^(?:\?[asdlu])+$', mask):
        raise ValueError(f"Invalid mask format: {mask}. Must contain only ?a, ?d, ?s, ?l, ?u sequences.")
    
    # Split the mask into character set identifiers
    charset_ids = [mask[i:i+2] for i in range(0, len(mask), 2)]
    
    # Map each identifier to its character set
    charsets = []
    for charset_id in charset_ids:
        if charset_id in MASK_CHARSETS:
            charsets.append(MASK_CHARSETS[charset_id])
        else:
            raise ValueError(f"Unknown character set: {charset_id}")
    
    return charsets

def generate_mask_combinations(charsets, increment=False):
    """
    Generate combinations based on the given character sets.
    If increment is True, generate combinations of all lengths from 1 up to the full length.
    """
    if not charsets:
        return []
    
    combinations = []
    
    # Determine max length we'll iterate to
    max_length = len(charsets)
    
    # If increment is True, we generate combinations for lengths 1 to max_length
    # Otherwise, we only generate combinations for the full length
    start_length = 1 if increment else max_length
    
    for length in range(start_length, max_length + 1):
        # For each length, get all possible combinations of charsets
        for charset_combo in itertools.combinations(range(max_length), length):
            # Make sure we're taking chars in order for increment
            if increment and list(charset_combo) != list(range(length)):
                continue
                
            # Get the charsets for this combination
            current_charsets = [charsets[i] for i in range(length)]
            
            # Calculate total possible combinations for this length
            total_combinations = 1
            for charset in current_charsets:
                total_combinations *= len(charset)
            
            # Print warning if this will be huge
            if total_combinations > 1000000:
                print(f"Warning: Generating {total_combinations:,} combinations for mask length {length}...")
            
            # Generate all combinations using itertools.product
            combinations.extend([''.join(combo) for combo in itertools.product(*current_charsets)])
    
    return combinations

def apply_masks(words, append_mask=None, prepend_mask=None, synchronize=False, increment=False):
    """
    Apply masks to a list of words, either appending, prepending, or both.
    
    Parameters:
    - words: List of words to transform
    - append_mask: Hashcat-style mask to append (?a?d?s etc.)
    - prepend_mask: Hashcat-style mask to prepend (?a?d?s etc.)
    - synchronize: If True, synchronize prepend and append masks
    - increment: If True, apply incremental mask lengths
    
    Returns:
    - Sorted list of transformed words
    """
    if not words:
        return []
    
    # Parse masks to get character sets
    append_charsets = parse_mask(append_mask) if append_mask else []
    prepend_charsets = parse_mask(prepend_mask) if prepend_mask else []
    
    result = set(words)  # Start with original words
    
    # Handle the case where both synchronize and increment are True
    if synchronize and increment and append_charsets and prepend_charsets:
        print("Applying synchronized incremental masks...")
        
        # Get the maximum lengths
        prepend_max_length = len(prepend_charsets)
        append_max_length = len(append_charsets)
        
        # For each incremental length for prepend
        for prepend_length in range(1, prepend_max_length + 1):
            current_prepend_charsets = prepend_charsets[:prepend_length]
            prepend_combinations = list(itertools.product(*current_prepend_charsets))
            
            # For each incremental length for append
            for append_length in range(1, append_max_length + 1):
                current_append_charsets = append_charsets[:append_length]
                append_combinations = list(itertools.product(*current_append_charsets))
                
                total_combinations = len(prepend_combinations) * len(append_combinations)
                if total_combinations > 1000000:
                    print(f"Warning: Generating {total_combinations:,} synchronized combinations for prepend length {prepend_length} and append length {append_length}...")
                
                # Generate all combinations
                for word in words:
                    for prepend_combo in prepend_combinations:
                        prepend_str = ''.join(prepend_combo)
                        for append_combo in append_combinations:
                            append_str = ''.join(append_combo)
                            result.add(prepend_str + word + append_str)
        
    # Handle just synchronize without increment
    elif synchronize and append_charsets and prepend_charsets:
        print("Applying synchronized masks...")
        
        # Don't truncate - use the full length of each mask
        # but ensure we synchronize the generation
        
        # Calculate total combinations for each mask
        append_combinations = list(itertools.product(*append_charsets))
        prepend_combinations = list(itertools.product(*prepend_charsets))
        
        total_combinations = len(append_combinations) * len(prepend_combinations)
        
        if total_combinations > 1000000:
            print(f"Warning: Generating {total_combinations:,} synchronized combinations...")
        
        # Generate all combinations for each word
        for word in words:
            for prepend_combo in prepend_combinations:
                prepend_str = ''.join(prepend_combo)
                for append_combo in append_combinations:
                    append_str = ''.join(append_combo)
                    result.add(prepend_str + word + append_str)
    
    # Handle just increment without synchronize
    elif increment:
        # Generate incremental mask combinations
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
        
        # Apply append combinations
        if append_combinations:
            print(f"Applying {len(append_combinations):,} append combinations...")
            for word in words:
                for combo in append_combinations:
                    result.add(word + combo)
        
        # Apply prepend combinations
        if prepend_combinations:
            print(f"Applying {len(prepend_combinations):,} prepend combinations...")
            for word in words:
                for combo in prepend_combinations:
                    result.add(combo + word)
    
    # Handle regular (non-incremental, non-synchronized) mask application
    else:
        # Generate mask combinations
        append_combinations = generate_mask_combinations(append_charsets) if append_charsets else []
        prepend_combinations = generate_mask_combinations(prepend_charsets) if prepend_charsets else []
        
        # Apply append combinations
        if append_combinations:
            print(f"Applying {len(append_combinations):,} append combinations...")
            for word in words:
                for combo in append_combinations:
                    result.add(word + combo)
        
        # Apply prepend combinations
        if prepend_combinations:
            print(f"Applying {len(prepend_combinations):,} prepend combinations...")
            for word in words:
                for combo in prepend_combinations:
                    result.add(combo + word)
    
    return sorted(result)

def mentalize(words, leet=False, toggle=False, underscores=False, spaces=False, hyphens=False, 
              append_mask=None, prepend_mask=None, synchronize=False, increment=False):
    """
    Apply various transformations to a list of words.
    
    Parameters:
    - words: List of words to transform
    - leet: Apply leetspeak transformations
    - toggle: Apply case toggling
    - underscores: Insert underscores between characters
    - spaces: Insert spaces between characters
    - hyphens: Insert hyphens between characters
    - append_mask: Hashcat-style mask to append (?a?d?s etc.)
    - prepend_mask: Hashcat-style mask to prepend (?a?d?s etc.)
    - synchronize: If True, synchronize prepend and append masks
    - increment: If True, apply incremental mask lengths
    
    Returns:
    - Sorted list of transformed words
    """
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
        
        mutated.update(variants)
    
    # Apply mask patterns after basic mutations
    if append_mask or prepend_mask:
        mutated = apply_masks(list(mutated), append_mask, prepend_mask, synchronize, increment)
    
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
    return sorted(combined)
