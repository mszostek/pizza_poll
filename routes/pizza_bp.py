from flask import Blueprint

from controllers.PizzaController import index, create, show, vote_up, change_status

pizza_bp = Blueprint('pizza_bp', __name__)

pizza_bp.route('/', methods=['GET'])(index)
pizza_bp.route('/add', methods=['POST'])(create)
pizza_bp.route('/show/<int:pizza_id>', methods=['GET'])(show)
pizza_bp.route('/vote/<int:pizza_id>', methods=['PATCH'])(vote_up)
pizza_bp.route('/change_status/<int:pizza_id>', methods=['PATCH'])(change_status)
