#!/usr/bin/env python
import json, os, requests
from models import db, FoodMenu, FoodServices

key = os.environ.get('UWOPENDATA_APIKEY')

def getData(service):
	payload = {'key': key, 'service': service}
	r = requests.get('http://api.uwaterloo.ca/public/v1/', params=payload)
	return r

foodMenu = getData('FoodMenu').text
foodMenuData = FoodMenu(foodMenu)
serviceInfo = getData('FoodServices').text
serviceInfoData = FoodServices(serviceInfo)
db.session.add(foodMenuData)
db.session.add(serviceInfoData)
db.session.commit()
