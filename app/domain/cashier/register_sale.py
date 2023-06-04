from bson import ObjectId
from app.domain.model.product import Product
from app.domain.model.sale import Sale


class RegisterSale:

    def __init__(self, cashier_id: str, product_ids: list[str]) -> None:
        self.cashier_id = cashier_id
        self.product_ids = list(map(lambda x: ObjectId(x), product_ids))

    def execute(self):
        products_collection = Product.get_collection()
        products = list(products_collection.find({'_id': {'$in': self.product_ids}}))

        sale = Sale()
        sale.products = products
        sale.cashier_id = self.cashier_id
        sale.total_value = sum(map(
            lambda y: next(filter(lambda x: x['_id'] == y, products))['price'],
            self.product_ids,
        ))

        Sale.get_collection().insert_one(sale.to_dict())
