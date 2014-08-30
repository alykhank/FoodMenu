# [UW Menu](http://uwmenu.alykhan.com)

[![Build Status](https://travis-ci.org/alykhank/FoodMenu.svg?branch=master)](https://travis-ci.org/alykhank/FoodMenu)
[![Dependency Status](https://gemnasium.com/alykhank/FoodMenu.svg)](https://gemnasium.com/alykhank/FoodMenu)

## Features

* Displays meals for the week at each on-campus eatery
* Presents information including location and hours for each eatery

![Menu](img/menu.png) ![Menu Info](img/menuinfo.png)
![Locations](img/locations.png)![Location Info](img/locationinfo.png)
![About](img/about.png)


## Technologies

* Hosted on [Heroku](http://www.heroku.com/), uses [Scheduler addon](https://addons.heroku.com/scheduler) to retrieve data daily
* Retrieves JSON data from the [University of Waterloo Open Data API](http://api.uwaterloo.ca/)
* Stores response in [PostgreSQL](https://addons.heroku.com/heroku-postgresql) database
* Parses and displays data via [Flask](http://flask.pocoo.org/) with [Jinja2](http://jinja.pocoo.org/)
* Uses [jQuery Mobile](http://jquerymobile.com/) for interface


## Usage

* Store [UW Open Data API Key](http://api.uwaterloo.ca/#!/keygen) and database URL in `.env`
	* [Local setup instructions](https://devcenter.heroku.com/articles/config-vars#local-setup)
	* Use `foreman run python retrieveData.py` to request data and store in database
* Use `foreman start` to run application locally and access at [http://localhost:5000/](http://localhost:5000/)
