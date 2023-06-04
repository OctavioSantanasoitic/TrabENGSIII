from app.domain.model.employee import Employee
from app.domain.model.product import Product
from app.domain.stocker.register_products import RegisterProducts
from tests import BaseTestCase


class TestRegisterProducts(BaseTestCase):

    DROP_MONGO = True

    def setUp(self) -> None:
        super().setUp()
        employee_collection = Employee.get_collection()
        product_collection = Product.get_collection()
        self.employee_id = employee_collection.insert_one(Employee.from_dict({
            'name': 'Foo',
            'birth_date': '1997-07-21T12:24:21-03:00',
            'position': Employee.Position.CASHIER.value,
            'cpf': '164.072.910-03',
        }).to_dict()).inserted_id

        self.product_id = product_collection.insert_one(Product.from_dict({
            'name': '<product-old>',
            'available_quantity': 312,
            'color': 'blue',
            'sizes': '46',
            'price': 149.9,
        }).to_dict()).inserted_id

    def create_products(self):
        RegisterProducts([
            {
                'name': '<product-1>',
                'available_quantity': 1237,
                'color': 'black',
                'sizes': 'fixed',
                'price': 11.9,
            },
        ]).execute()

    def test_create(self):
        self.create_products()

        product_dict = Product.get_collection() \
            .find_one({'name': '<product-1>'})
        product = Product.from_dict(product_dict)

        self.assertEqual(1237, product.available_quantity)
        self.assertEqual('black', product.color)
        self.assertEqual('fixed', product.sizes)
        self.assertEqual(11.9, product.price)

    def test_update(self):
        self.create_products()

        product_dict = Product.get_collection() \
            .find_one({'name': '<product-1>'})
        product = Product.from_dict(product_dict)
        product.available_quantity = 2

        RegisterProducts([Product.to_dict(product)]).execute()

        result = Product.from_dict(Product.get_collection().find_one({'name': '<product-1>'}))

        self.assertEqual(1239, result.available_quantity)
        self.assertEqual('black', result.color)
        self.assertEqual('fixed', result.sizes)
        self.assertEqual(11.9, result.price)
