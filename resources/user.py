import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel




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