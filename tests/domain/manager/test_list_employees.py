from app.domain.model.employee import Employee
from app.domain.manager.list_employees import ListEmployees
from tests import BaseTestCase


class TestListEmployees(BaseTestCase):

    DROP_MONGO = True

    def setUp(self) -> None:
        super().setUp()
        employee_collection = Employee.get_collection()
        self.employee_id = employee_collection.insert_one(Employee.from_dict({
            'name': '<1-employee>',
            'birth_date': '1990-01-01',
            'position': Employee.Position.MANAGER.name,
            'is_active': True,
            'cpf': '85932234008',
        }).to_dict()).inserted_id

        self.second_employee_id = employee_collection.insert_one(Employee.from_dict({
            'name': '<2-employee>',
            'birth_date': '1995-06-06',
            'position': Employee.Position.SALESMAN.name,
            'is_active': False,
            'cpf': '32985688051',
        }).to_dict()).inserted_id

    def test_list_first_page(self):
        employees = ListEmployees(page=1, limit=1).execute()
        employee_ids = list(map(lambda x: x['_id'], employees))

        self.assertEqual(1, len(employee_ids))
        self.assertEqual(self.employee_id, employee_ids[0])

    def test_list_second_page(self):
        employees = ListEmployees(page=2, limit=1).execute()
        employee_ids = list(map(lambda x: x['_id'], employees))

        self.assertEqual(1, len(employee_ids))
        self.assertEqual(self.second_employee_id, employee_ids[0])

    def test_filter(self):
        employees = ListEmployees(page=1, limit=1, filters={'position': 'SALESMAN'}).execute()
        employee_ids = list(map(lambda x: x['_id'], employees))

        self.assertEqual(1, len(employee_ids))
        self.assertEqual(self.second_employee_id, employee_ids[0])
