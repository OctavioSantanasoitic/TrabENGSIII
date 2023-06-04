from unittest import TestCase

from app.infra.database.mongodb import get_client


class BaseTestCase(TestCase):

    DROP_MONGO = False

    def _drop_mongo(self):
        if not self.DROP_MONGO:
            return

        client = get_client()
        client.drop_database('test')

    def setUp(self) -> None:
        super().setUp()
        self._drop_mongo()
