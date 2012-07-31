#! /usr/bin/python

# import simplejson, urllib
import json, urllib2, pickle

apiKey = open('apiKey.txt', 'r')
key = apiKey.readline()
apiKey.close()

service = 'FoodMenu'
# output = 'json'
# callback = 'None'
request = 'http://api.uwaterloo.ca/public/v1/'

def getMenu():
    url = request + '?' + 'key=' + key + '&' + 'service=' + service
    result = json.load(urllib2.urlopen(url))
    return result
    
menu = getMenu()
jsonResponseFile = open('response.txt', 'w')
pickle.dump(menu, jsonResponseFile)
jsonResponseFile.close()
