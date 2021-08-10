from flask import request
from flask_jwt_extended.utils import get_jwt_identity
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from models.item import ItemModel

BLANK_ERROR = "'{}' connot be blank"
NAME_ALREADY_EXIST = "An Item with name '{}' already exists"
ERROR_INSERTING = "An Error occurred while inserting the item"
ITEM_NOT_FOUND = "Item Not Found"
ITEM_DELETED = "Item Deleted"

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type = float,
        required = True,
        help = BLANK_ERROR.format("price")
    )
    parser.add_argument('store_id', 
        type = int,
        required = True,
        help = BLANK_ERROR.format("store_id")
    )

    @classmethod
    @jwt_required()
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': ITEM_NOT_FOUND}, 404
    
    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXIST.format(name)}, 400
        data = Item.parser.parse_args()
        new_item = ItemModel(name, **data)
        try:
            new_item.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500
        return new_item.json(), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin priilege Required.'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': ITEM_DELETED}

    @classmethod
    def put(cls, name: str):
        
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

    
class ItemList(Resource):

    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        user_id = get_jwt_identity()
        if user_id:
            return {'Items': [item.json() for item in ItemModel.query.all()]}, 200
        return {
            'Items': [item.name for item in ItemModel.query.all()],
            'message': 'More Data available if you login' 
            }, 200
        