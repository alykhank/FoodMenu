#!/usr/bin/env python

"""Serve menu web view and API."""

from collections import OrderedDict
from datetime import datetime
import json
import os

from flask import Flask, render_template, jsonify
import redis
import requests

MIXPANEL_TOKEN = os.environ.get("MIXPANEL_TOKEN")
KEY = os.environ.get("UWOPENDATA_APIKEY")
MENU_ENDPOINT = "menu.json"
LOCATIONS_ENDPOINT = "locations.json"
OUTLETS_ENDPOINT = "outlets.json"
PRODUCTS_ENDPOINT = "products/{}.json"
AGGREGATE_MENU = "foodservices"
app = Flask(__name__)
cache = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379"))

def retrieve(service):
    """Request service data from UW Open Data API as JSON HTTPResponse text."""
    resp = cache.get(service)
    if resp is None:
        payload = {"key": KEY}
        url = "https://api.uwaterloo.ca/v2/foodservices/" + service
        resp = requests.get(url, params=payload).text
        cache.set(service, resp, ex=60) # expire after 60 seconds
    return resp

def retrieve_all_outlet_details():
    """Retrieve menu, locations, and outlets data then aggregate into single object."""
    foodservices = cache.get(AGGREGATE_MENU)
    if foodservices:
        foodservices = json.loads(foodservices, object_pairs_hook=OrderedDict)
    else:
        menu = json.loads(retrieve(MENU_ENDPOINT))["data"]
        locations = json.loads(retrieve(LOCATIONS_ENDPOINT))["data"]
        outlets = json.loads(retrieve(OUTLETS_ENDPOINT))["data"]

        foodservices = {}
        eateries = {}
        for eatery in menu["outlets"]:
            eateries[eatery["outlet_id"]] = eatery
        for location in locations:
            if location["outlet_id"] in eateries:
                eateries[location["outlet_id"]]["location"] = location
            else:
                eateries[location["outlet_id"]] = {"outlet_name": location["outlet_name"],
                                                   "location": location}
        for outlet in outlets:
            daily_meals = []
            if outlet["has_breakfast"]: daily_meals += ["Breakfast"]
            if outlet["has_lunch"]: daily_meals += ["Lunch"]
            if outlet["has_dinner"]: daily_meals += ["Dinner"]
            if outlet["outlet_id"] in eateries:
                eateries[outlet["outlet_id"]]["meals"] = daily_meals
            else:
                eateries[outlet["outlet_id"]] = {"outlet_name": outlet["outlet_name"],
                                                 "meals": daily_meals}
        foodservices["date"] = menu["date"]
        foodservices["eateries"] = OrderedDict(sorted(eateries.items(),
                                                      key=lambda t: t[1]["outlet_name"]))
        cache.set(AGGREGATE_MENU, json.dumps(foodservices), ex=60) # expire after 60 seconds
    return foodservices

def attach_filters():
    """Attach Jinja filters to app for use in templates."""
    app.jinja_env.filters["fulldateformat"] = fulldateformat
    app.jinja_env.filters["dateformat"] = dateformat
    app.jinja_env.filters["timeformat"] = timeformat

@app.route("/")
def index():
    """Send menu and location data to templates."""
    foodservices = retrieve_all_outlet_details()
    return render_template("index.html", menu=foodservices, mixpanelToken=MIXPANEL_TOKEN)

@app.route("/product/<int:product_id>/")
def product_info(product_id):
    product = json.loads(retrieve(PRODUCTS_ENDPOINT.format(product_id)))["data"]
    special_attributes = ["product_id", "product_name", "diet_id", "diet_type", "ingredients",
                          "micro_nutrients", "tips", "serving_size", "serving_size_g"]
    return render_template("product.html", product=product, special_attributes=special_attributes)

@app.route("/menu/")
def menu_api():
    """Serve menu data as JSON API."""
    foodservices = retrieve_all_outlet_details()
    return jsonify(foodservices)

def fulldateformat(value,
                   full_date_format="%Y-%m-%d",
                   friendly_format="{date:%b} {date.day} {date.year}"):
    """Convert datetimes from 'Y-m-d' to 'd/m/Y'."""
    date = datetime.strptime(value, full_date_format)
    return friendly_format.format(date=date)
def dateformat(value,
               full_date_format="%Y-%m-%d",
               month_day_format="{date:%B} {date.day}"):
    """Convert datetimes from 'Y-m-d' to 'B d'."""
    date = datetime.strptime(value, full_date_format)
    return month_day_format.format(date=date)

def timeformat(value,
               full_time_format="%H:%M",
               friendly_format="{time:%l}:{time.minute:02} {time:%p}"):
    """Convert datetimes from 'H:M' to 'I:M p'."""
    time = datetime.strptime(value, full_time_format)
    return friendly_format.format(time=time)

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get("PORT", 5000))
    app.debug = os.environ.get("DEBUG")
    attach_filters()
    app.run(host="0.0.0.0", port=PORT)
