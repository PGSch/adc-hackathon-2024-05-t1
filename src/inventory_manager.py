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
        quantity (int or float): The number of items to add.

        Raises:
        ValueError: If the quantity is negative or not a number.
        """
        if not isinstance(quantity, (int, float)) or quantity < 0:
            raise ValueError('Quantity must be a non-negative number')

        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def remove_item(self, item, quantity):
        """
        Removes a specified quantity of an item from the inventory.

        Args:
        item (str): The name of the item to remove.
        quantity (int or float): The number of items to remove.

        Raises:
        ValueError: If the quantity is negative or more than the available quantity.
        """
        if not isinstance(quantity, (int, float)) or quantity < 0:
            raise ValueError('Quantity must be a non-negative number')

        if item not in self.inventory:
            raise ValueError('Item not found in inventory')

        if self.inventory[item] < quantity:
            raise ValueError('Not enough inventory')

        self.inventory[item] -= quantity

    def check_inventory(self, item):
        """
        Returns the quantity of the item in the inventory.

        Args:
        item (str): The name of the item to check.

        Returns:
        int: The quantity of the item in the inventory.
        """
        return self.inventory.get(item, 0)