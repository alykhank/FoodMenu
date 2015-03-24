#!/usr/bin/env python

"""Serve menu web view and API."""

from datetime import datetime
import json
import os

from flask import Flask, render_template, jsonify
import redis
import requests

MIXPANEL_TOKEN = os.environ.get('MIXPANEL_TOKEN')
KEY = os.environ.get('UWOPENDATA_APIKEY')
app = Flask(__name__)
cache = redis.from_url(os.environ.get('REDISTOGO_URL', 'redis://localhost:6379'))

def retrieve(service):
    """Request service data from UW Open Data API as JSON HTTPResponse text."""
    resp = cache.get(service)
    if resp is None:
        payload = {"key": KEY}
        url = "https://api.uwaterloo.ca/v2/foodservices/" + service
        resp = requests.get(url, params=payload).text
        cache.setex(service, resp, 60) # expire cached value after 60 seconds
    return resp

def attach_filters():
    """Attach Jinja filters to app for use in templates."""
    app.jinja_env.filters['fulldateformat'] = fulldateformat
    app.jinja_env.filters['dateformat'] = dateformat
    app.jinja_env.filters['timeformat'] = timeformat

@app.route('/')
def index():
    """Send menu and location data to templates."""
    menu = json.loads(retrieve('menu.json'))['data']
    locations = json.loads(retrieve('locations.json'))['data']
    outlets = json.loads(retrieve('outlets.json'))['data']
    for eatery in menu['outlets']:
        for location in locations:
            if eatery['outlet_id'] == location['outlet_id']:
                eatery['location'] = location
        for outlet in outlets:
            if eatery['outlet_id'] == outlet['outlet_id']:
                daily_meals = []
                if outlet['has_breakfast']: daily_meals += ['Breakfast']
                if outlet['has_lunch']: daily_meals += ['Lunch']
                if outlet['has_dinner']: daily_meals += ['Dinner']
                eatery['meals'] = daily_meals
    return render_template('index.html', menu=menu, mixpanelToken=MIXPANEL_TOKEN)

@app.route('/menu')
def menu_api():
    """Serve menu data as JSON API."""
    menu = json.loads(retrieve('menu.json'))['data']
    return jsonify(menu)

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
    PORT = int(os.environ.get('PORT', 5000))
    app.debug = os.environ.get('DEBUG')
    attach_filters()
    app.run(host='0.0.0.0', port=PORT)
