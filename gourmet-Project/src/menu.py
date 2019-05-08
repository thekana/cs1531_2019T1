from src.item import Item, Burger, Wrap, Drink, Side
from src.order import Order
'''
Menu: a class used to store menu information, which is composed of items.
'''


class Menu:

    def __init__(self, menu_name: str):
        # the name for the menu, e.g. Mains, Drinks ...
        self._name = menu_name
        self._nitems = 0         # the number of items inside
        self._items = {}    # a dict for items

    # add some items into the menu
    def add_items(self, *argv: Item):
        for item in argv:
            self._items[item.name] = item
            self._nitems += 1

    # get an item by its name
    def get_item(self, item_name: str) -> Item:
        if item_name in self._items.keys():
            return self._items[item_name]
        else:
            return None

    # print all the items inside the menu
    def display(self):
        items = []
        print(f"{self.name}:")
        for item in self._items.values():
            items.append(item)
            item = f"<{item.name}> Price: {item.price}" 
            print(item)
        return items

    # put items into an order
    def putin_order(self, order: Order, *argv: Item):
        for item_name in argv:
            item = self.get_item(item_name)
            if item:
                order.add_item(item)

    '''
    Property
    '''

    @property
    def name(self):
        return self._name

    @property
    def nitem(self):
        return self._nitems
    
    @property
    def items(self):
        return self._items

    '''
    str
    '''

    def __str__(self):
        return f"Menu {self._name}: {self._nitems} item(s)"


if __name__ == "__main__":
    coke_zero = Drink("Coke Zero", 2.5)
    coke_diet = Drink("Coke Diet", 2.5) 
    drink_menu = Menu("Drink")
    drink_menu.add_items(coke_diet, coke_zero)
    print(drink_menu)
    drink_menu.display()