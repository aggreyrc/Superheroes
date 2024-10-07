from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

# Hero table
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    
    # serialize rules
    serialize_rules = ('-hero_powers.hero')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    super_name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationship to hero_powers table
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade="all,delete-orphan")
    
    def __repr__(self):
        return f"<Hero {self.name} for {self.super_name}>"
    


# Powers table
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    
    # serialize rules
    serialize_rules = ('-hero_powers.power')
    
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(20), nullable=False)
    
    # Relationship to hero_powers table
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade="all,delete-orphan")
    
    # heroes = association_proxy('hero_powers', 'hero', creator=lambda hero_id: HeroPower(hero_id=hero_id))
    
    def __repr__(self):
        return f"<Power {self.name}>"



# Hero_powers table
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    
    # serialize rules
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(10))
    
    # Foreign keys
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    
    __table_args__ = (
        CheckConstraint("strength IN ('Strong', 'Weak', 'Average')"),
    )
    
    # Relationships to heroes and powers tables
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')
    
    def __repr__(self):
        return f"<HeroPower {self.hero_id} for {self.power_id}>"
    