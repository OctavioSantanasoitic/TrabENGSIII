from bson import ObjectId

from app.domain.model.base.base_model import BaseModel


class Sale(BaseModel):

    TABLE_NAME = 'sale'

    FIELDS = [
        '_id',
        'products',
        'cashier_id',
        'client_id',
        'total_value',
    ]

    @property
    def validation(self) -> list[tuple[bool, str]]:
        return [
            (self.products, 'Sale products are required'),
            (list(self.products), 'Products are list'),
            (self.cashier_id, 'Sale cashier id is required'),
            (self.total_value, 'Sale total value is required'),
        ]

    def after_fill(self):
        self.cashier_id = ObjectId(self.cashier_id) if self.cashier_id else None
        self.client_id = ObjectId(self.client_id) if self.client_id else None
