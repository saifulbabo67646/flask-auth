import os
from flask import Flask
from flask.scaffold import F
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nthubrexkwsuwo:ca40099034d42f0f9fd32bfd97bc155e1e0f31e647404a99c8b8d20ab41b718f@ec2-54-228-139-34.eu-west-1.compute.amazonaws.com:5432/ddqr01k6d9ljt5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'saiful'
api = Api(app)

jwt = JWT(app, authenticate, identity)



api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)