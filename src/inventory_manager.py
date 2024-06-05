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
        ValueError: If the quantity is negative.
        """
        if quantity < 0:
            raise ValueError('Quantity must be non-negative')

        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def remove_item(self, item, quantity):
        """
        Removes a specified quantity of an item from the inventory.

        Args:
        item (str): The name of the item to remove.
        quantity (int): The number of items to remove.

        Raises:
        ValueError: If the quantity is negative, the item is not in the inventory, or the quantity to remove exceeds the available quantity.
        """
        if quantity < 0:
            raise ValueError('Quantity must be non-negative')

        if item not in self.inventory:
            raise ValueError('Not enough inventory')

        if self.inventory[item] < quantity:
            raise ValueError('Not enough inventory')

        self.inventory[item] -= quantity

        if self.inventory[item] == 0:
            del self.inventory[item]

    def check_inventory(self, item):
        """
        Returns the quantity of the item in the inventory.

        Args:
        item (str): The name of the item to check.

        Returns:
        int: The quantity of the item in the inventory.
        """
        if not isinstance(item, str):
            raise TypeError('Item should be a string')

        return self.inventory.get(item, 0)