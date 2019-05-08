from src.ingredient import Ingredient, isNaN
from src.inventory import Inventory
import math
import uuid
'''
This is a class for food items such as burgers, wraps, drinks and sides.
A completely customized burger with many ingredients will be classified as an item to be put in an order.

An item that has every ingredients for a particular type (main,side,drinks) will be used to show in menu.

User should see the lists of available ingredients in the item through menu through system.
And through the system, user may create their item using shown ingredients and add to their order.

Class:
  - Item
    - Main
      - Burger
      - Wrap
    - Drink
    - Side
    - Sundae
'''


class Item(object):

    def __init__(self, name: str, price: float, type: str, description: str = 'N/A', availability: bool = True):
        self._name = name
        self._price = price
        self._type = type                       # "Mains", "Sides", "Drinks"

        # optional fields:
        self._description = description         # string
        self._is_available = availability       # boolean

        # other fields:
        self._ingredients = {}                  # dict<ingredient>
        self._uuid = ''
                               # error messages
    # add ingredients into the item
    def add_ingredients(self, *argv: Ingredient):
        for ingredient in argv:
            self._ingredients[ingredient.name] = ingredient

    # check whether this item is available in the inventory, based on whether its ingredients are available
    # This method is not suitable for Mains class
    def _check_availability(self, inventory: Inventory):
        for ingredient in self._ingredients.values():
            if ingredient.amount == 0:
                self._is_available = False
                return
            else:
                if (not isNaN(ingredient.amount) and not inventory.is_available(ingredient.name, ingredient.amount)):
                    self._is_available = False
                    return
        self._is_available = True

    # this method will return whether available
    def is_available(self, inventory: Inventory):
        self._check_availability(inventory)
        return self._is_available

    def generateID(self):
        self._uuid = str(uuid.uuid4())
    '''
    Property
    '''

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def type(self):
        return self._type

    @property
    def description(self):
        return self._description

    @property
    def ingredients(self):
        return self._ingredients

    @property
    def uniqueid(self):
        return self._uuid
    '''
    str, equal, notequal
    '''

    def __str__(self):
        return (f"{self._type}: {self._name}, price: ${self._price:.2f}, description: {self._description}")


'''
This should be a special class for the mains.
Notes: There should be a defaulted ingredients list for a main food and corresponding limits.
'''
# when we instantiate main object (FOR MENU) price should be start at 0


class Main(Item):

    def __init__(self, name: str, price: float = 0, description: str = 'N/A', availability: bool = True):
        super().__init__(name, price, "Mains", description, availability)
        # dict<Ingredient>
        self._ingredients = {}
        # dict<int>
        self._max_limit = {}
        # float, price + additional price
        self._total_price = price
        self._errors = {}

    # Code to add ingredients in the main
    def add_ingredients(self, *argv: Ingredient):
        for ingredient in argv:
            if "Bun" in ingredient.name:
                self._ingredients["Bun"][ingredient.name] = ingredient
            elif "Patty" in ingredient.name:
                self._ingredients["Patty"][ingredient.name] = ingredient
            #This wrap refers to base material which is used in constructing the main wrap
            elif  "Wrap" in ingredient.name:
                self._ingredients["Wrap"][ingredient.name] = ingredient
            else:
                self._ingredients["Other"][ingredient.name] = ingredient

    def set_ingredient_limit(self, ingredient_name: str, amount: float):
        if ingredient_name not in ("Bun", "Patty", "Wrap") and ingredient_name not in self._ingredients['Others'].keys():
            print(f"<{ingredient_name}> not in the item!")
            return f"<{ingredient_name}> not in the item!"
        self._max_limit[ingredient_name] = amount

    def getSumInMain(self,ingredient_type: str):
        sum = 0
        for ingredient in self._ingredients[ingredient_type].values():
            sum += ingredient.amount if not isNaN(ingredient.amount) else 0
        return sum

    def getLimit(self, ingredient_type: str) -> float:
        if ingredient_type in self._max_limit.keys():
            return self._max_limit[ingredient_type]
        else:
            print(f"<{ingredient_type}> not in limit!")
            return None

    '''
    modify functions
    '''
    # private function to modify ingredients 
    def _modify_ingredients(self, ingredient_type: str, inventory: Inventory, *argv: Ingredient):
        # check input
        if ingredient_type in ("Bun", "Patty", "Wrap"):
            total_amount = 0
            for ingredient in argv:
                total_amount += ingredient.amount
                # if more than max limit, reject
                if ingredient_type in self._max_limit.keys():
                    if (total_amount+self.getSumInMain(ingredient_type)) > self._max_limit[ingredient_type]:
                        print(f"{ingredient_type} are more than the max amount!")
                        self._errors[ingredient_type] = f"{ingredient_type} are more than the max amount!"
                        return
                if not inventory.is_available(ingredient.name, ingredient.amount):
                    print(f"{ingredient.name} is not enough in the inventory!")
                    self._errors[ingredient.name] = f"{ingredient.name} is not enough in the inventory!"
                    return
                self._ingredients[ingredient_type][ingredient.name] = Ingredient(ingredient.name,ingredient.amount,additional_price= ingredient.additional_price)
                ## At this stage we should remove the error from the list
                self._errors.pop(ingredient_type, None)
                self._errors.pop(ingredient.name, None)
                total_amount = 0
        elif ingredient_type == "Other":
            for ingredient in argv:
                # if more than max limit, reject
                if ingredient.name in self._max_limit.keys():
                    if ingredient.amount > self._max_limit[ingredient.name]:
                        print(f"{ingredient.name} are more than the max amount!")
                        return f"{ingredient.name} are more than the max amount!"
                if not inventory.is_available(ingredient.name, ingredient.amount):
                    print(f"{ingredient.name} is not enough in the inventory!")
                    self._errors[ingredient.name] = f"{ingredient.name} is not enough in the inventory!"
                    return
                self._ingredients[ingredient_type][ingredient.name] = Ingredient(ingredient.name,ingredient.amount,additional_price= ingredient.additional_price)
                self._errors.pop(ingredient.name, None)
        else:
            print("invalid ingredient type!")
        
        self.calculate_price()

    def modify_buns(self, inventory: Inventory, *argv: Ingredient):
        self._modify_ingredients("Bun", inventory, *argv)

    def modify_patties(self, inventory: Inventory, *argv: Ingredient):
        self._modify_ingredients("Patty", inventory, *argv)

    def modify_wraps(self, inventory: Inventory, *argv: Ingredient):
        self._modify_ingredients("Wrap", inventory, *argv)

    def modify_other_ingredients(self, inventory: Inventory, *argv: Ingredient):
        self._modify_ingredients("Other", inventory, *argv)

    # calculate the total price according the ingredients' prices and its base price
    def calculate_price(self):
        total_price = self._price
        for ingredient_type in self._ingredients.values():
            for ingredient in ingredient_type.values():
                if not isNaN(ingredient.amount) and not isNaN(ingredient.additional_price):
                    total_price += ingredient.additional_price * ingredient.amount
        self._total_price = total_price

    # display the details of this creation
    def review(self):
        print(str(self))
        return str(self)

    def _check_availability(self, inventory: Inventory):
        # when modifying the ingredients, we have ensured they are available
        self._is_available = True

    def __str__(self):
        pass

    @property
    def price(self):
        return self._total_price


class Burger(Main):

    def __init__(self, name: str = 'Big Mac', price: float = 0, description: str = 'N/A', availability: bool = True):
        super().__init__(name, price, description, availability)
        # dict<Ingredient>
        self._ingredients = {
            'Bun':      {},
            'Patty':    {},
            'Other':    {}  # and other ingredients
        }
        # dict<int>
        self._max_limit = {
            'Bun':      False,
            'Patty':   False
            # and other ingredients
        }
    
    def make_default_burger(self, invent: Inventory):
        self.add_ingredients(
            Ingredient("Muffin Bun", additional_price=1),
            Ingredient("Chicken Patty", additional_price=2),
            Ingredient("Cheddar Cheese", additional_price=0.5))
        self.set_ingredient_limit("Bun", 2)
        self.set_ingredient_limit("Patty", 1)
        self.modify_buns(invent, Ingredient("Muffin Bun", amount=2, additional_price=1))
        self.modify_patties(invent, Ingredient("Chicken Patty", amount=1, additional_price=2))
        self.modify_other_ingredients(invent, Ingredient("Cheddar Cheese", amount=1, additional_price=0.5))
    
    @property
    def ingredientsDict(self):
        return self._ingredients

    @property
    def ingredients(self):
        Buns = [f"{bun.name}: {bun.amount}" for bun in self._ingredients['Bun'].values() if not isNaN(bun.amount) and bun.amount > 0]
        Patties = [f"{patty.name}: {patty.amount}" for patty in self._ingredients['Patty'].values() if not isNaN(patty.amount) and patty.amount > 0]
        Others = [f"{other.name}: {other.amount}" for other in self._ingredients['Other'].values() if not isNaN(other.amount) and other.amount > 0]
        return (f"Ingredients: \n\t- Buns: {Buns} \n\t- Patties: {Patties} \n\t- Others: {Others}")

    def __str__(self):
        Buns = [f"{bun.name}: {bun.amount}" for bun in self._ingredients['Bun'].values() if not isNaN(bun.amount) and bun.amount > 0]
        Patties = [f"{patty.name}: {patty.amount}" for patty in self._ingredients['Patty'].values() if not isNaN(patty.amount) and patty.amount > 0]
        Others = [f"{other.name}: {other.amount}" for other in self._ingredients['Other'].values() if not isNaN(other.amount) and other.amount > 0]
        return (f"{self._type}: {self._name} \nIngredients: \n\t- Buns: {Buns} \n\t- Patties: {Patties} \n\t- Others: {Others} \nNet Price: ${self.price:.2f} \nDescription: {self._description}")

class Wrap(Main):

    def __init__(self, name: str = 'Classic Wrap', price: float = 0, description: str = 'N/A', availability: bool = True):
        super().__init__(name, price, description, availability)
        # dict<Ingredient>
        self._ingredients = {
            'Wrap':      {},
            'Patty':    {},
            'Other':    {}  # and other ingredients
        }
        # dict<int>
        self._max_limit = {
            'Wrap':      1000,
            'Patty':    1000
            # and other ingredients
        }
    def make_default_wrap(self,invent: Inventory):
        self.add_ingredients(Ingredient("Wrap", additional_price=1),Ingredient("Chicken Patty",additional_price=2),Ingredient("Swiss Cheese",additional_price=0.5))
        self.modify_wraps(invent,Ingredient("Wrap", amount=1, additional_price=1))
        self.modify_patties(invent,Ingredient("Chicken Patty",amount=1,additional_price=2))
        self.modify_other_ingredients(invent,Ingredient("Swiss Cheese",amount=1,additional_price=0.5))

    @property
    def ingredientsDict(self):
        return self._ingredients

    @property
    def ingredients(self):
        Wraps = [f"{wrap.name}: {wrap.amount}" for wrap in self._ingredients['Wrap'].values() if not isNaN(wrap.amount) and wrap.amount >= 0]
        Patties = [f"{patty.name}: {patty.amount}" for patty in self._ingredients['Patty'].values() if not isNaN(patty.amount) and patty.amount >= 0]
        Others = [f"{other.name}: {other.amount}" for other in self._ingredients['Other'].values() if not isNaN(other.amount) and other.amount >= 0]
        return (f"Ingredients: \n\t- Wraps: {Wraps} \n\t- Patties: {Patties} \n\t- Others: {Others}")

    def __str__(self):
        Wraps = [f"{wrap.name}: {wrap.amount}" for wrap in self._ingredients['Wrap'].values() if not isNaN(wrap.amount) and wrap.amount >= 0]
        Patties = [f"{patty.name}: {patty.amount}" for patty in self._ingredients['Patty'].values() if not isNaN(patty.amount) and patty.amount >= 0]
        Others = [f"{other.name}: {other.amount}" for other in self._ingredients['Other'].values() if not isNaN(other.amount) and other.amount >= 0]
        return (f"{self._type}: {self._name} \nIngredients: \n\t- Wraps: {Wraps} \n\t- Patties: {Patties} \n\t- Others: {Others} \nNet Price: ${self.price:.2f} \nDescription: {self._description}")


class Side(Item):

    def __init__(self, name: str, price: float, description='N/A', availability=True):
        super().__init__(name, price, "Sides", description, availability)


class Drink(Item):

    def __init__(self, name: str, price: float, description='N/A', availability=True):
        super().__init__(name, price, "Drinks", description, availability)

class Sundae(Item):

    def __init__(self, name: str, price: float, description='N/A', availability=True):
        super().__init__(name, price, "Sundaes", description, availability)


if __name__ == "__main__":
    invent = Inventory()
    invent.add_new_ingredients(
        Ingredient("Veg Bun", amount=10)
    )
    big_mac = Burger("Big Mac")
    big_mac.add_ingredients(
        "Bun",
        Ingredient("Veg Bun", additional_price=1)
    )
    # big_mac.set_ingredient_limit("Veg Bun", 0)
    big_mac.modify_buns(
        invent,
        Ingredient("Veg Bun", amount=1, additional_price=1)
    )
    print(big_mac)