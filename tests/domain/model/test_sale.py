from app.domain.model.client import Client
from app.domain.model.employee import Employee
from app.domain.model.product import Product
from app.domain.model.sale import Sale
from tests import BaseTestCase


class TestSale(BaseTestCase):

    DROP_MONGO = True

    def setUp(self) -> None:
        super().setUp()
        employee_collection = Employee.get_collection()
        employee = Employee.from_dict({
            'name': 'Foo',
            'birth_date': '1997-07-21T12:24:21-03:00',
            'position': Employee.Position.CASHIER.name,
            'cpf': '164.072.910-03',
        })
        self.employee_id = employee_collection.insert_one(employee.to_dict()).inserted_id

        product_collection = Product.get_collection()
        product = Product.from_dict({
            'name': 'Foo',
            'available_quantity': 5,
            'price': 12.25,
        })
        self.product_id = product_collection.insert_one(product.to_dict()).inserted_id

        client_collection = Client.get_collection()
        client = Client.from_dict({
            'name': 'Foo',
            'cpf': '859.778.450-49',
            'registered_by_employee_id': self.employee_id,
        })
        self.client_id = client_collection.insert_one(client.to_dict()).inserted_id

    def test_validation(self):
        product_collection = Product.get_collection()
        sale = Sale.from_dict({
            'products': product_collection.find({'_id': self.product_id}),
            'cashier_id': self.employee_id,
            'client_id': self.client_id,
            'total_value': 12.25,
        })

        self.assertEqual([], list(sale.errors))
