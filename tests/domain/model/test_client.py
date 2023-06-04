from app.domain.model.client import Client
from app.domain.model.employee import Employee
from tests import BaseTestCase


class TestClient(BaseTestCase):

    DROP_MONGO = True

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

    def test_valid_client(self):
        client = Client.from_dict({
            'name': 'Foo',
            'cpf': '859.778.450-49',
            'registered_by_employee_id': self.employee_id,
        })

        self.assertEqual([], list(client.errors))
