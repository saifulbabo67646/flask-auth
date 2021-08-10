from typing import Dict, Union
from db import db

ItemJson = Dict[str, Union[int, str, float, int]]

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name: str, price: float, store_id: int) -> None:
         self.name = name
         self.price = price
         self.store_id = store_id
    
    def json(self) -> ItemJson:
        return {
            'id': self.id,
            'name': self.name, 
            'price': self.price,
            'store_id': self.store_id
            }

    @classmethod
    def find_by_name(cls, name) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()