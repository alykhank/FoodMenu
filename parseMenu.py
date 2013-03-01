#!/usr/bin/env python
import json, os, requests
from awsauth import S3Auth

def displayMenu(restaurant, foodlist):
	if foodlist and 'Menu' in foodlist:
		print(restaurant + ':')
		print
		print
		days = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
		for day in days:
			if day in foodlist['Menu'].keys():
				print('    ' + day + ':')
				print
				for meal, itemlist in foodlist['Menu'][day].iteritems():
					print('        ' + meal + ':')
					if type(itemlist['Items']['result']) == list:
						for item in itemlist['Items']['result']:
							print('        ' + item)
					else:
						print('        ' + itemlist['Items']['result'])
					print
				print

if __name__ == "__main__":
	ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
	SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
	r = requests.get('http://s3.amazonaws.com/uwfoodmenu/response.txt', auth=S3Auth(ACCESS_KEY, SECRET_KEY))
	menu = r.json()['response']['data']
	for restaurant, foodlist in menu['Restaurants'].iteritems():
		displayMenu(restaurant, foodlist)
	print
	print('This menu is valid from ' + menu['Start'] + ' to ' + menu['End'] + '.')
	print
	print
	# print json.dumps(menu, indent=4)
