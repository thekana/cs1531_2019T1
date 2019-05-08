import csv
import pytest
from src.item import *
from src.order import *
from src.menu import *
from src.inventory import *
from src.staff_system import *
from src.system_creator import *

'''
This is a test for the Order System, which covers the Epic story 1 and 2.
'''

@pytest.fixture
def setup():
    system = create_system(
        mains=create_mains_menu("docs/Menus.csv"),
        sides=create_sides_menu("docs/Menus.csv"),
        drinks=create_drinks_menu("docs/Menus.csv"),
        sundaes=create_sundaes_menu("docs/Menus.csv"),
        inventory=create_inventory("docs/Inventory.csv"),
        staff_system=create_staffsystem("docs/StaffSystem.csv")
    )
    return system

@pytest.fixture
def setup1():
    system = create_system(
        mains=create_mains_menu("docs/Menus.csv"),
        sides=create_sides_menu("docs/Menus.csv"),
        drinks=create_drinks_menu("docs/Menus.csv"),
        sundaes=create_sundaes_menu("docs/Menus.csv"),
        inventory=create_inventory("docs/Inventory.csv"),
        staff_system=create_staffsystem("docs/StaffSystem.csv")
    )
    system.make_order()
    itemList = ["Coke Can", "Nugget - 6 pack", "Orange Juice - Small", "Fries - Medium"]
    system.add_items_in_orders(
        1,
        system.get_item(itemList[0]),
        system.get_item(itemList[1]),
        system.get_item(itemList[2]),
        system.get_item(itemList[3])
    )
    system.add_items_in_orders(1,system.get_item("Burger"),system.get_item("Wrap"))
    #Creating Ingredients
    sesame_bun = Ingredient(name="Sesame Bun", amount=1, additional_price=1)
    muffin_bun = Ingredient(name="Muffin Bun", amount=1, additional_price=1)
    wrap = Ingredient(name = "Wrap", amount= 2, additional_price=1)
    # patties
    chicken_patty = Ingredient(name="Chicken Patty", amount=1, additional_price=2)
    vegetarian_patty = Ingredient(name="Vegetarian Patty",amount=1, additional_price=2)
    beef_patty = Ingredient(name="Beef Patty",amount=1,additional_price=2)
    # other
    tomato = Ingredient(name="Tomato", amount=1, additional_price=0.2)
    lettuce = Ingredient(name="Lettuce", amount=1, additional_price=0.2)
    cheddar_cheese = Ingredient(name = "Cheddar Cheese", amount=1, additional_price= 0.5)
    swiss_cheese = Ingredient(name = "Swiss Cheese", amount = 1, additional_price= 0.5)
    sauce = Ingredient(name = "Tomato Sauce", amount= 1, additional_price=0.1)
    
    system._get_pendingorder(1).items["Wrap"][0].modify_wraps(
        system.inventory,
        wrap
    )
    system._get_pendingorder(1).items["Wrap"][0].modify_patties(
        system.inventory,
        chicken_patty,
        vegetarian_patty,
        beef_patty
    )
    system._get_pendingorder(1).items["Wrap"][0].modify_other_ingredients(
        system.inventory,
        tomato,
        lettuce,
        cheddar_cheese,
        swiss_cheese,
        sauce
    )

    system._get_pendingorder(1).items["Burger"][0].modify_buns(
        system.inventory,
        sesame_bun,
        muffin_bun
    )
    system._get_pendingorder(1).items["Burger"][0].modify_patties(
        system.inventory,
        chicken_patty,
        vegetarian_patty,
        beef_patty
    )
    system._get_pendingorder(1).items["Burger"][0].modify_other_ingredients(
        system.inventory,
        tomato,
        lettuce,
        cheddar_cheese,
        swiss_cheese,
        sauce
    )
    system._get_pendingorder(1).calculate_price()

    return system

def test_wrong_menu(setup):
    assert("Wrong name menu not exist!" == setup.display_menu("Wrong name"))


def test_wrong_item(setup):
    assert("Wrong item not in the system" == setup.get_item("Wrong item"))


def test_correct_item(setup):
    with open("docs/Menus.csv") as f:
        nameList = []
        reader = csv.DictReader(f)
        for row in reader:
            nameList.append(row["Item Name"])
    for name in nameList:
        assert(name == setup.get_item(name).name)


def test_make_order(setup):
    assert setup.total_order == 0
    setup.make_order()
    assert setup.total_order == 1


def test_add_items_to_order(setup):
    # add some drinks and sides
    # continue from above
    assert setup.total_order == 0
    setup.make_order()
    itemList = ["Coke Can", "Nugget - 6 pack", "Orange Juice - Small", "Fries - Medium"] 
    setup.add_items_in_orders(
        1,
        setup.get_item(itemList[0]),
        setup.get_item(itemList[1]),
        setup.get_item(itemList[2]),
        setup.get_item(itemList[3])
    )
    for itemName in itemList:
        assert(itemName in setup._get_pendingorder(1).items.keys())


def test_delete_items_from_order(setup):
    
    assert setup.total_order == 0
    itemList = ["Coke Can", "Nugget - 6 pack", "Orange Juice - Small", "Fries - Medium"]
    setup.make_order()
    setup.add_items_in_orders(
        1,
        setup.get_item(itemList[0]),
        setup.get_item(itemList[1]),
        setup.get_item(itemList[2]),
        setup.get_item(itemList[3])
    )
    order = setup._get_pendingorder(1)
    #order.items['Coke Can'][0].uniqueID
    setup.del_items_in_orders(1,order.items['Coke Can'][0].uniqueid)
    setup.del_items_in_orders(1,order.items['Nugget - 6 pack'][0].uniqueid)
    setup.del_items_in_orders(1,order.items['Orange Juice - Small'][0].uniqueid)
    for itemName in itemList:
        if itemName != "Fries - Medium":
            assert(itemName not in setup._get_pendingorder(1).items.keys())
        assert("Fries - Medium" in setup._get_pendingorder(1).items.keys())
    

def test_add_mains_to_order(setup):
    setup.make_order()
    assert setup.total_order == 1
    setup.add_items_in_orders(1,setup.get_item("Burger"),setup.get_item("Wrap"))
    assert "Burger" in setup._get_pendingorder(1).items.keys()
    assert "Wrap" in setup._get_pendingorder(1).items.keys()
    
def test_modify_mains(setup):
    #Make order and add mains
    setup.make_order()
    assert setup.total_order == 1
    setup.add_items_in_orders(1,setup.get_item("Burger"),setup.get_item("Wrap"))
    assert "Burger" in setup._get_pendingorder(1).items.keys()
    assert "Wrap" in setup._get_pendingorder(1).items.keys()
    #Creating Ingredients
    sesame_bun = Ingredient(name="Sesame Bun", amount=1, additional_price=1)
    muffin_bun = Ingredient(name="Muffin Bun", amount=1, additional_price=1)
    wrap = Ingredient(name = "Wrap", amount= 2, additional_price=1)
    # patties
    chicken_patty = Ingredient(name="Chicken Patty", amount=1, additional_price=2)
    vegetarian_patty = Ingredient(name="Vegetarian Patty",amount=1, additional_price=2)
    beef_patty = Ingredient(name="Beef Patty",amount=1,additional_price=2)
    # other
    tomato = Ingredient(name="Tomato", amount=1, additional_price=0.2)
    lettuce = Ingredient(name="Lettuce", amount=1, additional_price=0.2)
    cheddar_cheese = Ingredient(name = "Cheddar Cheese", amount=1, additional_price= 0.5)
    swiss_cheese = Ingredient(name = "Swiss Cheese", amount = 1, additional_price= 0.5)
    sauce = Ingredient(name = "Tomato Sauce", amount= 1, additional_price=0.1)

    IngListBurger = [sesame_bun,muffin_bun,chicken_patty,vegetarian_patty,beef_patty,
                tomato,lettuce,cheddar_cheese,swiss_cheese,sauce]
    IngListWrap = [wrap,chicken_patty,vegetarian_patty,beef_patty,
                tomato,lettuce,cheddar_cheese,swiss_cheese,sauce]

    setup._get_pendingorder(1).items["Burger"][0].modify_buns(
        setup.inventory,
        sesame_bun,
        muffin_bun
    )
    setup._get_pendingorder(1).items["Burger"][0].modify_patties(
        setup.inventory,
        chicken_patty,
        vegetarian_patty,
        beef_patty
    )
    setup._get_pendingorder(1).items["Burger"][0].modify_other_ingredients(
        setup.inventory,
        tomato,
        lettuce,
        cheddar_cheese,
        swiss_cheese,
        sauce
    )
    setup._get_pendingorder(1).calculate_price()
    assert setup._get_pendingorder(1).price == 25.5
    setup._get_pendingorder(1).items["Wrap"][0].modify_wraps(
        setup.inventory,
        wrap
    )
    setup._get_pendingorder(1).items["Wrap"][0].modify_patties(
        setup.inventory,
        chicken_patty,
        vegetarian_patty,
        beef_patty
    )
    setup._get_pendingorder(1).items["Wrap"][0].modify_other_ingredients(
        setup.inventory,
        tomato,
        lettuce,
        cheddar_cheese,
        swiss_cheese,
        sauce
    ) 
    setup._get_pendingorder(1).calculate_price()
    assert setup._get_pendingorder(1).price == 35
    
    for things in setup._get_pendingorder(1).items["Wrap"][0]._ingredients.values():
        for stuff in IngListWrap:
            if stuff.name in things.keys():
                assert stuff.amount == things[stuff.name].amount and stuff.additional_price == things[stuff.name].additional_price

    for things in setup._get_pendingorder(1).items["Burger"][0]._ingredients.values():
        for stuff in IngListBurger:
            if stuff.name in things.keys():
                assert stuff.amount == things[stuff.name].amount and stuff.additional_price == things[stuff.name].additional_price


def test_add_sundae(setup):
    setup.make_order()
    setup.add_items_in_orders(1,setup.get_item('Strawberry Sundae - Medium'),setup.get_item('Chocolate Sundae - Medium'))
    assert "Strawberry Sundae - Medium" in setup._get_pendingorder(1).items.keys()
    assert "Chocolate Sundae - Medium" in setup._get_pendingorder(1).items.keys()
    assert "Chocolate Sundae - Small" not in setup._get_pendingorder(1).items.keys()

def test_add_default_mains(setup):

    setup.make_order()
    setup.add_default_main(1,setup.get_item("Burger"))
    assert "Big Mac" in setup._get_pendingorder(1).items.keys()
    setup.add_default_main(1,setup.get_item("Wrap"))
    assert "Classic Wrap" in setup._get_pendingorder(1).items.keys()

def test_2_more_mains_to_order(setup):
    setup.make_order()
    assert setup.total_order == 1
    setup.add_items_in_orders(1,setup.get_item("Burger"),setup.get_item("Wrap"))
    assert "Burger" in setup._get_pendingorder(1).items.keys()
    assert "Wrap" in setup._get_pendingorder(1).items.keys()
    setup.add_items_in_orders(1,setup.get_item("Burger"),setup.get_item("Wrap"))
    assert len(setup._get_pendingorder(1).items['Burger']) == 2
    assert len(setup._get_pendingorder(1).items['Wrap']) == 2


def test_adding_ingredients_more_than_max_limit(setup):
    #Create order and add mains
    setup.make_order()
    assert setup.total_order == 1
    setup.add_items_in_orders(1,setup.get_item("Burger"))
    assert "Burger" in setup._get_pendingorder(1).items.keys()
    #Creating Ingredients
    sesame_bun = Ingredient(name="Sesame Bun", amount=2, additional_price=1)
    muffin_bun = Ingredient(name="Muffin Bun", amount=2, additional_price=1)
    # patties
    chicken_patty = Ingredient(name="Chicken Patty", amount=2, additional_price=2)
    vegetarian_patty = Ingredient(name="Vegetarian Patty",amount=1, additional_price=2)
    beef_patty = Ingredient(name="Beef Patty",amount=1,additional_price=2)
    # other
    tomato = Ingredient(name="Tomato", amount=1, additional_price=0.2)
    lettuce = Ingredient(name="Lettuce", amount=1, additional_price=0.2)
    cheddar_cheese = Ingredient(name = "Cheddar Cheese", amount=1, additional_price= 0.5)
    swiss_cheese = Ingredient(name = "Swiss Cheese", amount = 1, additional_price= 0.5)
    sauce = Ingredient(name = "Tomato Sauce", amount= 1, additional_price=0.1)

    IngListBurger = [sesame_bun,muffin_bun,chicken_patty,vegetarian_patty,beef_patty,
                tomato,lettuce,cheddar_cheese,swiss_cheese,sauce]

    setup._get_pendingorder(1).items["Burger"][0].modify_buns(
        setup.inventory,
        sesame_bun,
        muffin_bun
    )
    setup._get_pendingorder(1).items["Burger"][0].modify_patties(
        setup.inventory,
        chicken_patty,
        vegetarian_patty,
        beef_patty
    )
    setup._get_pendingorder(1).items["Burger"][0].modify_other_ingredients(
        setup.inventory,
        tomato,
        lettuce,
        cheddar_cheese,
        swiss_cheese,
        sauce
    )
    print(setup._get_pendingorder(1).items["Burger"][0]._errors)
    #assert(0)
    setup._get_pendingorder(1).calculate_price()
    # Second burger should reject beef patty (amount of beef patty in burger should be nan)
    for things in setup._get_pendingorder(1).items["Burger"][0]._ingredients.values():
        for stuff in IngListBurger:
            if stuff.name in things.keys():
                if stuff.name == 'Beef Patty':
                    assert(isNaN(things[stuff.name].amount))
                else:
                    assert stuff.amount == things[stuff.name].amount and stuff.additional_price == things[stuff.name].additional_price
    assert(setup._get_pendingorder(1).price == 19.5)


def test_check_out_simple(setup):
    assert setup.total_order == 0
    itemList = ["Coke Can", "Nugget - 6 pack", "Orange Juice - Small", "Fries - Medium"]
    setup.make_order()
    setup.add_items_in_orders(
        1,
        setup.get_item(itemList[0]),
        setup.get_item(itemList[1]),
        setup.get_item(itemList[2]),
        setup.get_item(itemList[3])
    )
    assert(not setup._get_pendingorder(1).is_payed)
    setup.checkout(1)
    assert(setup._get_pendingorder(1).is_payed)
    setup.display_order(1)


def test_initial_inventory_simple(setup):
    assert(setup.inventory.get_ingredient('Lettuce').amount == 200)
    assert(setup.inventory.get_ingredient('Nugget').amount == 25)
    assert(setup.inventory.get_ingredient('Fries').amount == 300)
    assert(setup.inventory.get_ingredient('Tomato Sauce').amount == 100)
    assert(setup.inventory.get_ingredient('Swiss Cheese').amount == 100)
    assert(setup.inventory.get_ingredient('Cheddar Cheese').amount == 100)
    assert(setup.inventory.get_ingredient('Tomato').amount == 100)
    assert(setup.inventory.get_ingredient('Chicken Patty').amount == 100)
    assert(setup.inventory.get_ingredient('Vegetarian Patty').amount == 100)
    assert(setup.inventory.get_ingredient('Beef Patty').amount == 100)
    assert(setup.inventory.get_ingredient('Sesame Bun').amount == 100)
    assert(setup.inventory.get_ingredient('Muffin Bun').amount == 100)
    assert(setup.inventory.get_ingredient('Wrap').amount == 100)


def test_inventory_numbers(setup1):
    assert setup1._get_pendingorder(1).price == 48.5
    setup1.checkout(1)
    assert(setup1.inventory.get_ingredient('Coke').amount == 1125)
    assert(setup1.inventory.get_ingredient('Nugget').amount == 19)
    assert(setup1.inventory.get_ingredient('OrangeJuice').amount == 750)
    assert(setup1.inventory.get_ingredient('Ice').amount == 980)
    assert(setup1.inventory.get_ingredient('Fries').amount == 175)
    
    assert(setup1.inventory.get_ingredient('Lettuce').amount == 140)
    assert(setup1.inventory.get_ingredient('Tomato Sauce').amount == 98)
    assert(setup1.inventory.get_ingredient('Swiss Cheese').amount == 98)
    assert(setup1.inventory.get_ingredient('Cheddar Cheese').amount == 98)
    assert(setup1.inventory.get_ingredient('Tomato').amount == 98)
    assert(setup1.inventory.get_ingredient('Chicken Patty').amount == 98)
    assert(setup1.inventory.get_ingredient('Vegetarian Patty').amount == 98)
    assert(setup1.inventory.get_ingredient('Beef Patty').amount == 98)
    assert(setup1.inventory.get_ingredient('Sesame Bun').amount == 99)
    assert(setup1.inventory.get_ingredient('Muffin Bun').amount == 99)
    assert(setup1.inventory.get_ingredient('Wrap').amount == 98)


def test_staff_mark_order(setup1):
    order1 = setup1._get_pendingorder(1)
    setup1.checkout(1)
    assert(not order1.is_prepared)
    setup1.update_order(1,'Kanadech','4568')
    assert(order1.is_prepared)


def test_checkout_order_when_stock_low(setup):

    orderID = setup.make_order()
    itemList = ["Coke Can", "Nugget - 6 pack", "Orange Juice - Small", "Fries - Medium"]
    setup.add_items_in_orders(orderID,
            setup.get_item(itemList[1]),
            setup.get_item(itemList[1]),
            setup.get_item(itemList[1]),
            setup.get_item(itemList[1]),
            setup.get_item(itemList[1]),
            setup.get_item(itemList[2]),
            setup.get_item(itemList[2]),
            setup.get_item(itemList[2]),
            setup.get_item(itemList[2])
    )
    setup.checkout(orderID)
    # Numbers should remain intact as the order got rejected
    assert(setup.inventory.get_ingredient('Nugget').amount == 25)
    assert(setup.inventory.get_ingredient('OrangeJuice').amount == 1000)
    assert(setup.inventory.get_ingredient('Ice').amount == 1000)

    #Doing so will delete order number 2 from the system customer has to create a new one

    #Try making new order and reordering OrangeJuice
    orderID_next = setup.make_order()
    setup.add_items_in_orders(orderID_next,
            setup.get_item(itemList[2]),
            setup.get_item(itemList[2]),
            setup.get_item(itemList[2]),
            setup.get_item(itemList[2]),
            setup.get_item(itemList[1]),
            setup.get_item(itemList[1]),
            setup.get_item(itemList[1]),
            setup.get_item(itemList[1])
            )

    #Try adding a lot of lettuce in burger (only have 200 g lettuce adding 7 means 7x30 = 210)
    setup.add_items_in_orders(orderID_next, setup.get_item("Burger"))
    lettuce = Ingredient(name="Lettuce", amount=7, additional_price=0.2)
    swiss_cheese = Ingredient(name = "Swiss Cheese", amount = 6, additional_price= 0.5)
    setup._get_pendingorder(orderID_next).items["Burger"][0].modify_other_ingredients(
        setup.inventory,
        swiss_cheese,
        lettuce
    )
    assert setup._get_pendingorder(orderID_next).items["Burger"][0]._ingredients['Other']["Swiss Cheese"].amount == 6
    assert isNaN(setup._get_pendingorder(orderID_next).items["Burger"][0]._ingredients['Other']["Lettuce"].amount)
    setup.checkout(orderID_next)
    assert(setup.inventory.get_ingredient('OrangeJuice').amount == 0)
    assert(setup.inventory.get_ingredient('Ice').amount == 1000-80)
    assert(setup.inventory.get_ingredient('Nugget').amount == 1)


def test_inventory_unavailable(setup):
    orderID = setup.make_order()
    itemList = ["Coke Can", "Nugget - 6 pack", "Orange Juice - Small", "Fries - Medium"]
    setup.add_items_in_orders(orderID,
            setup.get_item(itemList[2]),
            setup.get_item(itemList[2]),
            setup.get_item(itemList[2]),
            setup.get_item(itemList[2]),
            setup.get_item(itemList[1]),
            setup.get_item(itemList[1]),
            setup.get_item(itemList[1]),
            setup.get_item(itemList[1])
            )
    setup.checkout(1)
    assert len(setup.inventory.display_unavailable_ingredients()) == 2
    assert "OrangeJuice" in setup.inventory.display_unavailable_ingredients()
    assert "Nugget" in setup.inventory.display_unavailable_ingredients()
    setup.display_order_lists()


def test_customer_check_status(setup1):
    #For front end we will use display_order() to show customer their order
    setup1.checkout(1)
    order1 = setup1._get_pendingorder(1)
    assert(order1.is_payed)
    assert(not order1.is_prepared)
    setup1.update_order(1,'Kanadech','4568')
    order1 = setup1._get_completedorder(1)
    assert(order1.is_payed)
    assert(order1.is_prepared)
