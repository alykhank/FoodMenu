#!/usr/bin/env python
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
