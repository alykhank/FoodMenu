#!/usr/bin/env python
import json, os, requests
from awsauth import S3Auth

key = os.environ.get('UWOPENDATA_APIKEY')
service = 'FoodMenu'

def getMenu():
	payload = {'key': key, 'service': service}
	r = requests.get('http://api.uwaterloo.ca/public/v1/', params=payload)
	return r.text

menu = getMenu()
ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
requests.put('http://s3.amazonaws.com/uwfoodmenu/response.txt', data=menu, auth=S3Auth(ACCESS_KEY, SECRET_KEY))
