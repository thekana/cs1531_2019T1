from src.item import Item, Burger, Wrap, Side, Drink
from src.inventory import Inventory
from src.ingredient import Ingredient, isNaN
from copy import deepcopy
'''
Order: a class used to store information about online orders.
'''


class Order(object):

    def __init__(self, order_id: int):
        self._order_id = order_id

        # Order status fields:
        self._is_payed = False            # boolean, whether it is payed or not
        self._is_prepared = False       # boolean, whether it is prepared or not

        # Customized fields:
        # Dictionary key = item name, value = list of item (to support duplicate)
        self._items = { }
        # float, the total price for the order
        self._price = float('nan')
        # string, some special notes by the customer
        self._notes = ''


    # if Order is payed
    def update_payment_status(self, status: bool):
        self._is_payed = status


    # if Order is ready
    def update_preparation_status(self, status: bool):
        self._is_prepared = status


    # add new items into an order
    # dont call this
    def add_items(self, *argv: Item):
        for item in argv:
            if item.name in self._items:
                self._items[item.name].append(item)
            else:
                self._items[item.name] = [item]
            self.calculate_price()


    #function to delete items from order
    def delete_items(self, itemID: str):
        for item_name in self._items.keys():
            if len(self._items[item_name]) == 1:
                if self._items[item_name][0].uniqueid == itemID:
                    del self._items[item_name]
                    self.calculate_price()
                    return
            else:
                count = 0
                for inneritem in self._items[item_name]:
                    if inneritem.uniqueid == itemID:
                        del self._items[item_name][count]
                        self.calculate_price()
                        return
                    count+=1

        
    # calculate order price
    def calculate_price(self):
        price = 0
        for item_list in self._items.values():
            for item in item_list:
                price = price + item.price
        self._price = price


    # Display the items of orders
    def display(self):
        print('Order {0} has items:'.format(self._order_id))
        for item_list in self._items.values():
            for item in item_list:
                print(item)
        print('Total price: ${}'.format(self._price))
        print("Paid?",self.is_payed)
        print("Prepared?",self.is_prepared)


    def check_order_availability(self, inventory: Inventory) -> bool:
        temp_inventory = deepcopy(inventory)
        for items_list in self.items.values():
            for item in items_list:
                for ingredient_list in item._ingredients.values():
                    if ingredient_list.__class__.__name__ == "Ingredient":
                        if not temp_inventory.is_available(ingredient_list.name, ingredient_list.amount):
                            print(f"Inventory not enough for {ingredient_list.amount} {ingredient_list.name}")
                            return False
                        temp_inventory.update_stock(ingredient_list.name, -ingredient_list.amount)

                    else:
                        for ingredient in ingredient_list.values():
                            assert(ingredient.__class__.__name__ == "Ingredient")
                            if not isNaN(ingredient.amount) and not temp_inventory.is_available(ingredient.name, ingredient.amount):
                                print(f"Inventory not enough for {ingredient.amount} {ingredient.name}")
                                return False
                            temp_inventory.update_stock(ingredient.name, -ingredient.amount)
        return True

    # update inventory for the order
    def update_order_inventory(self, inventory: Inventory):
        for items_list in self.items.values():
            for item in items_list:
                for ingredient_list in item._ingredients.values():
                    if ingredient_list.__class__.__name__ == "Ingredient":
                        inventory.update_stock(ingredient_list.name,-ingredient_list.amount)
                    else: 
                        for ingredient in ingredient_list.values():
                            assert(ingredient.__class__.__name__ == "Ingredient")
                            if not isNaN(ingredient.amount):
                                inventory.update_stock(ingredient.name,-ingredient.amount)

    '''
    Property
    '''

    @property
    def items(self):
        return self._items

    @property
    def is_prepared(self):
        return self._is_prepared

    @property
    def is_payed(self):
        return self._is_payed

    @property
    def order_id(self):
        return self._order_id

    @property
    def price(self):
        return self._price
    
    @is_prepared.setter
    def is_prepared(self,vara):
       self._is_prepared = vara

    '''
    str
    '''

    def __str__(self):
        return f"Order ID: {self._order_id}, Total Price: {self._price:.2f}"


if __name__ == "__main__":
    pass
