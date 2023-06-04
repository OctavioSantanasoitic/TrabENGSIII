from app.domain.model.product import Product
from tests import BaseTestCase


class TestProduct(BaseTestCase):

    def test_valid_product(self):
        product = Product.from_dict({
            'name': 'Foo',
            'available_quantity': 5,
            'price': 12.25,
        })

        self.assertEqual([], list(product.errors))

    def test_join_product(self):
        product = Product.from_dict({
            '_id': 1,
            'name': '',
            'available_quantity': 5,
            'price': 12.25,
        })

        product2 = Product.from_dict({
            '_id': 1,
            'name': '',
            'available_quantity': 7,
            'price': 12.25,
        })

        product.add_product(product2)

        self.assertEqual(product._id, product2._id)
        self.assertEqual(product.available_quantity, product2.available_quantity)
        self.assertEqual(12, product2.available_quantity)

    def test_join_different_products(self):
        product = Product.from_dict({
            '_id': 1,
            'name': '',
            'available_quantity': 5,
            'price': 12.25,
        })

        product2 = Product.from_dict({
            '_id': 2,
            'name': '',
            'available_quantity': 7,
            'price': 12.25,
        })

        with self.assertRaises(ValueError) as exception:
            product.add_product(product2)

        self.assertEqual('You cannot add different products', exception.exception.args[0])
        self.assertNotEqual(product._id, product2._id)
        self.assertNotEqual(product.available_quantity, product2.available_quantity)
