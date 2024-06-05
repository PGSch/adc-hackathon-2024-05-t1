# imports
import pytest  # used for our unit tests

# function to test
from src.inventory_manager import InventoryManager

# unit tests
@pytest.mark.parametrize("item, quantity, expected_output", [
    ("apple", 5, 5),
    ("banana", 10, 10),
    ("orange", 3, 3),
])
def test_add_item(item, quantity, expected_output):
    # Arrange
    inventory_manager = InventoryManager()
    
    # Act
    inventory_manager.add_item(item, quantity)
    
    # Assert
    assert inventory_manager.items[item] == expected_output

@pytest.mark.parametrize("item, quantity, expected_output", [
    ("apple", 5, 5),
    ("banana", 10, 10),
    ("orange", 3, 3),
])
def test_remove_item(item, quantity, expected_output):
    # Arrange
    inventory_manager = InventoryManager()
    inventory_manager.add_item(item, 10)
    
    # Act
    inventory_manager.remove_item(item, quantity)
    
    # Assert
    assert inventory_manager.items[item] == expected_output