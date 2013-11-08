#!/usr/bin/env python
import json, os, requests
from datetime import datetime, date
from pytz import timezone
from flask import Flask, render_template, url_for, jsonify
from models import app, db, FoodMenu, Locations

MIXPANEL_TOKEN = os.environ.get('MIXPANEL_TOKEN')

@app.route('/')
def renderMenu():
	nowWaterloo = datetime.now(timezone('America/Toronto'))
	foodMenu = FoodMenu.query.order_by(FoodMenu.id.desc()).first().result
	menu = json.loads(foodMenu)['data']
	locationsInfo = Locations.query.order_by(Locations.id.desc()).first().result
	locations = json.loads(locationsInfo)['data']
	return render_template('index.html', menu=menu, locations=locations, nowWaterloo=nowWaterloo, mixpanelToken=MIXPANEL_TOKEN)

@app.route('/foodmenu')
def foodmenu():
	foodMenu = FoodMenu.query.order_by(FoodMenu.id.desc()).first().result
	menu = json.loads(foodMenu)['data']
	return jsonify(menu)

def datetimeformat(value, FULL_DATE_FORMAT='%Y-%m-%d', MONTH_DAY_FORMAT='%B %d'):
	valueDate = datetime.strptime(value, FULL_DATE_FORMAT)
	return valueDate.strftime(MONTH_DAY_FORMAT)

def building_info(outlet_id, locations):
	for location in locations:
		if location['outlet_id'] == outlet_id:
			return '%s - %s, %s' % (location['building'], location['latitude'], location['longitude'])

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.jinja_env.filters['datetimeformat'] = datetimeformat
	app.jinja_env.filters['building_info'] = building_info
	app.run(host='0.0.0.0', port=port)
