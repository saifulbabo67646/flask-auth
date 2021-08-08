from flask import request
from flask_jwt_extended.utils import get_jwt_identity
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from models.item import ItemModel

# items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type = float,
        required = True,
        help = 'This field cannot be blank!'
    )
    parser.add_argument('store_id', 
        type = int,
        required = True,
        help = 'Every Item need a store Id!'
    )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not Found!'}, 404
    
    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An Item with name {name} already exists'}, 400
        data = Item.parser.parse_args()
        new_item = ItemModel(name, **data)
        try:
            new_item.save_to_db()
        except:
            return {'message': 'An Error occured inserting the item'}, 500
        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin priilege Required.'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item Deleted'}

    def put(self, name):
        
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

    
class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        if user_id:
            return {'Items': [item.json() for item in ItemModel.query.all()]}, 200
        return {
            'Items': [item.name for item in ItemModel.query.all()],
            'message': 'More Data available if you login' 
            }, 200
        