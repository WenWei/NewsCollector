from pymongo import MongoClient

class DbUtils:
    client = {}

    def __init__(self, connectionString):
        self.client = MongoClient(connectionString)
    
    def getDatabase(self, name):
        return self.client[name]
    

