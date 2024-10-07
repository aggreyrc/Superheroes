from flask import Flask, jsonify, make_response, request
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
    return "Index for Heroes API"


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


# Patch powers
@app.route('/powers/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def power_by_id(id):
    power = Power.query.filter(Power.id == id).first()
    
    if power == None:
        response_body = {
            "error": "Power not found"
        }
        response = make_response(response_body,404)
        
        return response
    
    else:
        if request.method == 'GET':
            power_dict = {
                'name': power.name,
                'description': power.description,
            }
            response = make_response(
                power_dict,
                200
            )
            
            return response
        
        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(power, attr, request.form.get(attr))
                
            db.session.add(power)
            db.session.commit()
            
            power_dict = {
                'description': "Valid Updated Description",
                "id": power.id,
                'name': power.name
            }
            
            response = make_response(
                power_dict,
                200
            )
            
            return response
        
        
        elif request.method == 'DELETE':
            db.session.delete(power)
            db.session.commit()
            
            response_body = {
                "delete_successful": True,
                "message": "Power deleted successfully"
            }
            
            response = make_response(
                response_body,
                200
            )

            return response
        
        
# POST hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    try:
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(hero_power)
        db.session.commit()
        
        hero = Hero.query.get(hero_power.hero_id)
        power = Power.query.get(hero_power.power_id)
        
        return jsonify({
            "id": hero_power.id,
            "hero_id": hero_power.hero_id,
            "power_id": hero_power.power_id,
            "strength": hero_power.strength,
            "hero": {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            },
            "power": {
                "description": power.description,
                "id": power.id,
                "name": power.name
            }
        })
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"errors": ["Validation Errors"]}), 500
     
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)