#!/usr/bin/env python

"""Serve menu web view and API."""

import json
import os

from datetime import datetime
from pytz import timezone
from flask import render_template, jsonify

from models import app, FoodMenu, Locations

MIXPANEL_TOKEN = os.environ.get('MIXPANEL_TOKEN')

@app.route('/')
def render_menu():
    """Send menu and location data to templates."""
    now_waterloo = datetime.now(timezone('America/Toronto'))
    food_menu = FoodMenu.query.order_by(FoodMenu.id.desc()).first().result
    menu = json.loads(food_menu)['data']
    locations_info = Locations.query.order_by(
        Locations.id.desc()).first().result
    locations = json.loads(locations_info)['data']
    return render_template('index.html',
                           menu=menu,
                           locations=locations,
                           nowWaterloo=now_waterloo,
                           mixpanelToken=MIXPANEL_TOKEN)

@app.route('/menu')
def menu_api():
    """Serve menu data as JSON API."""
    food_menu = FoodMenu.query.order_by(FoodMenu.id.desc()).first().result
    menu = json.loads(food_menu)['data']
    return jsonify(menu)

def datetimeformat(
        value, full_date_format='%Y-%m-%d', month_day_format='%B %d'):
    """Convert datetimes from 'Y-m-d' to 'B d'."""
    value_date = datetime.strptime(value, full_date_format)
    return value_date.strftime(month_day_format)

def building_info(outlet_id, locations):
    """Find building name for given outlet ID."""
    for location in locations:
        if location['outlet_id'] == outlet_id:
            return '%s' % location['building']

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.filters['building_info'] = building_info
    app.run(host='0.0.0.0', port=PORT)
