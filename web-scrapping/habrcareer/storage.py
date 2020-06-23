from pymongo import MongoClient


class Storage:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['habrcareer']

    def get_company(self, name):
        return self.db.company.find_one({'name': name})

    def save_company(self, company):
        self.db.company.insert_one(company.to_dict())

    def save_transition(self, transition):
        self.db.company.insert_one(transition.to_dict())
