#!/usr/bin/env python
import json, os, requests
from datetime import datetime
from pytz import timezone
from models import db, FoodMenu, Locations, Response, Outlet, Menu, Meals, Product

key = os.environ.get('UWOPENDATA_APIKEY')

def retrieve(service):
	payload = {'key': key}
	url = os.environ.get('API_URL') + service
	r = requests.get(url, params=payload)
	return r

foodMenu = retrieve('menu.json').text
foodMenuData = FoodMenu(foodMenu)
locations = retrieve('locations.json').text
locationsData = Locations(locations)
db.session.add(foodMenuData)
db.session.add(locationsData)

data = json.loads(foodMenu)['data']
now = datetime.now(timezone('America/Toronto'))
outlets = []
for o in data['outlets']:
	menus = []
	for m in o['menu']:
		lunch_products = []
		for p in m['meals']['lunch']:
			product = Product(
					product_number=p['product_id'],
					product_name=p['product_name'],
					diet_type=p['diet_type']
				)
			lunch_products.append(product)
			db.session.add(product)
		dinner_products = []
		for p in m['meals']['dinner']:
			product = Product(
					product_number=p['product_id'],
					product_name=p['product_name'],
					diet_type=p['diet_type']
				)
			dinner_products.append(product)
			db.session.add(product)
		meals = Meals(
				lunch=lunch_products,
				dinner=dinner_products
			)
		db.session.add(meals)
		menu = Menu(
				date=m['date'],
				day=m['day'],
				meals=meals,
				notes=m['notes']
			)
		menus.append(menu)
		db.session.add(menu)
	outlet = Outlet(
			outlet_number=o['outlet_id'],
			outlet_name=o['outlet_name'],
			menu=menus
		)
	outlets.append(outlet)
	db.session.add(outlet)
response = Response(
		date=now,
		week=data['date']['week'],
		year=data['date']['year'],
		start=data['date']['start'],
		end=data['date']['end'],
		outlets=outlets
	)
db.session.add(response)

db.session.commit()
