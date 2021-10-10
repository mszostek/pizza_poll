from datetime import date

from flask import abort, request
from flask_json import as_json

from models.Models import Pizza, Topping


@as_json
def index():
    toppings = Topping.query.all()
    if len(toppings) == 0:
        abort(404)

    return [t.serialize for t in toppings]
    pass


def create():
    try:
        topping = Topping(name=request.form.get('name'), added=date.today())
        topping.create()
        return topping.serialize
    except Exception as e:
        # debugging for poor ones
        print(e)
    pass


def add_to_pizza(topping_id, pizza_id):
    if topping_id is None or pizza_id is None:
        abort(404)

    topping = Topping.query.filter_by(id=topping_id).first_or_404()
    pizza = Pizza.query.filter_by(id=pizza_id).first_or_404()
    topping.add_to_pizza(pizza)

    return pizza.serialize
