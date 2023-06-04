from app.domain.model.employee import Employee
from tests import BaseTestCase


class TestEmployee(BaseTestCase):

    DEFAULT_ARGS = {
        'name': 'Foo',
        'birth_date': '1997-07-21T12:24:21-03:00',
        'position': Employee.Position.MANAGER.name,
        'cpf': '164.072.910-03',
    }

    def test_after_fill(self):
        employee = Employee.from_dict({
            **TestEmployee.DEFAULT_ARGS,
            'is_active': True,
        })

        self.assertTrue(employee.is_active)
        self.assertEqual('16407291003', employee.cpf)

    def test_after_fill_not_active(self):
        employee = Employee.from_dict(TestEmployee.DEFAULT_ARGS)

        self.assertFalse(employee.is_active)
        self.assertEqual('16407291003', employee.cpf)

    def test_enable_from_disable(self):
        employee = Employee.from_dict(TestEmployee.DEFAULT_ARGS)

        employee.enable()

        self.assertTrue(employee.is_active)

    def test_enable_from_already_enabled(self):
        employee = Employee.from_dict({
            **TestEmployee.DEFAULT_ARGS,
            'is_active': True,
        })

        with self.assertRaises(ValueError) as exception:
            employee.enable()

        self.assertEqual(
            'You cannot enable an already active employee',
            exception.exception.args[0],
        )

    def test_disable_from_enabled(self):
        employee = Employee.from_dict({
            **TestEmployee.DEFAULT_ARGS,
            'is_active': True,
        })

        employee.disable()

        self.assertFalse(employee.is_active)

    def test_disable_from_already_disabled(self):
        employee = Employee.from_dict(TestEmployee.DEFAULT_ARGS)

        with self.assertRaises(ValueError) as exception:
            employee.disable()

        self.assertEqual(
            'You cannot disabled an already not active employee',
            exception.exception.args[0],
        )

    def test_errors(self):
        employee = Employee.from_dict(TestEmployee.DEFAULT_ARGS)

        self.assertEqual([], list(employee.errors))
