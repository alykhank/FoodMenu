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

* Hosted on [Heroku](https://www.heroku.com)
* Retrieves JSON data from the [University of Waterloo Open Data API](http://api.uwaterloo.ca)
* Caches some data using [Redis](http://redis.io)
* Parses and displays data via [Flask](http://flask.pocoo.org) with [Jinja](http://jinja.pocoo.org)
* Uses [jQuery Mobile](http://jquerymobile.com) for interface


## Development

Prerequisites: Ensure pip, Virtualenv, and [Foreman](https://devcenter.heroku.com/articles/config-vars#local-setup) are installed. Redis will be installed via Homebrew if it is not already.
Request a key for the [University of Waterloo Open Data API](http://api.uwaterloo.ca/apikey/).
`script/bootstrap`
`script/run`
`open http://localhost:5000/`

## Tests

`script/test`
