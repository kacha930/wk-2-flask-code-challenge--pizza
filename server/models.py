from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship 
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)

    # add relationship
    pizzas = relationship('RestaurantPizza', back_populates='restaurant', cascade="all, delete-orphan")


    # add serialization rules
    serialize_rules = ('-pizzas.restaurant',)

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "address": self.address,
        }
    
    def to_dict_with_pizza(self):
        return{
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "restaurant_pizzas": [rp.to_dict() for rp in self.pizzas]
        }

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String)

    # add relationship
    restaurants = relationship('RestaurantPizza', back_populates = 'pizza', cascade="all, delete-orphan")


    # add serialization rules
    serialize_rules = ('-restaurants.pizza',)


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
        }
    

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)

    restaurant = relationship('Restaurant', back_populates='pizzas')
    pizza = relationship('Pizza', back_populates='restaurants')

    # add serialization rules

    serialize_rules = ('-restaurant.pizzas', '-pizza.restaurants')

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "restaurant_id": self.restaurant_id,
            "pizza_id": self.pizza_id,         
        }
    
    def to_dict_with_relationships(self):
        return {
            "id": self.id,
            "price": self.price,
            "restaurant_id": self.restaurant_id,
            "pizza_id": self.pizza_id,
            "restaurant": self.restaurant.to_dict(),
            "pizza": self.pizza.to_dict()

        }

    # add validation
    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        return price
    
    
    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'
