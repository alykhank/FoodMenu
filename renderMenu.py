#!/usr/bin/env python
import json, os
from datetime import datetime, timedelta
from pytz import timezone

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def renderMenu():
	menu = None
	waterlooTimezone = timezone('America/Toronto')
	nowWaterloo = datetime.now(waterlooTimezone)
	currentDatetime = nowWaterloo.strftime('%I:%M %p on %A, %B %d, %Y')
	with open('response.txt') as jsonResponseFile:
		menu = json.load(jsonResponseFile)['response']['data']

	foodlist = menu['Restaurants'].values()
	return render_template('index.html', menu=menu, foodlist=foodlist, nowWaterloo=nowWaterloo, currentDatetime=currentDatetime)

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
