class InventoryManager:
    def __init__(self):
        self.inventory = {}

    def add_item(self, item, quantity):
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer")

        if quantity < 0:
            raise ValueError("Quantity must be non-negative")

        if not isinstance(item, str) or item == "":
            raise ValueError("Item must be a non-empty string")

        if len(item) > 1000:
            raise ValueError("Item name is too long")

        if not all(c.isalnum() or c in [' ', '-'] for c in item):
            raise ValueError("Item name can only contain alphanumeric characters, spaces, or hyphens")

        if not item.isascii():
            raise ValueError("Item name must contain only ASCII characters")

        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity