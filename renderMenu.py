#!/usr/bin/env python
import json, os, requests
from awsauth import S3Auth
from datetime import datetime
from pytz import timezone
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def renderMenu():
	nowWaterloo = datetime.now(timezone('America/Toronto'))
	currentDatetime = nowWaterloo.strftime('%I:%M %p on %a, %b %d')
	ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
	SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
	MIXPANEL_TOKEN = os.environ.get('MIXPANEL_TOKEN')
	r = requests.get('http://s3.amazonaws.com/uwfoodmenu/response.txt', auth=S3Auth(ACCESS_KEY, SECRET_KEY))
	menu = r.json()['response']['data']
	return render_template('index.html', menu=menu, nowWaterloo=nowWaterloo, currentDatetime=currentDatetime, mixpanelToken=MIXPANEL_TOKEN)

if __name__ == "__main__":
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
