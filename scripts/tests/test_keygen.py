import pytest
from mapper.keygen import get_unique_keys_from_set, KeyGenError, MAX_KEY_LENGTH

def test_unique_keys_normal():
    items = ["Apple", "Banana", "Carrot"]
    key_map = get_unique_keys_from_set(items)
    
    assert len(key_map.keys()) == 3
    assert key_map["Apple"] == "A"
    assert key_map["Banana"] == "B"
    assert key_map["Carrot"] == "C"

def test_collision_resolved_by_longer_prefix():
    items = ["Apple", "Apricot", "Banana"]
    key_map = get_unique_keys_from_set(items)
    
    assert len(key_map.keys()) == 3
    assert key_map["Apple"] == "App"
    assert key_map["Apricot"] == "Apr"
    assert key_map["Banana"] == "B"

def test_collision_too_short_raises_error():
    # Both start with "App", MAX_KEY_LENGTH=3 -> cannot resolve
    items = ["App", "Apple"]
    with pytest.raises(KeyGenError):
        get_unique_keys_from_set(items)

def test_single_item():
    items = ["Unique"]
    key_map = get_unique_keys_from_set(items)

    assert len(key_map.keys()) == 1
    assert key_map["Unique"] == "U"

def test_common_prefix_within_max_key_length():
    items = ["Cat", "Car", "Can"]
    # All start with "Ca", MAX_KEY_LENGTH=3 allows full resolution
    key_map = get_unique_keys_from_set(items)
    
    assert len(key_map.keys()) == 3
    assert key_map["Cat"] == "Cat"
    assert key_map["Car"] == "Car"
    assert key_map["Can"] == "Can"

def test_items_too_short_raises_error():
    items = ["A", "A"]
    with pytest.raises(KeyGenError):
        get_unique_keys_from_set(items)