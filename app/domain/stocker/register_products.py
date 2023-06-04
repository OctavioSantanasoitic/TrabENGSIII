from app.domain.model.product import Product


class RegisterProducts:

    def __init__(self, products: list[dict]) -> None:
        self.products = products

    def execute(self):
        collection = Product.get_collection()

        for product in map(Product.from_dict, self.products):
            if not product._id:
                collection.insert_one(product.to_dict())
                continue

            filter = {'_id': product._id}
            old_product = Product.from_dict(collection.find_one(filter))
            old_product.add_product(product)
            collection.update_one(filter, {'$set': product.to_dict()})
