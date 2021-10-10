from datetime import date

from flask import abort, request
from flask_json import as_json

from models.Models import Pizza, Topping


@as_json
def index():
    pizzas = Pizza.query.join(Topping, Pizza.topping, isouter=True)\
        .order_by(Pizza.votes.desc(), Pizza.active.desc()).all()
    # pizzas = Pizza.query.order_by(Pizza.votes.desc(), Pizza.active.desc()).all()
    if len(pizzas) == 0:
        abort(404)

    return [p.serialize for p in pizzas]


def create():
    try:
        pizza = Pizza(name=request.form.get('name'),
                      votes=0, added=date.today(),
                      active=True)
        pizza.create()
        return pizza.serialize
    except Exception as e:
        # debugging for poor ones
        print(e)
        pass


def show(pizza_id):
    if pizza_id is None:
        abort(404)
    pizza = Pizza.query.filter_by(id=pizza_id).first_or_404("Głodujemy")
    return pizza.serialize


def vote_up(pizza_id):
    if pizza_id is None:
        abort(404)
    pizza = Pizza.query.filter_by(id=pizza_id).first_or_404()
    pizza.vote()
    return pizza.serialize


def change_status(pizza_id):
    if pizza_id is None:
        abort(404)
    pizza = Pizza.query.filter_by(id=pizza_id).first_or_404()
    pizza.change_status()
    return pizza.serialize
