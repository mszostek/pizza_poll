from flask import Blueprint

from controllers.ToppingController import index, create, add_to_pizza

topping_bp = Blueprint('topping_bp', __name__)

topping_bp.route('/', methods=['GET'])(index)
topping_bp.route('/add', methods=['POST'])(create)
topping_bp.route('/<int:topping_id>/pizza/<int:pizza_id>', methods=['POST'])(add_to_pizza)
