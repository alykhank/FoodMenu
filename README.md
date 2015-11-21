# [UW Menu](http://uwmenu.com)

[![Build Status](https://travis-ci.org/alykhank/FoodMenu.svg?branch=master)](https://travis-ci.org/alykhank/FoodMenu)
[![Dependency Status](https://gemnasium.com/alykhank/FoodMenu.svg)](https://gemnasium.com/alykhank/FoodMenu)
[![Coverage Status](https://coveralls.io/repos/alykhank/FoodMenu/badge.svg?branch=master&service=github)](https://coveralls.io/github/alykhank/FoodMenu?branch=master)
[![Code Climate](https://codeclimate.com/github/alykhank/FoodMenu/badges/gpa.svg)](https://codeclimate.com/github/alykhank/FoodMenu)

* See meals for the week at each on-campus eatery, including nutrition facts
* Browse locations and hours for eateries

<img src="img/menu.png" alt="Menu" width="300px">
<img src="img/menuinfo.png" alt="Menu Info" width="300px">

<img src="img/locations.png" alt="Locations" width="300px">
<img src="img/locationinfo.png" alt="Location Info" width="300px">

<img src="img/about.png" alt="About" width="300px">

## Technologies

* Hosted on [Heroku](https://www.heroku.com)
* Retrieves JSON data from the [University of Waterloo Open Data API](https://api.uwaterloo.ca)
* Caches some data using [Redis](http://redis.io)
* Parses and displays data via [Flask](http://flask.pocoo.org) with [Jinja](http://jinja.pocoo.org)
* Uses [jQuery Mobile](https://jquerymobile.com) for interface

## Development

* Prerequisites:
  * Ensure [pip](https://pip.pypa.io/en/stable/), [Virtualenv](https://virtualenv.pypa.io/en/latest/), and [Heroku Toolbelt](https://toolbelt.heroku.com) are installed
  * [Redis](http://redis.io) will be installed via [Homebrew](http://brew.sh) if it is not already
* [Request a key](https://api.uwaterloo.ca/apikey/) for the UW Open Data API

```bash
script/bootstrap
script/run
open http://localhost:5000/
```

## Tests

```bash
script/test
```
