import pytest
from src.ingredient import Ingredient
from src.inventory import Inventory
from src.system_creator import create_inventory

'''
This is a test for inventory part, which covers the tests for the Epic story 3: Staff - Inventory Maintainence.
'''

@pytest.fixture()
def test_fixture():
    inventory = create_inventory("docs/Inventory.csv")
    return inventory

'''
Test whether we can get a valid ingredient by its name.
(US 3.1)
'''
def test_get_valid_ingredient(test_fixture):
    ingredient = test_fixture.get_ingredient("Fries")
    assert(ingredient.name == "Fries")
    assert(ingredient.amount == 300)
    assert(ingredient.is_soldout == False)
    assert(ingredient.unit == "g")

    ingredient = test_fixture.get_ingredient("Coke")
    assert(ingredient.name == "Coke")
    assert(ingredient.amount == 1500)
    assert(ingredient.is_soldout == False)
    assert(ingredient.unit == "ml")

    ingredient = test_fixture.get_ingredient("Cheddar Cheese")
    assert(ingredient.name == "Cheddar Cheese")
    assert(ingredient.amount == 100)
    assert(ingredient.is_soldout == False)
    assert(ingredient.unit == "slice")

'''
Test whether we can get an invalid ingredient. 
'''
def test_get_invalid_ingredient(test_fixture):
    try:
        test_fixture.get_ingredient("BAD NUGGET")
        assert(False)
    except KeyError:
        assert(True)

'''
Test whether we can change the number of the stock.
(US 3.2)
'''
def test_changing_stock_number(test_fixture):
    test_fixture.update_stock("Fries",100)
    assert test_fixture.get_ingredient("Fries").amount == 400
    test_fixture.update_stock("Ice",-600)
    assert test_fixture.get_ingredient("Ice").amount == 400
    test_fixture.update_stock("Lettuce",1)
    assert test_fixture.get_ingredient("Lettuce").amount == 230

'''
Test whether we check the availability of an item or ingredient.
'''
def test_availability(test_fixture):
    test_fixture.update_stock("Lettuce",-6)
    assert test_fixture.get_ingredient("Lettuce").amount == 20
    assert test_fixture.is_available("Lettuce",1) == False
    assert "Lettuce" in test_fixture.display_unavailable_ingredients()
    test_fixture.update_stock("OrangeJuice",-950)
    assert test_fixture.get_ingredient("OrangeJuice").amount == 50
    assert "OrangeJuice" and "Lettuce" in test_fixture.display_unavailable_ingredients()
    print(test_fixture.display_unavailable_ingredients())
    #assert(0)