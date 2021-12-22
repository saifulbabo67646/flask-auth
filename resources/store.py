from flask_restful import Resource
from models.store import StoreModel

NAME_ALREADY_EXIST = "A Store with name '{}' already exists"
ERROR_CREATING = "An Error occurred while creating the store"
STORE_NOT_FOUND = "Store Not Found"
STORE_DELETED = "Store Deleted"

class Store(Resource):

    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': STORE_NOT_FOUND}, 404
    
    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXIST.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': ERROR_CREATING}, 500

        return store.json(), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': STORE_DELETED}


class StoreList(Resource):

    @classmethod
    def get(cls):
        return {'Stores': [store.json() for store in StoreModel.query.all()]}