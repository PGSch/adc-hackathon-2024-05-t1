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
            raise ValueError("Quantity must be non-negative")
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
        ValueError: If the quantity is negative or more than the available quantity.
        """
        if quantity < 0:
            raise ValueError("Quantity must be non-negative")
        if item not in self.inventory or self.inventory[item] < quantity:
            raise ValueError("Not enough inventory")
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
        return self.inventory.get(item, 0)


def pig_latin(text):
    def translate(word):
        vowels = "aeiou"
        if word[0] in vowels:
            return word + "way"
        else:
            consonants = ""
            for letter in word:
                if letter not in vowels:
                    consonants += letter
                else:
                    break
            return word[len(consonants) :] + consonants + "ay"

    words = text.lower().split()
    translated_words = [translate(word) for word in words]
    return " ".join(translated_words)
