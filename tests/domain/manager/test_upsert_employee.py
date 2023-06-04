from app.domain.manager.upsert_employee import UpsertEmployee
from app.domain.model.employee import Employee
from tests import BaseTestCase


class TestUpsertEmployee(BaseTestCase):

    DROP_MONGO = True

    CPF = '16407291003'

    def test_not_valid(self):
        with self.assertRaises(ValueError) as exception:
            UpsertEmployee({
                'name': 'Foo',
                'birth_date': '1997-07-21T12:24:21-03:00',
                'cpf': self.CPF,
            }).execute()

        self.assertEqual(
            'Failed on fields validation "\n\tPosition is not valid"',
            exception.exception.args[0],
        )

    def test_create(self):
        data = {
            'name': 'Foo',
            'birth_date': '1997-07-21T12:24:21-03:00',
            'position': Employee.Position.CASHIER.name,
            'cpf': self.CPF,
        }
        UpsertEmployee(data).execute()

        employee_dict = Employee.get_collection().find_one({'cpf': self.CPF})
        employee = Employee.from_dict(employee_dict)

        self.assertEqual(data['cpf'], employee.cpf)
        self.assertEqual(data['name'], employee.name)
        self.assertEqual(data['position'], employee.position)
        self.assertEqual(data['birth_date'], employee.birth_date)

    def test_update(self):
        employee_collection = Employee.get_collection()
        employee = Employee.from_dict({
            'name': 'Foo',
            'birth_date': '1997-07-21T12:24:21-03:00',
            'position': Employee.Position.CASHIER.name,
            'cpf': self.CPF,
        })
        employee_id = employee_collection.insert_one(employee.to_dict()).inserted_id

        data = {
            '_id': employee_id,
            'name': 'Foo bar',
            'birth_date': '1997-07-21T12:24:21-03:00',
            'position': Employee.Position.CASHIER.name,
            'cpf': self.CPF,
        }
        UpsertEmployee(data).execute()

        employee_dict = Employee.get_collection().find_one({'cpf': self.CPF})
        employee = Employee.from_dict(employee_dict)

        self.assertEqual(employee_id, employee._id)
        self.assertEqual(data['cpf'], employee.cpf)
        self.assertEqual(data['name'], employee.name)
        self.assertEqual(data['position'], employee.position)
        self.assertEqual(data['birth_date'], employee.birth_date)

    def test_try_create_with_same_cpf(self):
        employee = Employee.from_dict({
            'name': 'Foo',
            'birth_date': '1997-07-21T12:24:21-03:00',
            'position': Employee.Position.CASHIER.name,
            'cpf': self.CPF,
        })
        Employee.get_collection().insert_one(employee.to_dict())

        data = {
            'name': 'Foo bar',
            'birth_date': '1997-07-21T12:24:21-03:00',
            'position': Employee.Position.CASHIER.name,
            'cpf': self.CPF,
        }
        with self.assertRaises(ValueError) as exception:
            UpsertEmployee(data).execute()

        self.assertEqual(
            'Employee with cpf "16407291003" already exists',
            exception.exception.args[0],
        )
