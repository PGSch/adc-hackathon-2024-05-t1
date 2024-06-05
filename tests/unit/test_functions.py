# imports
import pytest  # used for our unit tests

# function to test
from src.inventory_manager import InventoryManager

# unit tests
@pytest.mark.parametrize("item, quantity", [
    ("", 5),  # Testing edge case: Empty String as Item Name
    ("apple", 10**12),  # Testing edge case: Extremely Large Quantity Values
    ("apple@123", 3),  # Testing edge case: Non-Alphanumeric Characters in Item Name
    ("🍎", 2),  # Testing edge case: Unicode Characters in Item Name
    ("banana", 2.5)  # Testing edge case: Decimal Quantity Values
])
def test_edge_cases(item, quantity):
    manager = InventoryManager()
    
    if quantity < 0:
        with pytest.raises(ValueError):
            manager.add_item(item, quantity)
    else:
        manager.add_item(item, quantity)
        assert manager.inventory.get(item, 0) == quantity