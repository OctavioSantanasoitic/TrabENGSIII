from bson.objectid import ObjectId

from app.domain.model.employee import Employee


class UpsertEmployee:
    def __init__(self, employee_data: dict):
        self.employee_data = employee_data

    def execute(self):
        employee = Employee.from_dict(self.employee_data)
        if not employee.is_valid:
            raise ValueError('Failed on fields validation "{}"'.format(employee.string_errors))
        collection = Employee.get_collection()

        filter_by_id = {'_id': ObjectId(self.employee_data.get('_id'))}
        if self.employee_data.get('_id'):
            collection.update_one(filter_by_id, {'$set': employee.to_dict()})
            return

        if collection.find_one({'cpf': employee.cpf}) is not None:
            raise ValueError('Employee with cpf "{}" already exists'.format(employee.cpf))

        collection.insert_one(employee.to_dict())
