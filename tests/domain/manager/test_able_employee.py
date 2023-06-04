from app.domain.manager.able_employee import AbleEmployee
from app.domain.model.employee import Employee
from tests import BaseTestCase


class TestAbleEmployee(BaseTestCase):

    DROP_MONGO = True

    def setUp(self) -> None:
        super().setUp()
        employee_collection = Employee.get_collection()
        employee = Employee.from_dict({
            'name': 'Foo',
            'birth_date': '1997-07-21T12:24:21-03:00',
            'position': Employee.Position.CASHIER.value,
            'cpf': '164.072.910-03',
        })
        result = employee_collection.insert_one(employee.to_dict())
        self.employee_id = result.inserted_id

    def test_able_not_found_employee(self):
        with self.assertRaises(ValueError) as exception:
            AbleEmployee('647cdc0b920c2f87e8d1a89c').execute()

        self.assertEqual(
            'Without employee with id 647cdc0b920c2f87e8d1a89c',
            exception.exception.args[0],
        )

    def test_able(self):
        AbleEmployee(self.employee_id).execute()

        employee_dict = Employee.get_collection().find_one({'_id': self.employee_id})
        employee = Employee.from_dict(employee_dict)

        self.assertTrue(employee.is_active)
