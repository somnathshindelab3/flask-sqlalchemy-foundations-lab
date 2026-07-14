# server/app.py
#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


def seed_database():
    """Populate the database with sample earthquakes if no rows exist."""
    if Earthquake.query.count() == 0:
        earthquakes = [
            Earthquake(magnitude=9.5, location="Chile", year=1960),
            Earthquake(magnitude=9.2, location="Alaska", year=1964),
            Earthquake(magnitude=8.6, location="Alaska", year=1946),
            Earthquake(magnitude=8.5, location="Banda Sea", year=1934),
            Earthquake(magnitude=8.4, location="Chile", year=1922),
        ]
        db.session.add_all(earthquakes)
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_database()


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    quake = Earthquake.query.get(id)
    if quake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    return jsonify(quake.to_dict()), 200


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).order_by(Earthquake.id).all()
    quake_data = [quake.to_dict() for quake in quakes]
    return jsonify({"count": len(quake_data), "quakes": quake_data}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
