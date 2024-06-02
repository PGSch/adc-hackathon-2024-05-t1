# imports
import pytest  # used for our unit tests

# function to test
from src.inventory_manager import InventoryManager


# unit tests
# Test adding items with a valid quantity
@pytest.mark.parametrize("item, quantity", [("item1", 5), ("item2", 3)])
def test_add_item_valid_quantity(item, quantity):
    manager = InventoryManager()
    manager.add_item(item, quantity)
    assert manager.check_inventory(item) == quantity


# Test handling invalid input
@pytest.mark.parametrize("item, quantity", [("item3", -2), ("item4", 2.5)])
def test_add_item_invalid_input(item, quantity):
    manager = InventoryManager()
    with pytest.raises(ValueError):
        manager.add_item(item, quantity)


# Test removing items with a valid quantity
@pytest.mark.parametrize(
    "item, initial_quantity, quantity_to_remove", [("item1", 5, 3), ("item2", 8, 8)]
)
def test_remove_item_valid_quantity(item, initial_quantity, quantity_to_remove):
    manager = InventoryManager()
    manager.add_item(item, initial_quantity)
    manager.remove_item(item, quantity_to_remove)
    assert manager.check_inventory(item) == initial_quantity - quantity_to_remove


# Test handling errors and edge cases
@pytest.mark.parametrize("item, quantity", [("item5", -2), ("item6", 3.5)])
def test_remove_item_invalid_input(item, quantity):
    manager = InventoryManager()
    with pytest.raises(ValueError):
        manager.add_item(item, 5)
        manager.remove_item(item, quantity)


# Test checking the inventory for different items
@pytest.mark.parametrize("item, quantity", [("item1", 5), ("item7", 0)])
def test_check_inventory(item, quantity):
    manager = InventoryManager()
    manager.add_item("item1", 5)
    assert manager.check_inventory(item) == quantity


# Test retrieving accurate inventory quantities
def test_check_inventory_after_actions():
    manager = InventoryManager()
    item = "item1"
    manager.add_item(item, 5)
    assert manager.check_inventory(item) == 5
    manager.remove_item(item, 2)
    assert manager.check_inventory(item) == 3
