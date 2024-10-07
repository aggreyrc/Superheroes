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

if __name__ == '__main__':
    app.run(port=5555, debug=True)