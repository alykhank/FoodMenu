#!/usr/bin/env python
import json

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def renderMenu():
	menu = None
	days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	with open('response.txt') as jsonResponseFile:
		menu = json.load(jsonResponseFile)['response']['data']

	foodlist = menu['Restaurants'].values()
	return render_template('index.html', foodlist=foodlist, days=days)

if __name__ == "__main__":
	app.run()
