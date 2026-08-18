""" 
Problem: Handling different ice cream flavors in an Ice cream store

A factory design pattern is used to centralize object creation, allowing versatility. This pattern is
used since it allows ease of adding or removing different flavors of ice cream depending on their availability (e.g
Avocados peak fruiting is during May to September)
"""
import unittest
# Base Class
class IceCream:
    def get_description(self):
        pass

    def get_price(self):
        pass

# Different Flavors
class AvocadoIceCream(IceCream):
    def get_description(self):
        return "Avocado Ice Cream"

    def get_price(self):
        return 2.50

class ChocolateIceCream(IceCream):
    def get_description(self):
        return "Chocolate Ice Cream"

    def get_price(self):
        return 2.75

class StrawberryIceCream(IceCream):
    def get_description(self):
        return "Strawberry Ice Cream"

    def get_price(self):
        return 2.60

# The Factory
class IceCreamFactory:
    def create_icecream(self, flavor):
        flavor = flavor.lower()
        
        if flavor == "avocado":
            return AvocadoIceCream()
        elif flavor == "chocolate":
            return ChocolateIceCream()
        elif flavor == "strawberry":
            return StrawberryIceCream()
        
        # If the flavor isn't found, just return nothing
        return None


# Unit testing
class TestIceCreamFactory(unittest.TestCase):
    def test_avocado(self):
        factory = IceCreamFactory()
        icecream = factory.create_icecream("avocado")
        self.assertEqual(icecream.get_description(), "Avocado Ice Cream")
        self.assertEqual(icecream.get_price(), 2.50)

    def test_chocolate(self):
        factory = IceCreamFactory()
        icecream = factory.create_icecream("chocolate")
        self.assertEqual(icecream.get_description(), "Chocolate Ice Cream")
        self.assertEqual(icecream.get_price(), 2.75)

    def test_strawberry(self):
        factory = IceCreamFactory()
        icecream = factory.create_icecream("strawberry")
        self.assertEqual(icecream.get_description(), "Strawberry Ice Cream")
        self.assertEqual(icecream.get_price(), 2.60)

# Main progam
print("="*13+"Ice Cream Store" + "="*13)

shop_factory = IceCreamFactory()

my_treat = shop_factory.create_icecream("strawberry")

print("Ordered:", my_treat.get_description())
print("Price: $", my_treat.get_price())

# Run test
print("\n" + "="*13 + "Running Unit Tests" + "="*13)
unittest.main(argv=[''], exit=False)