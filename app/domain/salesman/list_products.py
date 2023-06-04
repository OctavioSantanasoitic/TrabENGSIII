import pymongo

from app.domain.model.product import Product


class SalesmanListProducts:
    def __init__(self, page: int, limit: int, product_name: str) -> None:
        self.page = int(page or 1)
        self.limit = int(limit or 10)
        self.product_name = str(product_name or '')

    def execute(self):
        name_filter = {'name': {'$regex': self.product_name}} if self.product_name else None

        return Product.get_collection() \
            .find(name_filter) \
            .limit(limit=self.limit) \
            .skip(skip=(self.page - 1) * self.limit) \
            .sort('name', pymongo.ASCENDING)
