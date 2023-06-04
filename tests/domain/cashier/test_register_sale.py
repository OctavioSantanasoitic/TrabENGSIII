from app.domain.cashier.register_sale import RegisterSale
from app.domain.model.employee import Employee
from app.domain.model.product import Product
from app.domain.model.sale import Sale
from tests import BaseTestCase


class TestRegisterSale(BaseTestCase):

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
            'name': '<product-1>',
            'available_quantity': 312,
            'color': 'blue',
            'sizes': '46',
            'price': 149.9,
        }).to_dict()).inserted_id

    def test_register_sale_once_product(self):
        product_ids = [self.product_id]
        RegisterSale(cashier_id=self.employee_id, product_ids=product_ids).execute()

        first_sale = Sale.from_dict(Sale.get_collection().find_one())
        self.assertEqual(149.9, first_sale.total_value)
        self.assertEqual(self.employee_id, first_sale.cashier_id)

    def test_register_sale_two_equals_product(self):
        product_ids = [self.product_id, self.product_id]
        RegisterSale(cashier_id=self.employee_id, product_ids=product_ids).execute()

        first_sale = Sale.from_dict(Sale.get_collection().find_one())
        self.assertEqual(299.8, first_sale.total_value)
        self.assertEqual(self.employee_id, first_sale.cashier_id)
