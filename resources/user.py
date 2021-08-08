import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from blacklist import BLACKLIST



class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str,
        required = True,
        help="This field not be blank!"
    )
    parser.add_argument('password', 
        type=str,
        required = True,
        help="This field can not be blank!"
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.get_by_username(data['username']):
            return {'message': 'This user Already Exist!'}, 400
            
        user = UserModel(**data)
        print(user)
        user.save_to_db()
        return {'message': 'User Created'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.get_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.get_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User Deleted.'}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str,
        required = True,
        help="This field not be blank!"
    )
    parser.add_argument('password', 
        type=str,
        required = True,
        help="This field can not be blank!"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.get_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_toke = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_toke,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid Credential'}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Successfully Logged Out.'}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_usser = get_jwt_identity()
        new_token = create_access_token(identity=current_usser, fresh=False)
        return {'access_token': new_token}, 200


