from app.domain.model.base.base_model import BaseModel


class Product(BaseModel):

    TABLE_NAME = 'product'

    FIELDS = [
        '_id',
        'name',
        'available_quantity',
        'color',
        'sizes',
        'price',
    ]

    @property
    def validation(self) -> list[tuple[bool, str]]:
        return [
            (self.name, 'Name is required'),
            (self.available_quantity and int(self.available_quantity), 'Quantity is a integer'),
            (self.price and float(self.price), 'Price is required'),
        ]

    def add_product(self, product: 'Product'):
        if self._id != product._id:
            raise ValueError('You cannot add different products')

        quantity_sum = self.available_quantity + product.available_quantity
        self.available_quantity = product.available_quantity = quantity_sum
