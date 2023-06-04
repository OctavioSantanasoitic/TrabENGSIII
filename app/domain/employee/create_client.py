from app.domain.model.client import Client


class CreateClient:
    def __init__(self, data: dict):
        self.data = data

    def execute(self):
        collection = Client.get_collection()

        client = Client.from_dict(self.data)
        string_errors = client.string_errors
        if string_errors:
            raise ValueError('Client data have errors: {}'.format(string_errors))

        registered_client = collection.find_one({'cpf': client.cpf})
        if registered_client:
            raise ValueError('Client with cpf "{}" already exists'.format(client.cpf))

        collection.insert_one(client.to_dict())
