from datetime import datetime

from bson import ObjectId
from app.infra.database.mongodb import get_database


class BaseModel:

    TABLE_NAME = ''

    FIELDS = []

    def after_fill(self):
        pass

    def parse_id(self):
        if not hasattr(self, '_id'):
            return
        if not self._id:
            return
        if isinstance(self._id, ObjectId):
            return
        if not isinstance(self._id, str):
            return
        self._id = ObjectId(self._id)

    @property
    def validation(self) -> list[tuple[bool, str]]:
        return []

    @property
    def errors(self):
        try:
            for (valid_condition, message) in self.validation:
                if not valid_condition:
                    yield message
        except Exception as e:
            yield 'Failed on validation "{}"'.format(str(e))

    @property
    def string_errors(self):
        errors = list(self.errors)
        return ('\n\t' + '\n\t'.join(errors)) if errors else ''

    @property
    def is_valid(self):
        return not any(self.errors)

    @classmethod
    def get_collection(cls):
        if not cls.TABLE_NAME:
            raise ValueError('Without tablename on class {}'.format(cls.__name__))

        database = get_database()

        return database[cls.TABLE_NAME]

    @classmethod
    def from_dict(cls, data: dict):
        new_item = cls()

        for key in cls.FIELDS:
            setattr(new_item, key, None)

        for key, value in data.items():
            setattr(new_item, key, value)

        if not hasattr(new_item, 'created_at'):
            setattr(new_item, 'created_at', datetime.utcnow())

        if not hasattr(new_item, 'updated_at'):
            setattr(new_item, 'updated_at', new_item.created_at)

        new_item.parse_id()
        new_item.after_fill()
        return new_item

    def to_dict(self):
        result = dict()

        for key in self.FIELDS:
            if key == '_id' and hasattr(self, '_id') and not getattr(self, '_id'):
                continue

            if hasattr(self, key):
                result[key] = getattr(self, key)

        result['created_at'] = result.get('created_at', datetime.utcnow())
        result['updated_at'] = result.get('updated_at', result['created_at'])

        return result
