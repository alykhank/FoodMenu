#!/usr/bin/env python
import json, os, requests
from models import db, FoodMenu, Locations

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
db.session.commit()
