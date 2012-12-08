#!/usr/bin/env python
import json, os

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def renderMenu():
	menu = None
	days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	with open('response.txt') as jsonResponseFile:
		menu = json.load(jsonResponseFile)['response']['data']

	foodlist = menu['Restaurants'].values()
	return render_template('index.html', menu=menu, foodlist=foodlist, days=days)

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
