# Fyyur 

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

The goal of this project was to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.


## Overview

The app was nearly complete but was using mock data. 
Models and model interactions have been built to be able to store retrieve, and update data from a database. After finishing all the task , Fyyur is a fully functioning site that is at capable of doing the following, using a PostgreSQL database:

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.


## Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.
  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Change the database settings in `config.py`

5. Navigate to Home page [http://localhost:5000](http://localhost:5000)


## Overall:

* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`

Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new artists, shows, and venues.
* `app.py` -- (Missing functionality.) Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `app.py` -- (Missing functionality.) Defines the data models that set up the database tables.
* `config.py` -- (Missing functionality.) Stores configuration variables and instructions, separate from the main application code. This is where you will need to connect to the database.


## Instructions to qualify

Here it is explained the process followed to complete different tasks and how has been done

### Models

Models can be found in `app.py`.

It has been created a one-to-many relationship between artists and shows and a one-to-many relationship between venues and shows. The table shows also references artists and venues, so once it has obtained a show we can directly get the information about it artist or venue.

Basic fields have been set to `nullable=False` to avoid introducing empty fields when mandatory (i.e. for basic information)


### Controllers

Controllers can be found in `app.py`
All the endpoints needed to solve the requests done by the frontend.

Above each endpoint there is a comment givin clear information about what that controller does


### Forms

Some forms have been completed as they were not incluying all the necessary fields to complete the functionality.
