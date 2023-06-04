import os
from unittest.mock import patch

from app.infra.database.mongodb import get_client
from tests import BaseTestCase


class TestMongodb(BaseTestCase):

    @patch.dict(os.environ, {'MONGO_DB_CONNECTION': ''})
    def test_get_client_without_connection_string(self):
        with self.assertRaises(ValueError) as exception:
            get_client()

        self.assertEqual(
            'Without connection string in environment variables',
            exception.exception.args[0],
        )
