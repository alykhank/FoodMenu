#!/usr/bin/env python

"""Declare models for objects in Menu and Locations data."""

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class FoodMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Text)

    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return "<FoodMenu('%s')>" % (self.result)

class Locations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Text)

    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return "<Locations('%s')>" % (self.result)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    week = db.Column(db.Integer)
    year = db.Column(db.Integer)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    outlets = db.relationship('Outlet', backref='response')

class Outlet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outlet_number = db.Column(db.Integer)
    outlet_name = db.Column(db.Text)
    menu = db.relationship('Menu', backref='outlet')
    response_id = db.Column(db.Integer, db.ForeignKey('response.id'))

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    day = db.Column(db.String(10))
    meals = db.relationship('Meals', uselist=False, backref='menu')
    notes = db.Column(db.Text)
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlet.id'))

class Meals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lunch = db.relationship('Product')
    dinner = db.relationship('Product')
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_number = db.Column(db.Integer)
    product_name = db.Column(db.String(100))
    diet_type = db.Column(db.String(20))
    meals_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
