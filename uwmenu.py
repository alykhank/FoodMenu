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
def index():
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

def fulldateformat(value,
                   full_date_format="%Y-%m-%d",
                   friendly_format="{date.day}/{date.month}/{date.year}"):
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

def building_info(outlet_id, locations):
    """Find building name for given outlet ID."""
    for location in locations:
        if location['outlet_id'] == outlet_id:
            return '%s' % location['building']

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    app.debug = os.environ.get('DEBUG')
    app.jinja_env.filters['fulldateformat'] = fulldateformat
    app.jinja_env.filters['dateformat'] = dateformat
    app.jinja_env.filters['timeformat'] = timeformat
    app.jinja_env.filters['building_info'] = building_info
    app.run(host='0.0.0.0', port=PORT)
