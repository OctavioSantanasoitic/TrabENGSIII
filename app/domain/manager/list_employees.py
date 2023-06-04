import pymongo

from app.domain.model.employee import Employee


class ListEmployees:
    def __init__(self, page: int, limit: int, filters: dict = {}) -> None:
        self.page = int(page or 1)
        self.limit = int(limit or 10)
        self.filters = filters

    def execute(self):
        filters = {}
        for key, value in self.filters.items():
            filters |= {key: {'$regex': value}}

        return Employee.get_collection() \
            .find(filters) \
            .limit(limit=self.limit) \
            .skip(skip=(self.page - 1) * self.limit) \
            .sort('name', pymongo.ASCENDING)
