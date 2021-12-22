import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from blacklist import BLACKLIST


BLANK_ERROR = "'{}' connot be blank"
USER_ALREADY_EXIST = "'{}' already exists"
ERROR_INSERTING = "An Error occurred while inserting the item"
USER_CREATED = "User Created"
USER_NOT_FOUND = "User Not Found"
USER_NOT_FOUND = "User Not Found"
USER_DELETED = "User Deleted"
INVALID_CREDENTIAL = "Invalid Credential"
LOGOUT_SUCCESS = "Successfully Logout"

parser = reqparse.RequestParser()
parser.add_argument('username',
                    type=str,
                    required=True,
                    help=BLANK_ERROR.format('username')
                    )
parser.add_argument('password',
                    type=str,
                    required=True,
                    help=BLANK_ERROR.format('password')
                    )


class UserRegister(Resource):
   
    @classmethod
    def post(cls):
        data = parser.parse_args()
        if UserModel.get_by_username(data['username']):
            return {'message': USER_ALREADY_EXIST.format(data['username'])}, 400

        user = UserModel(**data)
        print(user)
        user.save_to_db()
        return {'message': USER_CREATED}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.get_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.get_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {'message': USER_DELETED}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = parser.parse_args()
        user = UserModel.get_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_toke = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_toke,
                'refresh_token': refresh_token
            }, 200

        return {'message': INVALID_CREDENTIAL}, 401


class UserLogout(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': LOGOUT_SUCCESS}, 200


class TokenRefresh(Resource):

    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_usser = get_jwt_identity()
        new_token = create_access_token(identity=current_usser, fresh=False)
        return {'access_token': new_token}, 200
