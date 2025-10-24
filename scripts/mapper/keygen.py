from typing import Dict, Iterable, List

# Maximum length of any generated Key. Lower numbers may cause more collisions. 
# Choose a value < 0 to disable an upper limit!
MAX_KEY_LENGTH = 3

class KeyGenError(Exception):
    pass

# Maps full strings to a shortend key 
def get_unique_keys_from_set(items: Iterable[str]) -> Dict[str, str]:
    key_map: Dict[str, str] = {}
    for item in items:
        prefix_len = 1
        while item[:prefix_len] in key_map.values() and prefix_len <= len(item) and (prefix_len < MAX_KEY_LENGTH or MAX_KEY_LENGTH < 0):
            old_key = item[:prefix_len]
            prefix_len += 1
            old_item = key_map[old_key]
            if prefix_len > len(old_item):
                raise KeyGenError(f"Cannot get unique key from set. Conflict between '{old_item}' and '{item}'")
            
            new_key = old_item[:prefix_len]
            key_map.pop(old_key)
            key_map[new_key] = old_item
        
        if prefix_len > len(item):
            raise KeyGenError(f"Could not choose a key for {item} that is not the whole string and does not collide with other keys. Try renaming values in your key set")

        if item[:prefix_len] in key_map.values() and (prefix_len >= MAX_KEY_LENGTH and MAX_KEY_LENGTH > 0):
            raise KeyGenError(f"Could not choose a key for {item} that is a maximum of {MAX_KEY_LENGTH} characters long and does not collide with other keys. Try increasing the MAX_KEY_LENGTH or renaming values in your key set")
        
        key_map[item[:prefix_len]] = item
    
    return dict((v, k) for k, v in key_map.items())