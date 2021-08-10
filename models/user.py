from typing import Dict, Union
from db import db

UserJson = Dict[str, Union[int, str]]


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self) -> UserJson:
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def get_by_username(cls, username) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()
