#!/usr/bin/env python
import json, os, requests
from datetime import datetime, date
from pytz import timezone
from flask import Flask, render_template, url_for, jsonify
from models import app, db, FoodMenu, FoodServices

MIXPANEL_TOKEN = os.environ.get('MIXPANEL_TOKEN')

@app.route('/')
def renderMenu():
	nowWaterloo = datetime.now(timezone('America/Toronto'))
	foodMenu = FoodMenu.query.order_by(FoodMenu.id.desc()).first().result
	menu = json.loads(foodMenu)['data']
	serviceInfo = FoodServices.query.order_by(FoodServices.id.desc()).first().result
	locations = json.loads(serviceInfo)['response']['data']
	return render_template('index.html', menu=menu, locations=locations, nowWaterloo=nowWaterloo, mixpanelToken=MIXPANEL_TOKEN)

@app.route('/foodmenu')
def foodmenu():
	foodMenu = FoodMenu.query.order_by(FoodMenu.id.desc()).first().result
	menu = json.loads(foodMenu)['data']
	return jsonify(menu)

@app.route('/foodservices')
def foodservices():
	serviceInfo = FoodServices.query.order_by(FoodServices.id.desc()).first().result
	locations = json.loads(serviceInfo)['response']['data']
	return jsonify(locations)

def datetimeformat(value, format='%B %d'):
	currentDate = date(int(value[:4]), int(value[5:7]), int(value[8:]))
	return currentDate.strftime(format)

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.jinja_env.filters['datetimeformat'] = datetimeformat
	app.run(host='0.0.0.0', port=port)
