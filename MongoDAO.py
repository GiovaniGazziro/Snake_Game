import pymongo
from pymongo import MongoClient


class MongoDAO():
    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client.Snake

        self.Data = db.Data
    

    def insert_mongo(self, informacoes):
        try:
            print("\n")
            print("informacoes")
            print("\n")
            print(informacoes)
            print("\n")
            self.Data.insert(informacoes)
        except:
            print("Unexpected error:", sys.exc_info()[0])
        
t = MongoDAO()