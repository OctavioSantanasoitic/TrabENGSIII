from bson.objectid import ObjectId

from app.domain.model.employee import Employee


class DisableEmployee:
    def __init__(self, employee_id: str):
        self.employee_id = employee_id

    def execute(self):
        collection = Employee.get_collection()

        id_filter = {'_id': ObjectId(self.employee_id)}
        employee_dict = collection.find_one(id_filter)
        if not employee_dict:
            raise ValueError('Without employee with id {}'.format(self.employee_id))

        employee = Employee.from_dict(employee_dict)
        employee.disable()

        collection.update_one(id_filter, {'$set': {'is_active': False}})
