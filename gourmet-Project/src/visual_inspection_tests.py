from order_system import *
from inventory import *
from system_creator import *
import pickle

def setup():
    '''
    system initializer
    '''
    system = create_save_system(
        mains=create_mains_menu("../docs/Menus.csv"),
        sides=create_sides_menu("../docs/Menus.csv"),
        drinks=create_drinks_menu("../docs/Menus.csv"),
        inventory=create_inventory("../docs/Inventory.csv"),
        staff_system=create_staffsystem("../docs/StaffSystem.csv")
    )
    
    return system

def test_mains():
    s = setup()
    # create a new order
    order = Order(order_id=1)
    # add burger into the order
    order.add_items(s.get_item("Burger"))

    # modify the buns of the burger
    order.items["Burger"][0].modify_buns(
        s.inventory,
        Ingredient(name="Sesame Bun", amount=1, additional_price=1),
        Ingredient(name="Muffin Bun", amount=1, additional_price=1)
    )
    # modify the patties of the burger
    order.items["Burger"][0].modify_patties(
        s.inventory,
        Ingredient(name="Chicken Patty", amount=2, additional_price=3),
        Ingredient(name="Vegetarian Patty", amount=1, additional_price=2)
    )
    # modify other ingredients of the burger
    order.items["Burger"][0].modify_other_ingredients(
        s.inventory,
        Ingredient(name="Tomato", amount=1, additional_price=0.5),
        Ingredient(name="Lettuce", amount=0, additional_price=0.3)
    )

    # review this burger
    order.items['Burger'][0].review()

### Should not call this because this will allow customer to create infinite order
def test_mains_no_checkout():

    try:
        with open('system_data.dat','rb') as f:
            system = pickle.load(f)
    except FileNotFoundError:
        print("File not found creating new system")
        system = setup()
    orderID = system.make_order()
    print(orderID)
    system.add_items_in_orders(
        orderID, 
        system.get_item("Burger"), 
        system.get_item("Wrap"),
        system.get_item("Coke Can"),
        system.get_item("Coke Can"),
        system.get_item("Nugget 6 pack"),
        system.get_item("Nugget 6 pack")
    )
    
    # buns
    sesame_bun = Ingredient(name="Sesame Bun", amount=2, additional_price=1)
    muffin_bun = Ingredient(name="Muffin Bun", amount=1, additional_price=1)
    # patties
    chicken_patty = Ingredient(name="Chicken Patty", amount=3, additional_price=3)
    vegetarian_patty = Ingredient(name="Vegetarian Patty",amount=1, additional_price=2)
    # other
    tomato = Ingredient(name="Tomato", amount=2, additional_price=0.5)
    lettuce = Ingredient(name="Lettuce", amount=3, additional_price=0.2)

    '''
    Modify burger
    '''

    system._get_pendingorder(orderID).items["Burger"][0].modify_buns(
        system.inventory,
        sesame_bun,
        muffin_bun
    )
    system._get_pendingorder(orderID).items["Burger"][0].modify_patties(
        system.inventory,
        chicken_patty,
        vegetarian_patty
    )
    system._get_pendingorder(orderID).items["Burger"][0].modify_other_ingredients(
        system.inventory,
        tomato,
        lettuce
    )

    '''
    Modify Wrap
    '''

    system._get_pendingorder(orderID).items["Wrap"][0].modify_wraps(
        system.inventory,
        
    )

    system._get_pendingorder(orderID).calculate_price()
    system.display_order(orderID)
    system.checkout(orderID)

    print(f"Amount of Sesame Bun left {system.inventory.get_ingredient('Sesame Bun').amount}")
    print("Amount of Lettuce left {}".format(system.inventory.get_ingredient('Lettuce').amount))
    print("Amount of Nugget left {}".format(system.inventory.get_ingredient('Nugget').amount))
    print("Amount of Tomato left {}".format(system.inventory.get_ingredient('Tomato').amount))
    print("Amount of Cheddar Cheese left {}".format(system.inventory.get_ingredient('Cheddar Cheese').amount))

    print("~~~~~~~~~~~~~~~~~~Showing Mains Menu~~~~~~~~~~~~~~~~")
    system.display_menu("Mains")
    print(system.get_item("Burger"))
    print(system.get_item("Wrap"))
    print("Pickling system")
    with open('system_data.dat','wb') as f:
        pickle.dump(system,f,pickle.HIGHEST_PROTOCOL)


def test_persistance():
    try:
        with open('system_data.dat','rb') as f:
            system = pickle.load(f)
    except FileNotFoundError:
        print("File not Found")
        assert(False)
    for i in range(1,system.total_order+1):
        system.display_order(i)

def test_mains_checkout():
    try:
        with open('system_data.dat','rb') as f:
            system = pickle.load(f)
    except FileNotFoundError:
        print("File not found creating new system")
        system = setup()

    orderID = system.make_order()
    print(orderID)
    system.add_items_in_orders(
        orderID, 
        system.get_item("Burger"), 
        system.get_item("Wrap"),
        system.get_item("Coke Can"),
        system.get_item("Coke Can"),
        system.get_item("Nugget 6 pack"),
        system.get_item("Nugget 6 pack")
    )
    
    # buns
    sesame_bun = Ingredient(name="Sesame Bun", amount=2, additional_price=1)
    muffin_bun = Ingredient(name="Muffin Bun", amount=1, additional_price=1)
    # patties
    chicken_patty = Ingredient(name="Chicken Patty", amount=3, additional_price=3)
    vegetarian_patty = Ingredient(name="Vegetarian Patty",amount=1, additional_price=2)
    # other
    tomato = Ingredient(name="Tomato", amount=2, additional_price=0.5)
    lettuce = Ingredient(name="Lettuce", amount=3, additional_price=0.2)

    '''
    Modify burger
    '''

    system._get_pendingorder(orderID).items["Burger"][0].modify_buns(
        system.inventory,
        sesame_bun,
        muffin_bun
    )
    system._get_pendingorder(orderID).items["Burger"][0].modify_patties(
        system.inventory,
        chicken_patty,
        vegetarian_patty
    )
    system._get_pendingorder(orderID).items["Burger"][0].modify_other_ingredients(
        system.inventory,
        tomato,
        lettuce
    )

    '''
    Modify Wrap
    '''

    system._get_pendingorder(orderID).items["Wrap"][0].modify_wraps(
        system.inventory,
        
    )

    system._get_pendingorder(orderID).calculate_price()
    system.display_order(orderID)
    print(f"Checking out Order {orderID}")
    system.checkout(orderID)
    print(f"Amount of Sesame Bun left {system.inventory.get_ingredient('Sesame Bun').amount}")
    print(f"Amount of Muffin Bun left {system.inventory.get_ingredient('Muffin Bun').amount}")
    print("Amount of Lettuce left {}".format(system.inventory.get_ingredient('Lettuce').amount))
    print("Amount of Nugget left {}".format(system.inventory.get_ingredient('Nugget').amount))
    print("Amount of Tomato left {}".format(system.inventory.get_ingredient('Tomato').amount))
    print("Amount of Chicken Patty left {}".format(system.inventory.get_ingredient('Chicken Patty').amount))
    
    with open('system_data.dat','wb') as f:
        pickle.dump(system,f,pickle.HIGHEST_PROTOCOL)
    #TODO: before first run $ rm system_data.dat
    # Unpickle the system_data.dat here
    # Checkout order_id 1
    # inspect if the inventory is being decremented correctly
    # 1st run seems ok? Modify the fucntion so that it checkout everyorder in the pending_order list
    # inspect that everyorder is in completed_order list
    # may be do some testings on your staff class here too.
   # pass

def test_staff_mark_order():
    try:
        with open('system_data.dat','rb') as f:
            system = pickle.load(f)
    except FileNotFoundError:
        print("File not Found")
        assert(False)
    system.update_order(1,'Gaurang','1234')
    system.display_order_lists()
    system.display_order(2)
    system.update_order(2,'Gaurang','1234')
    system.update_order(3,'Gaurang','1234')
    system.update_order(4,'Gaurang','1234')

    system.display_order_lists()
    system.display_order(3)
    with open('system_data.dat','wb') as f:
        pickle.dump(system,f,pickle.HIGHEST_PROTOCOL)   

def test_money():

    setup = create_system(
        mains=create_mains_menu("../docs/Menus.csv"),
        sides=create_sides_menu("../docs/Menus.csv"),
        drinks=create_drinks_menu("../docs/Menus.csv"),
        inventory=create_inventory("../docs/Inventory.csv"),
        staff_system=create_staffsystem("../docs/StaffSystem.csv")
    )
    setup.make_order()
    #Creating Ingredients
    sesame_bun = Ingredient(name="Sesame Bun", amount=1, additional_price=1)
    muffin_bun = Ingredient(name="Muffin Bun", amount=1, additional_price=1)
    wrap = Ingredient(name = "Wrap", amount= 1, additional_price=1)
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
    setup.add_items_in_orders(1,setup.get_item("Burger"),setup.get_item("Wrap"))
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
    setup.display_order(1)

if __name__ == "__main__":
    # test_mains_checkout()   #create & checkout order 1
    # test_mains_checkout()   #create & checkout order 2
    # test_mains_checkout()   #create & checkout order 3
    # test_mains_checkout()   #create & checkout order 4
    # test_staff_mark_order() #mark order 1 as completed
    test_money()
