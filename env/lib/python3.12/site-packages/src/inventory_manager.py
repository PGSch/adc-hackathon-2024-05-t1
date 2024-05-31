class InventoryManager:
    def __init__(self):
        """
        Initializes the inventory manager with an empty inventory.
        """
        self.inventory = {}

    def add_item(self, item, quantity):
        """
        Adds a specified quantity of an item to the inventory.

        Args:
        item (str): The name of the item to add.
        quantity (int): The number of items to add.

        Raises:
        ValueError: If the quantity is negative or item is not a string or item name is empty.
        TypeError: If the quantity is not an integer.
        """
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer")

        if quantity < 0:
            raise ValueError("Quantity must be non-negative")

        if not isinstance(item, str) or item == "":
            raise ValueError("Item must be a non-empty string")

        if not item.isascii():
            raise ValueError("Item name must contain only ASCII characters")

        if len(item) > 1000:
            raise ValueError("Item name is too long")

        if any(not c.isalnum() and c not in [' ', '-'] for c in item):
            raise ValueError("Item name can only contain alphanumeric characters, spaces, or hyphens")

        try:
            if item in self.inventory:
                self.inventory[item] += quantity
            else:
                self.inventory[item] = quantity
        except Exception as e:
            raise ValueError("System interruption occurred while adding the item")