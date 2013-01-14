#!/usr/bin/env python

import json, os, requests
from awsauth import S3Auth

key = os.environ['UWOPENDATA_APIKEY']

service = 'FoodMenu'
# output = 'json'
# callback = 'None'
request = 'http://api.uwaterloo.ca/public/v1/'

def getMenu():
	url = request + '?' + 'key=' + key + '&' + 'service=' + service
	result = requests.get(url).text
	return result

menu = getMenu()
ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
requests.put('http://s3.amazonaws.com/uwfoodmenu/response.txt', data=menu, auth=S3Auth(ACCESS_KEY, SECRET_KEY))
