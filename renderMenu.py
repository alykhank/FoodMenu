#!/usr/bin/env python
import json, os, requests
from awsauth import S3Auth
from datetime import datetime
from pytz import timezone
from flask import Flask, render_template, url_for

app = Flask(__name__)
ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
MIXPANEL_TOKEN = os.environ.get('MIXPANEL_TOKEN')

@app.route('/')
def renderMenu():
	nowWaterloo = datetime.now(timezone('America/Toronto'))
	foodMenu = requests.get('http://s3.amazonaws.com/uwfoodmenu/foodMenu.txt', auth=S3Auth(ACCESS_KEY, SECRET_KEY))
	menu = foodMenu.json()['response']['data']
	serviceInfo = requests.get('http://s3.amazonaws.com/uwfoodmenu/serviceInfo.txt', auth=S3Auth(ACCESS_KEY, SECRET_KEY))
	locations = serviceInfo.json()['response']['data']
	return render_template('index.html', menu=menu, locations=locations, nowWaterloo=nowWaterloo, mixpanelToken=MIXPANEL_TOKEN)

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
