# imports
import pytest  # used for our unit tests

# function to test
from src.inventory_manager import InventoryManager

# unit tests
@pytest.mark.parametrize("item_name, quantity, expected_output", [
    ("apple", 5, 5),  # testing adding a new item to inventory
    ("banana", 10, 10),  # testing adding a new item to inventory
    ("apple", -2, "Invalid quantity"),  # testing adding a negative quantity
    ("banana", 0, "Invalid quantity"),  # testing adding zero quantity
    ("apple", 3, 8),  # testing adding quantity to existing item
    ("banana", 5, 15),  # testing adding quantity to existing item
    ("grapes", 5, "Item not found"),  # testing adding quantity to non-existing item
])
def test_add_item_to_inventory(item_name, quantity, expected_output):
    # Arrange
    inventory_manager = InventoryManager()
    
    # Act
    actual_output = inventory_manager.add_item(item_name, quantity)
    
    # Assert
    assert actual_output == expected_output