# imports
import pytest  # used for our unit tests

# function to test
from src.inventory_manager import InventoryManager


# unit tests
@pytest.fixture
def manager():
    return InventoryManager()


def test_add_item_positive_integer(manager):
    manager.add_item("apple", 5)
    assert manager.check_inventory("apple") == 5


def test_add_item_positive_float(manager):
    manager.add_item("banana", 3.5)
    assert manager.check_inventory("banana") == 3.5


def test_add_item_zero_quantity(manager):
    manager.add_item("orange", 0)
    assert manager.check_inventory("orange") == 0


def test_add_item_negative_quantity(manager):
    with pytest.raises(ValueError):
        manager.add_item("pear", -2)


def test_remove_item_positive_integer(manager):
    manager.add_item("apple", 10)
    manager.remove_item("apple", 3)
    assert manager.check_inventory("apple") == 7


def test_remove_item_positive_float(manager):
    manager.add_item("banana", 5.5)
    manager.remove_item("banana", 2.5)
    assert manager.check_inventory("banana") == 3.0


def test_remove_item_zero_quantity(manager):
    manager.add_item("orange", 8)
    manager.remove_item("orange", 0)
    assert manager.check_inventory("orange") == 8


def test_remove_item_negative_quantity(manager):
    with pytest.raises(ValueError):
        manager.remove_item("pear", -1)


def test_remove_item_not_found(manager):
    with pytest.raises(ValueError):
        manager.remove_item("grape", 3)


def test_remove_item_not_enough_inventory(manager):
    manager.add_item("melon", 5)
    with pytest.raises(ValueError):
        manager.remove_item("melon", 8)


def test_check_inventory_existing_item(manager):
    manager.add_item("apple", 10)
    assert manager.check_inventory("apple") == 10


def test_check_inventory_non_existing_item(manager):
    assert manager.check_inventory("kiwi") == 0
