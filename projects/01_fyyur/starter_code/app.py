#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect
from flask import url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import distinct, text
from datetime import datetime
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# connect to a local postgresql database - DONE in config.py

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, default=False, nullable=True)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship('Show', back_populates="venue")


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, default=False, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', back_populates="artist")


class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  start_time = db.Column(db.String(), nullable=False)
  artist = db.relationship("Artist", back_populates="shows")
  venue = db.relationship("Venue", back_populates="shows")


# DONE: implement any missing fields, as a database migration using Flask-Migrate
# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

# returns all the venues grouped by areas
@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.

  areas = []
  sql = text('select city, state FROM venue GROUP BY city, state ORDER BY city')
  result = db.engine.execute(sql)
  cityAndState = result.fetchone()
  while cityAndState is not None:
    currentArea = {}
    currentArea["city"] = city = cityAndState[0]
    currentArea["state"] = state = cityAndState[1]
    
    venues = []
    venuesInArea = Venue.query.filter_by(city=city, state=state).all()
    for venue in venuesInArea:
      currentVenue = {}
      currentVenue["id"] = venue.id
      currentVenue["name"] = venue.name
      num_upcoming_shows=0
      for show in venue.shows:
        if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
          num_upcoming_shows = num_upcoming_shows + 1
      currentVenue["num_upcoming_shows"] = num_upcoming_shows
      venues.append(currentVenue)
    
    currentArea["venues"] = venues
    areas.append(currentArea)
    cityAndState = result.fetchone()

  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  return render_template('pages/venues.html', areas=areas)


# Returns all the venues which name contains the search term passed in the body request
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  searchTerm = request.form['search_term']
  if searchTerm:
    venues = Venue.query.filter(Venue.name.ilike('%'+searchTerm+'%')).all()
  else:
    venues = Venue.query.all()

  response={}
  response["count"]=len(venues);
  data = []
  for venue in venues:
    currentVenue = {}
    currentVenue["id"]=venue.id
    currentVenue["name"]=venue.name
    num_upcoming_shows=0
    for show in venue.shows:
      if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
        num_upcoming_shows = num_upcoming_shows + 1
    currentVenue["num_upcoming_shows"] = num_upcoming_shows
    data.append(currentVenue)
 
  response["data"]=data

  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


# Returns the venue with the id indicated in the request
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.get(venue_id)
  
  if venue is None:
    return redirect(url_for('venues'))

  data={}
  data["id"]=venue.id
  data["name"]=venue.name
  data["genres"]=venue.genres
  data["address"]=venue.address
  data["city"]=venue.city
  data["state"]=venue.state
  data["phone"]=venue.phone
  data["website"]=venue.website
  data["facebook_link"]=venue.facebook_link
  data["seeking_talent"]=venue.seeking_talent
  data["seeking_description"]=venue.seeking_description
  data["image_link"]=venue.image_link

  upcoming_shows_count=0
  past_shows_count=0
  upcoming_shows = []
  past_shows = []
  for show in venue.shows:
    current_show = {}
    current_show['artist_id'] = show.artist_id
    current_show['artist_name'] = show.artist.name
    current_show['artist_image_link'] = show.artist.image_link
    current_show['start_time'] = show.start_time
    if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
      upcoming_shows_count = upcoming_shows_count + 1
      upcoming_shows.append(current_show)
    else:
      past_shows_count = past_shows_count + 1
      past_shows.append(current_show)

  data["upcoming_shows_count"] = upcoming_shows_count
  data["past_shows_count"] = past_shows_count
  data["past_shows"] = past_shows
  data["upcoming_shows"] = upcoming_shows

  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

# Returns the form to create a new venue 
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

# Creates a venue with the information indicated in the form 
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db

  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    website= request.form['website']
    image_link = request.form['image_link']
    if 'seeking_talent' not in request.form:
      seeking_talent = False
      seeking_description = None
    else:
      seeking_talent = True
      seeking_description = request.form['seeking_description']
    
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone,
    facebook_link=facebook_link, genres=genres, website=website, image_link=image_link,
    seeking_talent=seeking_talent, seeking_description=seeking_description)

    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
      db.session.close()
  if error:
    flash('An error occurred. Venue ' + name + ' could not be listed.')
  else:
    # on successful db insert, flash success
    #flash('Venue ' + request.form['name'] + ' was successfully listed!')
    flash('Venue ' + name + ' was successfully listed!')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
  return render_template('pages/home.html')
  
  # DONE: on unsuccessful db insert, flash an error instead.
  

# Deletes the venue with the id given in the request
@app.route('/venues/<venue_id>', methods=['DELETE'])
# @app.route('/venues/delete/<venue_id>')
def delete_venue(venue_id):
  # DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  error = False
  try:
    venue = Venue.query.filter_by(id=venue_id).one_or_none()
    db.session.delete(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
      db.session.close()
  if error:
    abort(400)
    # flash('An error occurred. Venue with id ' + venue_id + ' could not be deleted.')
  else:
    return jsonify({ 'success': True })
    # flash('Venue with id ' + venue_id + ' was successfully deleted!')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
  # DONE BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  # return redirect(url_for('venues'))
  


#  Artists
#  ----------------------------------------------------------------

# return all the artists
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database

  artists = Artist.query.all();

  data = []
  for currentArtist in artists:
    artist = {}
    artist["id"]=currentArtist.id
    artist["name"]=currentArtist.name
    num_upcoming_shows=0
    for show in currentArtist.shows:
      if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
        num_upcoming_shows = num_upcoming_shows + 1
    artist["num_upcoming_shows"] = num_upcoming_shows
    data.append(artist)

  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=data)

# return all the artist which name is contained in the search term
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  searchTerm = request.form['search_term']
  if searchTerm:
    artists = Artist.query.filter(Artist.name.ilike('%'+searchTerm+'%')).all()
  else:
    artists = Artist.query.all()

  response={}
  response["count"]=len(artists);
  data = []
  
  for artist in artists:
    currentArtist = {}
    currentArtist["id"]=artist.id
    currentArtist["name"]=artist.name
    num_upcoming_shows=0
    for show in artist.shows:
      if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
        num_upcoming_shows = num_upcoming_shows + 1
    currentArtist["num_upcoming_shows"] = num_upcoming_shows
    data.append(currentArtist)
 
  response["data"]=data

  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


# returns the artist with the id indicated in the route
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id

  artist = Artist.query.get(artist_id)

  data = {}
  data["id"]=artist.id
  data["name"]=artist.name
  data["genres"]=artist.genres
  data["city"]=artist.city
  data["state"]=artist.state
  data["website"]=artist.website
  data["facebook_link"]=artist.facebook_link
  data["seeking_venue"]=artist.seeking_venue
  data["seeking_description"]=artist.seeking_description
  data["phone"]=artist.phone
  data["image_link"]=artist.image_link

  upcoming_shows_count=0
  past_shows_count=0
  upcoming_shows = []
  past_shows = []
  for show in artist.shows:
    current_show = {}
    current_show['venue_id'] = show.venue_id
    current_show['venue_name'] = show.venue.name
    current_show['venue_image_link'] = show.venue.image_link
    current_show['start_time'] = show.start_time
    if datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
      upcoming_shows_count = upcoming_shows_count + 1
      upcoming_shows.append(current_show)
    else:
      past_shows_count = past_shows_count + 1
      past_shows.append(current_show)

  data["upcoming_shows_count"] = upcoming_shows_count
  data["past_shows_count"] = past_shows_count
  data["past_shows"] = past_shows
  data["upcoming_shows"] = upcoming_shows

  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------

# returns the data to show the form to edit the artist with the id indicated in the request
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  artist = Artist.query.get(artist_id)
  
  form = ArtistForm()

  genresString = ""
  for genre in artist.genres:
    genresString += genre + ","

  form.genres.data = genresString
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)


# edit the artist with the id indicated with the data received from the edit form
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    website= request.form['website']
    image_link = request.form['image_link']
    if 'seeking_venue' not in request.form:
      seeking_venue = False
      seeking_description = None
    else:
      seeking_venue = True
      seeking_description = request.form['seeking_description']

    artist = Artist.query.get(artist_id)
    artist.name=name
    artist.city=city
    artist.state=state
    artist.phone=phone
    artist.facebook_link=facebook_link
    artist.genres=genres
    artist.website=website
    artist.image_link=image_link
    artist.seeking_venue=seeking_venue
    artist.seeking_description=seeking_description

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
      db.session.close()
  if error:
    flash('An error occurred. Artist ' + name + ' could not be edited.')
  else:
    # on successful db insert, flash success
    #flash('Venue ' + request.form['name'] + ' was successfully listed!')
    flash('Artist ' + name + ' was successfully edited!')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


  return redirect(url_for('show_artist', artist_id=artist_id))


# returns the info of the venue so it can be edited in a form
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = Venue.query.get(venue_id)
  
  genresString = ""
  for genre in venue.genres:
    genresString += genre + ","

  form.genres.data = genresString
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)


# takes the info of the venue inserted in the form to edit such artist
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    website= request.form['website']
    image_link = request.form['image_link']
    if 'seeking_talent' not in request.form:
      seeking_talent = False
      seeking_description = ""
    else:
      seeking_talent = True
      seeking_description = request.form['seeking_description']

    venue = Venue.query.get(venue_id)
    venue.name=name
    venue.address=address
    venue.city=city
    venue.state=state
    venue.phone=phone
    venue.facebook_link=facebook_link
    venue.genres=genres
    venue.website=website
    venue.image_link=image_link
    venue.seeking_talent=seeking_talent
    venue.seeking_description=seeking_description

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
      db.session.close()
  if error:
    flash('An error occurred. Venue ' + name + ' could not be edited.')
  else:
    # on successful db insert, flash success
    #flash('Venue ' + request.form['name'] + ' was successfully listed!')
    flash('Venue ' + name + ' was successfully edited!')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

# shows the form to create a new artist
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


# get the data from the form and create an artist with that information
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion

  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    website= request.form['website']
    image_link = request.form['image_link']
    if 'seeking_venue' not in request.form:
      seeking_venue = False
      seeking_description = ""
    else:
      seeking_venue = True
      seeking_description = request.form['seeking_description']

    
    artist = Artist(name=name, city=city, state=state, phone=phone,
    facebook_link=facebook_link, genres=genres, website=website, image_link=image_link,
    seeking_venue=seeking_venue, seeking_description=seeking_description)

    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
      db.session.close()
  if error:
    flash('An error occurred. Artist ' + name + ' could not be listed.')
  else:
    # on successful db insert, flash success
    #flash('Venue ' + request.form['name'] + ' was successfully listed!')
    flash('Artist ' + name + ' was successfully listed!')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

# returns all shows
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.

  shows = Show.query.all();

  data = []
  for show in shows:
    currentShow = {}
    currentShow["venue_id"]=show.venue_id
    currentShow["venue_name"]=show.venue.name
    currentShow["artist_id"]=show.artist_id
    currentShow["artist_name"]=show.artist.name
    currentShow["artist_image_link"]=show.artist.image_link
    currentShow["start_time"]=show.start_time
    data.append(currentShow)

  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=data)


# shows the form to create a new show
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


# get the data from the form to create a new show and insert it in the database
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead

  artist_id = request.form["artist_id"]
  venue_id = request.form["venue_id"]
  start_time = request.form["start_time"]
  artist = Artist.query.get(artist_id)
  venue = Venue.query.get(venue_id)

  print(artist)
  if artist is None or venue is None:
    flash('There was an error!')
  else:
    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time, artist=artist, venue=venue)
    db.session.add(show)
    db.session.commit()
    flash('Show was created succesfully!')

  # on successful db insert, flash success
  
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
