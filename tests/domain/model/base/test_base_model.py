from unittest.mock import MagicMock

from bson import ObjectId

from app.domain.model.base.base_model import BaseModel
from tests import BaseTestCase


class TestBaseModel(BaseTestCase):

    def test_started_values(self):
        base_model = BaseModel()

        self.assertEqual('', base_model.TABLE_NAME)
        self.assertEqual([], base_model.FIELDS)
        self.assertEqual([], base_model.validation)
        self.assertEqual([], list(base_model.errors))
        self.assertEqual('', base_model.string_errors)
        self.assertIsNone(base_model.after_fill())
        self.assertTrue(base_model.is_valid)

    def test_errors(self):
        class ValidationErrors(BaseModel):
            @property
            def validation(self) -> list[tuple[bool, str]]:
                return [(True, 'Is valid'), (False, '<error>')]

        base_model = ValidationErrors()

        self.assertEqual(['<error>'], list(base_model.errors))

    def test_errors_raise_exception(self):
        class ValidationErrorsSideEffect(BaseModel):
            @property
            def validation(self) -> list[tuple[bool, str]]:
                return [(True, 'Is valid'), (False, '<error>'), (False)]

        base_model = ValidationErrorsSideEffect()

        expected = ['<error>', 'Failed on validation "cannot unpack non-iterable bool object"']
        self.assertEqual(expected, list(base_model.errors))

    def test_from_dict(self):
        class FromDictModel(BaseModel):
            FIELDS = ['a', 'b', 'd']

        base_model = FromDictModel.from_dict({
            'a': 'Foo',
            'b': 'Bar',
            'c': 'Not in fields',
        })
        base_model.after_fill = MagicMock()

        self.assertTrue(hasattr(base_model, 'a'))
        self.assertTrue(hasattr(base_model, 'b'))
        self.assertTrue(hasattr(base_model, 'c'))
        self.assertTrue(hasattr(base_model, 'd'))
        self.assertTrue(hasattr(base_model, 'created_at'))
        self.assertTrue(hasattr(base_model, 'updated_at'))

        self.assertEqual('Foo', base_model.a)
        self.assertEqual('Bar', base_model.b)
        self.assertEqual('Not in fields', base_model.c)
        self.assertIsNone(base_model.d)

    def test_from_dict_with_timestamps(self):
        class FromDictModel(BaseModel):
            FIELDS = ['a', 'b', 'd']

        base_model = FromDictModel.from_dict({
            'a': 'Foo',
            'b': 'Bar',
            'c': 'Not in fields',
            'created_at': '2021-01-01T12:25:32',
            'updated_at': '2021-01-01T12:25:32',
        })

        self.assertEqual('2021-01-01T12:25:32', base_model.created_at)
        self.assertEqual('2021-01-01T12:25:32', base_model.updated_at)

    def test_to_dict(self):
        class ToDictModel(BaseModel):
            FIELDS = ['_id', 'a', 'b', 'd']

        base_model = ToDictModel()
        base_model._id = 123
        base_model.a = 'Filled'
        base_model.c = 'Ignored'
        base_model.d = None

        dictionary_model = base_model.to_dict()
        keys = set(dictionary_model.keys())

        self.assertEqual(123, dictionary_model['_id'])
        self.assertEqual('Filled', dictionary_model['a'])
        self.assertIsNone(dictionary_model['d'])
        self.assertIsNotNone(dictionary_model['created_at'])
        self.assertIsNotNone(dictionary_model['updated_at'])
        self.assertEqual({'_id', 'a', 'd', 'created_at', 'updated_at'}, keys)

    def test_to_dict_without_id(self):
        class ToDictModel(BaseModel):
            FIELDS = ['_id', 'a']

        base_model = ToDictModel()
        base_model._id = None
        base_model.a = 'Filled'

        dictionary_model = base_model.to_dict()
        keys = set(dictionary_model.keys())

        self.assertEqual('Filled', dictionary_model['a'])
        self.assertEqual({'a', 'created_at', 'updated_at'}, keys)

    def test_get_collection_without_table_name(self):
        base_model = BaseModel()

        with self.assertRaises(ValueError) as error:
            base_model.get_collection()

        self.assertEqual('Without tablename on class BaseModel', error.exception.args[0])

    def test_get_collection_when_not_started(self):
        class TableModel(BaseModel):
            TABLE_NAME = 'foo'
        base_model = TableModel()

        collection = base_model.get_collection()

        self.assertIsNotNone(collection)

    def test_parse_id_object_id(self):
        base_model = BaseModel()
        base_model._id = '647cf43a468761ccea969d9e'
        base_model.parse_id()

        self.assertIsInstance(base_model._id, ObjectId)

    def test_parse_id_int(self):
        base_model = BaseModel()
        base_model._id = 12
        base_model.parse_id()

        self.assertIsInstance(base_model._id, int)

    def test_parse_id_none(self):
        base_model = BaseModel()
        base_model._id = None
        base_model.parse_id()

        self.assertIsNone(base_model._id)

    def test_parse_not_id(self):
        base_model = BaseModel()
        base_model.parse_id()

        with self.assertRaises(AttributeError):
            base_model._id
