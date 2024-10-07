from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Hero API"


# Get heroes
@app.route('/heroes')
def heroes():
    heroes = []
    for hero in Hero.query.all():
        hero_dict = {
            'name': hero.name,
            'super_name': hero.super_name,
        }
        heroes.append(hero_dict)
        
    response = make_response(
        heroes,
        200,
        {'Content-Type': 'application/json'}
    )
    return response

# Get heroes by id
@app.route('/heroes/<int:id>')
def get_hero_by_id(id):
    hero = Hero.query.filter(Hero.id == id).first()
    if hero:
        hero_dict = {
            'name': hero.name,
            'super_name': hero.super_name,
        }
        response = make_response(
            hero_dict,
            200,
            {'Content-Type': 'application/json'}
        )
    else:
        response = make_response(
            jsonify({'error': 'Hero not found'}),
            404,
            {'Content-Type': 'application/json'}
        )
    return response


# Get Powers
@app.route('/powers')
def powers():
    powers = []
    for power in Power.query.all():
        power_dict = {
            'name': power.name,
            'description': power.description,
        }
        powers.append(power_dict)
        
    response = make_response(
        powers,
        200,
        {'Content-Type': 'application/json'}
    )
    return response

# Get powers by id
@app.route('/powers/<int:id>')
def get_power_by_id(id):
    power = Power.query.filter(Power.id == id).first()
    if power:
        power_dict = {
            'name': power.name,
            'description': power.description,
        }
        response = make_response(
            power_dict,
            200,
            {'Content-Type': 'application/json'}
        )
    else:
        response = make_response(
            jsonify({'error': 'Power not found'}),
            404,
            {'Content-Type': 'application/json'}
        )
    return response
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)