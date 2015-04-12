# [UW Menu](http://uwmenu.com)

[![Build Status](https://travis-ci.org/alykhank/FoodMenu.svg?branch=master)](https://travis-ci.org/alykhank/FoodMenu)
[![Dependency Status](https://gemnasium.com/alykhank/FoodMenu.svg)](https://gemnasium.com/alykhank/FoodMenu)

## Features

* Displays meals for the week at each on-campus eatery
* Presents information including location and hours for each eatery

<img src="img/menu.png" alt="Menu" width="300px">
<img src="img/menuinfo.png" alt="Menu Info" width="300px">

<img src="img/locations.png" alt="Locations" width="300px">
<img src="img/locationinfo.png" alt="Location Info" width="300px">

<img src="img/about.png" alt="About" width="300px">


## Technologies

* Hosted on [Heroku](http://www.heroku.com/)
* Retrieves JSON data from the [University of Waterloo Open Data API](http://api.uwaterloo.ca/)
* Caches some data using [Redis](http://redis.io)
* Parses and displays data via [Flask](http://flask.pocoo.org/) with [Jinja2](http://jinja.pocoo.org/)
* Uses [jQuery Mobile](http://jquerymobile.com/) for interface


## Usage

* Store [UW Open Data API Key](http://api.uwaterloo.ca/#!/keygen) in `.env`
	* `echo "UWOPENDATA_APIKEY=<KEY>" >> .env`
	* [Local setup instructions](https://devcenter.heroku.com/articles/config-vars#local-setup)
* Use `foreman start` to run application locally and access at [http://localhost:5000/](http://localhost:5000/)
