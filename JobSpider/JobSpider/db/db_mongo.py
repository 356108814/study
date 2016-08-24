# encoding: utf-8
"""
mongodb
@author Yuriseus
@create 2016-8-24 14:54
"""
from pymongo import MongoClient


class DBMongo(object):
    def __init__(self, host, port, db):
        self._client = MongoClient('mongodb://%s:%s' % (host, port))
        self._db = self._client[db]

    def find(self, collection_name, param_dict=None):
        docs = []
        collection = self._db[collection_name]
        if param_dict:
            cursor = collection.find(param_dict)
        else:
            cursor = collection.find()
        for document in cursor:
            docs.append(document)
        if len(docs) == 1:
            return docs[0]
        return docs

    def insert(self, collection_name, doc_or_docs):
        collection = self._db[collection_name]
        result = collection.insert(doc_or_docs)
        return result

    def update(self, collection_name, data_dict):
        collection = self._db[collection_name]
        result = collection.update_one(data_dict)
        return result

    def delete_many(self, collection_name, param_dict):
        collection = self._db[collection_name]
        result = collection.delete_many(param_dict)
        return result

if __name__ == '__main__':
    db_mongo = DBMongo('172.16.1.206', 27017, 'lagou')
    jobs = db_mongo.find('job', {'title': 'python'})
    print(jobs)
