from typing import Dict, Iterable, List

# Maximum length of any generated Key. Lower numbers may cause more collisions. 
# Choose a value < 0 to disable an upper limit!
MAX_KEY_LENGTH = 3

class KeyGenError(Exception):
    pass


# Maps full strings to a shortend key 
def get_unique_keys_from_set(items: Iterable[str]) -> Dict[str, str]:
    key_map: Dict[str, str] = {}
    
    # Sort items to get deterministic output
    items = list(items)

    for item in items:
        prefix_len = 1

        while True:
            if prefix_len > len(item) or (prefix_len > MAX_KEY_LENGTH and MAX_KEY_LENGTH > 0):
                break

            simple_conflict = [k for k in key_map.keys() if k.startswith(item[:prefix_len])]
            hard_conflict = item[:prefix_len] in key_map.keys()

            if not simple_conflict and not hard_conflict:
                break

            if hard_conflict:
                old_key = item[:prefix_len]
                prefix_len += 1
                old_item = key_map[old_key]
                if prefix_len > len(old_item):
                    raise KeyGenError(f"Cannot get unique key from set. Conflict between '{old_item}' and '{item}'")
                
                new_key = old_item[:prefix_len]
                key_map.pop(old_key)
                key_map[new_key] = old_item
            else:
                # only a simple conflict
                prefix_len += 1
        
        if prefix_len > len(item):
            raise KeyGenError(f"Could not choose a key for {item} that is not the whole string and does not collide with other keys. Try renaming values in your key set")

        if (hard_conflict or simple_conflict) and (prefix_len > MAX_KEY_LENGTH and MAX_KEY_LENGTH > 0):
            raise KeyGenError(f"Could not choose a key for {item} that is a maximum of {MAX_KEY_LENGTH} characters long and does not collide with other keys. Try increasing the MAX_KEY_LENGTH or renaming values in your key set")
        
        key_map[item[:prefix_len]] = item

    name_map = dict((v, k) for k, v in key_map.items())

    if len(name_map.keys()) != len(items):
        missing = [k for k in items if k not in name_map.keys()]
        raise KeyGenError(f"Failed generating unique keymap! Following entities did not receive a key: {missing}")
    
    return name_map