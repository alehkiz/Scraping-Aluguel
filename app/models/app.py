

from app.core.db import db


class Immobile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bedrooms = db.Column(db.Integer, unique=False, nullable=True)
    bathrooms = db.Column(db.Integer, unique=False, nullable=True)
    parking = db.Column(db.Integer, unique=False, nullable=True)
    area = db.Column(db.Integer, unique=False, nullable=True)
    neighborhood = db.Column(db.Integer, unique=False, nullable=True)
    s_neighborhood = db.Column(db.String, unique=False, nullable=True)
    validate = db.Column(db.Boolean, unique=False, nullable=True)
    price = db.Column(db.Float, unique=False, nullable=True)
    correct_value = db.Column(db.Float, unique=False, nullable=True)