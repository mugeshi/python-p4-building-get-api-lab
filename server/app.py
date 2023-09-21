#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def get_all_bakeries():
    try:
        bakeries = Bakery.query.all()
        bakery_data = [{'id': bakery.id, 'name': bakery.name} for bakery in bakeries]
        return jsonify(bakery_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_with_baked_goods(id):
    try:
        bakery = Bakery.query.get(id)
        if not bakery:
            return jsonify({'error': 'Bakery not found'}), 404

        baked_goods = BakedGood.query.filter_by(bakery_id=id).all()
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'baked_goods': [{'id': bg.id, 'name': bg.name, 'price': bg.price} for bg in baked_goods]
        }
        return jsonify(bakery_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    try:
        baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
        baked_goods_data = [{'id': bg.id, 'name': bg.name, 'price': bg.price} for bg in baked_goods]
        return jsonify(baked_goods_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    try:
        most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
        if not most_expensive_baked_good:
            return jsonify({'error': 'No baked goods found'}), 404

        baked_good_data = {
            'id': most_expensive_baked_good.id,
            'name': most_expensive_baked_good.name,
            'price': most_expensive_baked_good.price
        }
        return jsonify(baked_good_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(port=5555, debug=True)
