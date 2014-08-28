#!/usr/bin/env python

"""Retrieve Menu and Locations from UW Open Data API and store in DB."""

import json
import os

import requests
from datetime import datetime
from pytz import timezone

from models import db
from models import FoodMenu, Locations, Response, Outlet, Menu, Meals, Product

KEY = os.environ.get('UWOPENDATA_APIKEY')

def retrieve(service):
    """Request service data from UW Open Data API as JSON HTTPResponse."""
    payload = {'key': KEY}
    url = os.environ.get('API_URL') + service
    resp = requests.get(url, params=payload)
    return resp

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