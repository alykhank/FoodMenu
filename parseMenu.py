#! /usr/bin/python

import pickle
jsonResponseFile = open('response.txt', 'r')
menu = pickle.load(jsonResponseFile)
data = menu['response']['data']

days = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')

def displayMenu(restaurant, foodlist):
    if foodlist:
        print(restaurant + ':')
        print
        print
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

print
print('This menu is valid from ' + data['Start'] + ' to ' + data['End'] + '.')
print
print
print

for restaurant, foodlist in data['Restaurants'].iteritems():
    displayMenu(restaurant, foodlist)
