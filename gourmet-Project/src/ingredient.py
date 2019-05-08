'''
Ingredient: a class used to store ingredients.
'''

# a function used to check whether a float variable is Nan
def isNaN(num):
    return num != num

class Ingredient(object):

    def __init__(self, name: str, amount: float =float('nan'), unit: str ='', additional_price: float =0, min_selling = 1, multiplier=1):
        self._name = name
        self._amount = amount
        self._unit = unit
        self._additional_price = additional_price
        self._min_selling = min_selling
        self.__is_soldout()
        self._multiplier = multiplier

    # check whether it is sold_out
    def __is_soldout(self):
        if self._amount >= self._min_selling:
             self._is_soldout = False
        else:
             self._is_soldout = True

    # this function call is for updating inventory stock
    def change(self, amount: float):
        self._amount += amount * float(self._multiplier)
        self.__is_soldout()

    # reset its amount
    def reset(self, amount: float):
        self._amount = amount
        self.__is_soldout()

    '''
    Property
    '''
    @property
    def name(self):
        return self._name

    @property
    def amount(self):
        return self._amount

    @property
    def is_soldout(self):
        return self._is_soldout

    @property
    def additional_price(self):
        return self._additional_price
    
    @property 
    def minimum(self):
        return self._min_selling

    @property 
    def multiplier(self):
        return self._multiplier
    
    @property
    def unit(self):
        return self._unit
    '''
    str
    '''
    def __str__(self):
        if (self._amount != self.amount) and (self._unit == ''):
            return f"{self._name}"
        else:
            return f"{self._name}: {self._amount} {self._unit}"


if __name__ == "__main__":
    butter = Ingredient("butter")
    tomato = Ingredient("tomato", 10, "gram(s)")

    print(butter.name, butter.amount, butter.is_soldout)
    print(butter)

    print(tomato)
    tomato.change(-5)
    print(tomato)
    tomato.reset(10)
    print(tomato)