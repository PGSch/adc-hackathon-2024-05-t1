# imports
import pytest  # used for our unit tests

# function to test
from src.inventory_manager import InventoryManager

# unit tests
@pytest.mark.parametrize(
    "item, quantity",
    [
        # Testing valid inputs
        ("apple", 5),
        ("banana", 10),
        ("apple", 3),
        ("apple orange", 2),

        # Testing invalid inputs for quantity
        ("pear", -1),
        ("grapes", "invalid"),
        ("kiwi", 3.5),

        # Testing invalid inputs for item
        ("", 5),
        ("a" * 1001, 3),
        ("©", 2),
        ("^$#@", 3),

        # Testing edge cases
        ("max_length_item_name" * 100, 5),
        ("zero_quantity", 0),
        ("large_quantity_item", 999999999999),
        ("scientific_notation", 1e5),
        ("item_unicode_😃", 4),

        # Testing rare edge cases
        ("\x00", 5),
        ("item_with_emojis_🍇🍌", 10),
        ("large_quantity_item_overflow", 999999999999999999999999999999),
        ("scientific_notation_overflow", 1e50),
        ("float_precision_issue", 2.999999999999999),
        ("concurrent_item_addition", 3),
        ("item_unicode_Название", 6),
        ("item_unicode_𝓟", 7),
    ]
)
def test_add_item(item, quantity):
    inventory_manager = InventoryManager()
    inventory_manager.add_item(item, quantity)
    
    # Add assertions to check the expected behavior after calling add_item
    pass