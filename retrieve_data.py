#!/usr/bin/env python

"""Retrieve Menu and Locations from UW Open Data API and store in DB."""

from datetime import datetime
import json
import os

import requests

from models import db
from models import FoodMenu, Locations, Response, Outlet, Menu, Meals, Product

KEY = os.environ.get('UWOPENDATA_APIKEY')

def retrieve(service):
    """Request service data from UW Open Data API as JSON HTTPResponse."""
    payload = {'key': KEY}
    url = os.environ.get('API_URL') + service
    resp = requests.get(url, params=payload)
    return resp

def main():
    """Retrieve menu and location data, store in database."""
    FOOD_MENU = retrieve('menu.json').text
    FOOD_MENU_DATA = FoodMenu(FOOD_MENU)
    LOCATIONS = retrieve('locations.json').text
    LOCATIONS_DATA = Locations(LOCATIONS)
    db.session.add(FOOD_MENU_DATA)
    db.session.add(LOCATIONS_DATA)

    DATA = json.loads(FOOD_MENU)['data']
    NOW = datetime.now()
    OUTLETS = []
    for o in DATA['outlets']:
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
        OUTLETS.append(outlet)
        db.session.add(outlet)
    RESPONSE = Response(
        date=NOW,
        week=DATA['date']['week'],
        year=DATA['date']['year'],
        start=DATA['date']['start'],
        end=DATA['date']['end'],
        outlets=OUTLETS
    )
    db.session.add(RESPONSE)

    db.session.commit()

if __name__ == "__main__":
    main()
