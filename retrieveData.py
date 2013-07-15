#!/usr/bin/env python
import json, os, requests
from models import db, FoodMenu, FoodServices, Outlets

key = os.environ.get('UWOPENDATA_APIKEY')

def getData(service):
	payload = {'key': key, 'service': service}
	r = requests.get('http://api.uwaterloo.ca/public/v1/', params=payload)
	return r

def retrieve(service):
	payload = {'key': key}
	url = os.environ.get('API_URL') + service
	r = requests.get(url, params=payload)
	return r

foodMenu = retrieve('menu.json').text
foodMenuData = FoodMenu(foodMenu)
serviceInfo = getData('FoodServices').text
serviceInfoData = FoodServices(serviceInfo)
outlets = retrieve('outlets.json').text
outletsData = Outlets(outlets)
db.session.add(foodMenuData)
db.session.add(serviceInfoData)
db.session.add(outletsData)
db.session.commit()
