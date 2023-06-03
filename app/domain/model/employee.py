from enum import Enum

from app.domain.model.base.base_model import BaseModel
from app.domain.value_objects.cpf import Cpf


class Employee(BaseModel):
    class Position(Enum):
        SALESMAN = 1
        STOCKER = 2
        CASHIER = 3
        MANAGER = 4

    TABLE_NAME = 'employee'

    FIELDS = [
        '_id',
        'name',
        'birth_date',
        'position',
        'is_active',
        'cpf',
    ]

    @property
    def validation(self) -> list[tuple[bool, str]]:
        return [
            (self.name, 'Name is required'),
            (self.birth_date, 'Birth date is required'),
            (
                self.position and Employee.Position[self.position] in Employee.Position,
                'Position is not valid',
            ),
            (Cpf.validate(self.cpf), 'Cpf is not valid'),
        ]

    def after_fill(self):
        self.is_active = self.is_active is True
        self.cpf = Cpf(self.cpf).to_str()

    def enable(self):
        if self.is_active:
            raise ValueError('You cannot enable an already active employee')
        self.is_active = True

    def disable(self):
        if not self.is_active:
            raise ValueError('You cannot disabled an already not active employee')
        self.is_active = False
