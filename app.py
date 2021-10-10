from flask import Flask
from flask_migrate import Migrate
from flask_json import FlaskJSON, as_json

from models.Models import db
from routes.pizza_bp import pizza_bp
from routes.topping_bp import topping_bp

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

json = FlaskJSON(app)

app.register_blueprint(pizza_bp, url_prefix='/pizza')
app.register_blueprint(topping_bp, url_prefix='/topping')

if __name__ == '__main__':
    app.debug = True
    app.run()


@app.route("/")
@as_json
def hello():
    return "Hello, World!"


@app.route("/bye")
@as_json
def bye():
    return dict(msg="Bye, bye cruel world…")
