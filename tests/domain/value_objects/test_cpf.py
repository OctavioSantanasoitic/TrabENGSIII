from app.domain.value_objects.cpf import Cpf
from tests import BaseTestCase


class TestCpf(BaseTestCase):

    CPF_VALUE_FORMATTED = '695.241.840-79'
    CPF_VALUE_CLEAN = '69524184079'
    CPF_SEQUENCE_EQUALS = '11111111111'

    def test_parse(self):
        parsed_value = Cpf.parse(self.CPF_VALUE_FORMATTED)

        self.assertEqual(self.CPF_VALUE_CLEAN, parsed_value)

    def test_validated(self):
        is_valid = Cpf.validate(self.CPF_VALUE_FORMATTED)

        self.assertTrue(is_valid)

    def test_validated_when_has_more_digits(self):
        is_valid = Cpf.validate(self.CPF_VALUE_FORMATTED + '1')

        self.assertFalse(is_valid)

    def test_validated_when_has_less_digits(self):
        is_valid = Cpf.validate(self.CPF_VALUE_FORMATTED[:10])

        self.assertFalse(is_valid)

    def test_sequence_equals(self):
        is_valid = Cpf.validate(self.CPF_SEQUENCE_EQUALS)

        self.assertFalse(is_valid)

    def test_to_str(self):
        cpf = Cpf(self.CPF_VALUE_FORMATTED)

        self.assertEqual(self.CPF_VALUE_CLEAN, cpf.to_str())
        self.assertEqual(self.CPF_VALUE_FORMATTED, cpf.cpf_raw)

    def test_format_without_cpf(self):
        cpf = Cpf(self.CPF_SEQUENCE_EQUALS)

        self.assertIsNone(cpf.cpf)
        self.assertIsNone(cpf.format())
        self.assertEqual(self.CPF_SEQUENCE_EQUALS, cpf.cpf_raw)

    def test_format(self):
        cpf = Cpf(self.CPF_VALUE_CLEAN)

        self.assertEqual(self.CPF_VALUE_CLEAN, cpf.cpf)
        self.assertEqual(self.CPF_VALUE_CLEAN, cpf.cpf_raw)
        self.assertEqual(self.CPF_VALUE_FORMATTED, cpf.format())
