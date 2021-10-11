from dataclasses import dataclass
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


association_table = db.Table('association', db.Model.metadata,
    db.Column('pizza_id', db.Integer, db.ForeignKey('pizzas.id'), primary_key=True),
    db.Column('topping_id', db.Integer, db.ForeignKey('toppings.id'), primary_key=True)
)


@dataclass
class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    votes = db.Column(db.Integer, default=0)
    added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    topping = relationship("Topping", secondary=association_table, backref="toppings_pizza")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'votes': self.votes,
            'added': dump_datetime(self.added),
            'active': self.active,
            'toppings': [topping.serialize_name for topping in self.topping],
        }

    def __init__(self, name, votes, added, active):
        self.name = name
        self.votes = votes
        self.added = added
        self.active = active

    def create(self):
        db.session.add(self)
        db.session.commit()

    def vote(self):
        self.votes += 1
        db.session.merge(self)
        db.session.commit()

    def change_status(self):
        self.active = not self.active
        db.session.merge(self)
        db.session.commit()


@dataclass
class Topping(db.Model):
    __tablename__ = 'toppings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pizza = relationship("Pizza", secondary=association_table, backref="pizza_toppings")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'added': dump_datetime(self.added),
        }

    @property
    def serialize_name(self):
        return self.name

    def __init__(self, name, added):
        self.name = name
        self.added = added

    def create(self):
        print(self)
        db.session.add(self)
        db.session.commit()

    def add_to_pizza(self, pizza):
        pizza.topping.append(self)
        db.session.commit()


def dump_datetime(value):
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")
