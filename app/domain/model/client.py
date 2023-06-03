from bson import ObjectId
from app.domain.model.base.base_model import BaseModel
from app.domain.value_objects.cpf import Cpf


class Client(BaseModel):

    TABLE_NAME = 'employee'

    FIELDS = [
        '_id',
        'name',
        'birth_date',
        'cpf',
        'registered_by_employee_id',
    ]

    @property
    def validation(self) -> list[tuple[bool, str]]:
        return [
            (self.name, 'Name is required'),
            (self.cpf, 'Cpf is required'),
            (self.registered_by_employee_id, 'Employee id is required'),
            (Cpf.validate(self.cpf), 'Cpf is not valid'),
        ]

    def after_fill(self):
        self.cpf = Cpf(self.cpf).to_str()
        self.registered_by_employee_id = ObjectId(self.registered_by_employee_id) \
            if self.registered_by_employee_id \
            else None
