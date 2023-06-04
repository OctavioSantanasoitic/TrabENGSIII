from app.domain.employee.create_client import CreateClient
from app.domain.model.client import Client
from app.domain.model.employee import Employee
from tests import BaseTestCase


class TestCreateClient(BaseTestCase):

    DROP_MONGO = True

    PAYLOAD = {
        'name': '<client-name>',
    }

    def setUp(self) -> None:
        super().setUp()
        employee_collection = Employee.get_collection()
        employee = Employee.from_dict({
            'name': 'Foo',
            'birth_date': '1997-07-21T12:24:21-03:00',
            'position': Employee.Position.SALESMAN.value,
            'cpf': '164.072.910-03',
        })
        result = employee_collection.insert_one(employee.to_dict())
        self.employee_id = result.inserted_id

    def test_create_success(self):
        cpf = '30169492028'
        CreateClient({
            **self.PAYLOAD,
            'cpf': cpf,
            'registered_by_employee_id': self.employee_id,
        }).execute()

        client_dict = Client.get_collection().find_one({'cpf': cpf})
        client = Client.from_dict(client_dict)
        self.assertEqual('<client-name>', client.name)

    def test_having_validation_error(self):
        cpf = '90301513074'
        with self.assertRaises(ValueError) as exception:
            CreateClient(self.PAYLOAD | {'cpf': cpf}).execute()

        self.assertEqual(
            'Client data have errors: \n\tEmployee id is required',
            exception.exception.args[0],
        )

    def test_create_duplicated(self):
        first_payload = {
            **self.PAYLOAD,
            'cpf': '43242324072',
            'registered_by_employee_id': self.employee_id,
        }

        second_payload = {
            **first_payload,
            'name': '<ignored-name>',
        }

        CreateClient(first_payload).execute()

        with self.assertRaises(ValueError) as exception:
            CreateClient(second_payload).execute()

        self.assertEqual(
            'Client with cpf "43242324072" already exists',
            exception.exception.args[0],
        )
