# imports
import pytest
from src.inventory_manager import InventoryManager

# function to test
# class InventoryManager is imported from src.inventory_manager

# unit tests
@pytest.fixture
def empty_inventory_manager():
    return InventoryManager()

@pytest.mark.parametrize("item, quantity", [
    ("apple", 5),
    ("banana", 10),
    ("orange", 0),
])
def test_add_item(empty_inventory_manager, item, quantity):
    empty_inventory_manager.add_item(item, quantity)
    assert empty_inventory_manager.check_inventory(item) == quantity

def test_add_item_negative_quantity(empty_inventory_manager):
    with pytest.raises(ValueError):
        empty_inventory_manager.add_item("apple", -5)

@pytest.mark.parametrize("item, quantity", [
    ("apple", 5),
    ("banana", 10),
    ("orange", 3),
])
def test_remove_item(empty_inventory_manager, item, quantity):
    empty_inventory_manager.add_item(item, quantity)
    empty_inventory_manager.remove_item(item, quantity)
    assert empty_inventory_manager.check_inventory(item) == 0

def test_remove_item_negative_quantity(empty_inventory_manager):
    with pytest.raises(ValueError):
        empty_inventory_manager.remove_item("apple", -5)

def test_remove_item_not_in_inventory(empty_inventory_manager):
    with pytest.raises(ValueError):
        empty_inventory_manager.remove_item("grapes", 2)

def test_remove_item_insufficient_quantity(empty_inventory_manager):
    empty_inventory_manager.add_item("apple", 5)
    with pytest.raises(ValueError):
        empty_inventory_manager.remove_item("apple", 10)

def test_check_inventory_existing_item(empty_inventory_manager):
    empty_inventory_manager.add_item("apple", 5)
    assert empty_inventory_manager.check_inventory("apple") == 5

def test_check_inventory_non_existing_item(empty_inventory_manager):
    assert empty_inventory_manager.check_inventory("grapes") == 0