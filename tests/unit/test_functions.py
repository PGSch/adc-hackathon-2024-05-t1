# imports
import pytest  # used for our unit tests

# function to test
from src.inventory_manager import InventoryManager

# unit tests
@pytest.fixture
def manager():
    return InventoryManager()

def test_valid_input(manager):
    manager.add_item("Apple", 10)
    assert manager.inventory == {"Apple": 10}

def test_quantity_validation_negative(manager):
    with pytest.raises(ValueError):
        manager.add_item("Banana", -5)

def test_quantity_validation_non_integer(manager):
    with pytest.raises(TypeError):
        manager.add_item("Orange", "10")

def test_item_name_validation_empty_string(manager):
    with pytest.raises(ValueError):
        manager.add_item("", 5)

def test_item_name_validation_too_long(manager):
    with pytest.raises(ValueError):
        manager.add_item("VeryLongItemName" * 100, 5)

def test_item_name_validation_special_characters(manager):
    with pytest.raises(ValueError):
        manager.add_item("@#$", 5)

def test_item_name_validation_non_ascii(manager):
    with pytest.raises(ValueError):
        manager.add_item("Résumé", 5)

def test_existing_item_add_quantity(manager):
    manager.add_item("Apple", 5)
    manager.add_item("Apple", 3)
    assert manager.inventory == {"Apple": 8}

def test_existing_item_add_zero_quantity(manager):
    manager.add_item("Apple", 5)
    manager.add_item("Apple", 0)
    assert manager.inventory == {"Apple": 5}

def test_existing_item_add_negative_quantity(manager):
    with pytest.raises(ValueError):
        manager.add_item("Apple", -3)

# Add the edge case tests as well following a similar pattern