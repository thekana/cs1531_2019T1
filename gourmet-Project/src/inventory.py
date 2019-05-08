from src.ingredient import Ingredient
'''
Inventory: a class used to store inventory.
'''
### add minimum amount to sell

class Inventory(object):

    def __init__(self):
        self._ingredients = {}      # dict<Ingredient>

    # add new ingredients to the inventory
    # ingredients to be created first (aggregation relationship)
    def add_new_ingredients(self, *argv: Ingredient):
        for ingredient in argv:
            self._ingredients[ingredient.name] = ingredient

    # add or substract amount of an ingredient
    def update_stock(self, ingredient_name: str, amount: float):
        self._ingredients[ingredient_name].change(amount)

    # check an ingredient whether available (with an amount)
    def is_available(self, ingredient_name: str, amount: float =None):
        available_amount = self._ingredients[ingredient_name].amount/self._ingredients[ingredient_name].multiplier
        if amount or (amount == 0):
            return True if available_amount >= amount else False
        else:
            return self._ingredients[ingredient_name].is_soldout

    # display all the unavailable ingredients in the inventory
    def display_unavailable_ingredients(self):
        unavailable_ingredients = []
        for ingredient in self._ingredients.values():
            if ingredient.is_soldout:
                unavailable_ingredients.append(ingredient.name)
            elif not self.is_available(ingredient.name, ingredient.minimum):
                unavailable_ingredients.append(ingredient.name)
        return unavailable_ingredients
    
    # get ingredient details
    def get_ingredient(self, name: str) -> Ingredient:
        return self._ingredients[name]

    def get_ingredients(self):
        return [ingredient for ingredient in self._ingredients.values()] 

    def __str__(self):
        l = [f"{ingredient.name}: {ingredient.amount}" for ingredient in self._ingredients.values()]
        return str(l)

if __name__ == "__main__":
    butter = Ingredient("butter")
    tomato = Ingredient("tomato", 10)
    inventory = Inventory()

    inventory.add_new_ingredients(butter, tomato)
    print(inventory._ingredients)
