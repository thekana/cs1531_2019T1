from src.menu import *
from src.item import *
from src.ingredient import *
from src.inventory import *
from src.order_system import *
from src.staff_system import *
import csv
import pickle

'''
This is a helper function,
which will read data from a file and output a system with correct menus and inventory.
'''

BURGER_BASE_PRICE = 8
WRAP_BASE_PRICE = 8
MAX_BUNS = 4
MAX_PATTIES = 3


def create_staffsystem(file_address: str) -> StaffSystem:
    staffsystem = StaffSystem()

    with open(file_address) as f:
        reader = csv.DictReader(f)
        for row in reader:
            staffsystem.add_staff(
                username=row["Username"],
                password=row["Password"]
            )
    return staffsystem


def create_inventory(file_address: str) -> Inventory:
    inventory = Inventory()

    with open(file_address) as f:
        reader = csv.DictReader(f)
        for row in reader:
            inventory.add_new_ingredients(
                Ingredient(
                    name=row["Ingredient Name"],
                    amount=float(row['Stock Amount']),
                    unit=row["Stock Unit"],
                    additional_price=float(row["Additional Price"] if row["Additional Price"] else 0),
                    min_selling= float(row["Min Selling"]),
                    multiplier = float(row["Multiplier"])
                )
            )

    return inventory


def create_mains_menu(file_address: str) -> Menu:

    mains_menu = Menu("Mains")

    with open(file_address, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Type"] != "Main":
                continue
            elif row["Item Name"] == "Burger":
                burger = Burger(row["Item Name"], float(row["Price"]))
                ingredients = row["Ingredients"].split(' | ')
                for ingredient in ingredients:
                    burger.add_ingredients(Ingredient(ingredient))
            elif row["Item Name"] == "Wrap":
                wrap = Wrap(row["Item Name"], float(row["Price"]))
                ingredients = row["Ingredients"].split(' | ')
                for ingredient in ingredients:
                    wrap.add_ingredients(Ingredient(ingredient))

    burger.set_ingredient_limit(ingredient_name="Bun", amount=MAX_BUNS)
    burger.set_ingredient_limit(ingredient_name="Patty", amount=MAX_PATTIES)

    mains_menu.add_items(burger, wrap)

    return mains_menu


def create_sides_menu(file_address: str) -> Menu:
    sides_menu = Menu("Sides")

    with open(file_address, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Type"] != "Side":
                continue
            side = Side(row["Item Name"], float(row["Price"]))
            ingredients = row["Ingredients"].split(' | ')
            for ingredient in ingredients:
                ingredient = ingredient.split(":")
                side.add_ingredients(Ingredient(
                    ingredient[0], float(ingredient[1])))
            sides_menu.add_items(side)

    return sides_menu


def create_drinks_menu(file_address: str) -> Menu:
    drinks_menu = Menu("Drinks")

    with open(file_address, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Type"] != "Drink":
                continue
            drink = Drink(row["Item Name"], float(row["Price"]))
            ingredients = row["Ingredients"].split(' | ')
            for ingredient in ingredients:
                ingredient = ingredient.split(":")
                drink.add_ingredients(Ingredient(
                    ingredient[0], float(ingredient[1])))
            drinks_menu.add_items(drink)

    return drinks_menu

def create_sundaes_menu(file_address: str) -> Menu:
    sundaes_menu = Menu("Sundaes")

    with open(file_address, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Type"] != "Sundae":
                continue
            sundae = Sundae(row["Item Name"], float(row["Price"]))
            ingredients = row["Ingredients"].split(' | ')
            for ingredient in ingredients:
                ingredient = ingredient.split(":")
                sundae.add_ingredients(Ingredient(
                    ingredient[0], float(ingredient[1])))
            sundaes_menu.add_items(sundae)

    return sundaes_menu

### Creating system with pickling
def create_save_system(mains: Menu, sides: Menu, drinks: Menu, sundaes: Menu, inventory: Inventory, staff_system: StaffSystem) -> OrderSystem:
    system = OrderSystem(
        Menus={"Mains": mains,
               "Sides": sides,
               "Drinks": drinks,
               "Sundaes": sundaes},
        Inventory=inventory,
        Staff_system=staff_system
    )

    with open('system_data.dat', 'wb') as f:
        pickle.dump(system, f, pickle.HIGHEST_PROTOCOL)

    return system

### Creating system without pickling
def create_system(mains: Menu, sides: Menu, drinks: Menu, sundaes: Menu, inventory: Inventory, staff_system: StaffSystem) -> OrderSystem:
    system = OrderSystem(
        Menus={"Mains": mains,
               "Sides": sides,
               "Drinks": drinks,
               "Sundaes": sundaes},
        Inventory=inventory,
        Staff_system=staff_system
    )
    return system

if __name__ == "__main__":

    system = create_save_system(
        mains=create_mains_menu("docs/Menus.csv"),
        sides=create_sides_menu("docs/Menus.csv"),
        drinks=create_drinks_menu("docs/Menus.csv"),
        sundaes=create_sundaes_menu("docs/Menus.csv"),
        inventory=create_inventory("docs/Inventory.csv"),
        staff_system=create_staffsystem("docs/StaffSystem.csv")
    )