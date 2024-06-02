# imports
import pytest  # used for our unit tests

# function to test
from src.inventory_manager import InventoryManager

# unit tests
class TestInventoryManager:
    @pytest.fixture
    def manager(self):
        return InventoryManager()

    @pytest.mark.parametrize("item, quantity", [
        ("apple", 5),  # Add a new item with a positive quantity
        ("banana", 10),  # Add an existing item with a positive quantity
        ("orange", -3),  # Attempt to add an item with a negative quantity
    ])
    def test_add_item(self, manager, item, quantity):
        if quantity < 0:
            with pytest.raises(ValueError):
                manager.add_item(item, quantity)
        else:
            manager.add_item(item, quantity)
            assert manager.check_inventory(item) == quantity

    @pytest.mark.parametrize("item, quantity", [
        ("apple", 2),  # Remove an existing item with a positive quantity
        ("banana", -5),  # Attempt to remove an item with a negative quantity
        ("orange", 10),  # Attempt to remove more quantity than available
        ("apple", 2),  # Remove an item to make its quantity zero
    ])
    def test_remove_item(self, manager, item, quantity):
        manager.add_item(item, 5)  # Add some initial quantity for testing removal
        if quantity < 0 or quantity > 5:
            with pytest.raises(ValueError):
                manager.remove_item(item, quantity)
        else:
            manager.remove_item(item, quantity)
            if quantity == 5:
                assert manager.check_inventory(item) == 0
            else:
                assert manager.check_inventory(item) == 5 - quantity

    @pytest.mark.parametrize("item, expected_quantity", [
        ("apple", 0),  # Check the quantity of an existing item in the inventory
        ("banana", 0),  # Check the quantity of a non-existing item in the inventory
        ("orange", 3),  # Check the quantity of an item after adding and removing quantities
    ])
    def test_check_inventory(self, manager, item, expected_quantity):
        manager.add_item("orange", 3)  # Add an item for testing inventory check
        assert manager.check_inventory(item) == expected_quantity

    # Add more test cases for the edge scenarios mentioned above
    # Remember to handle each edge case appropriately with assertions and exception handling