from app.domain.model.product import Product
from app.domain.salesman.list_products import SalesmanListProducts
from tests import BaseTestCase


class TestListProducts(BaseTestCase):

    DROP_MONGO = True

    def setUp(self) -> None:
        super().setUp()
        product_collection = Product.get_collection()
        self.product_id = product_collection.insert_one(Product.from_dict({
            'name': '<product-1>',
            'available_quantity': 124,
            'color': 'blue',
            'sizes': 'GG',
            'price': 79.9,
        }).to_dict()).inserted_id

        self.second_product_id = product_collection.insert_one(Product.from_dict({
            'name': '<product-2>',
            'available_quantity': 312,
            'color': 'blue',
            'sizes': '46',
            'price': 149.9,
        }).to_dict()).inserted_id

    def test_list_first_page(self):
        products = SalesmanListProducts(page=1, limit=1, product_name=None).execute()
        product_ids = list(map(lambda x: x['_id'], products))

        self.assertEqual(1, len(product_ids))
        self.assertEqual(self.product_id, product_ids[0])

    def test_list_second_page(self):
        products = SalesmanListProducts(page=2, limit=1, product_name=None).execute()
        product_ids = list(map(lambda x: x['_id'], products))

        self.assertEqual(1, len(product_ids))
        self.assertEqual(self.second_product_id, product_ids[0])

    def test_filter(self):
        products = SalesmanListProducts(page=1, limit=1, product_name='2').execute()
        product_ids = list(map(lambda x: x['_id'], products))

        self.assertEqual(1, len(product_ids))
        self.assertEqual(self.second_product_id, product_ids[0])
