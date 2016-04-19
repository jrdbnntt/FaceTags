facetags
========
See what your friends look like through a computer's eyes.

# Setup
## Requirements
## Server
* python 2.7
* pip
* PostgresSQL 9.5
* api/db keys

## Static Frontend
* node
* npm
```bash
$ sudo npm install -g bower gulp-cli jade
$ cd static/
$ npm install
$ bower install
```


## Installation
```bash
$ sudo apt-get install python-psycopg2 virtualenv
$ pip install Django
$ pip install django-allauth
$ pip install git+git://github.com/Clarifai/clarifai-python.git
```

## Running
I recommend using Atom to edit the static/ and PyCharm to manage the server.

### facetags-server

### facetags-static
Gulp builder for frontend code.
```bash
$ cd static/
$ gulp watch    # Development (watches files)
$ gulp          # Production (compiles once)
```

# Components
* PostgreSQL
* Facebook oauth via [`django-allauth`](http://django-allauth.readthedocs.org/en/latest/overview.html)
* Facebook graph api integration for grabbing pictures
* Clarifi api for tagging pictures


# Project Setup

## Apps
* `accounts` - account management, user setup
* `tagger' -


