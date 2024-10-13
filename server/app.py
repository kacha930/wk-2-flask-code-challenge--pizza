#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify 
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])


@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.to_dict_with_pizza()) 
    else:
        return jsonify({'error': 'Restaurant not found'}), 404
    

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({'message': 'Restaurant deleted'}), 204
    else:
        return jsonify({'error': 'Restaurant not found'}), 404
    

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    try:
        if 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:

            return make_response(jsonify({"errors": ["Missing required fields"]}), 400)
        
        # pizza = pizza.query.get(data['pizza_id'])
        # restaurant = Restaurant.query.get(data['restaurant_id'])

        # if not pizza or not restaurant:
        #     return make_response(jsonify({"errors": ["Invalid pizza or restaurant ID"]}), 400)
        new_rp = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        db.session.add(new_rp)
        db.session.commit()

        return make_response(new_rp.to_dict_with_relationships(), 201)
    
    except Exception as e:
        return make_response(jsonify({'error': str(e)})), 400


         
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)
