#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import sys
import dateutil.parser
import babel
import logging
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///myfyyurdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#  ------->>   Venue  <<-------
class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship("Show", backref="venue", lazy=True)
    

    def __repr__(self):
      return f'<Venue id:{self.id}> name:{self.name}>' 

#  ------->>   artists  <<-------

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship("Show", backref="artist", lazy=True)

    def __repr__(self):
      return f'<Artist id:{self.id}> name:{self.name}>'

#  ------->>   Show  <<-------
class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
      return f'<Show id:{self.id} venue_id:{self.venue_id} artist_id:{self.artist_id}>'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/')
def index():
  return render_template('pages/home.html')

#  ----------------------------------------------------------------
#  /venues , /artists and /shows
#  ----------------------------------------------------------------

#  ------->>   venues  <<-------
@app.route('/venues') 
def venues():
  data = []
  allvenue = db.session.query(Venue.city, Venue.state)
  for venues in allvenue:
    venue_q = Venue.query.filter(Venue.state == venues.state).filter(Venue.city == venues.city).all()
    venue_d = []

    for venue in venue_q:
      venue_d.append({
        'id': venue.id,
        'name': venue.name,
        # 'num_upcoming_shows': len(db.session.query(Show).filter(Show.start_time > datetime.now()).all())
        })
      data.append({
        'city': venues.city,
        'state': venues.state,
        'venues': venue_d
        })
  return render_template('pages/venues.html', areas=data);


#  ------->>   artists  <<-------
@app.route('/artists') 
def artists():
  data=[]
  allartist = db.session.query(Artist.id, Artist.name)
  for artist in allartist:
    data.append({
      "id": artist.id,
      "name": artist.name
      })

  return render_template('pages/artists.html', artists=data)

#  ------->>   shows  <<-------
@app.route('/shows') 
def shows():
  data=[]
  allshow =  db.session.query(Show).join(Artist).join(Venue).all()
  for theshow in allshow:
    data.append({
      "venue_id": theshow.venue_id,
      "venue_name": theshow.venue.name,
      "artist_id": theshow.artist_id,
      "artist_name": theshow.artist.name,
      "artist_image_link": theshow.artist.image_link,
      "start_time": theshow.start_time.strftime("%m/%d/%Y")
      })
  return render_template('pages/shows.html', shows=data)

#  ----------------------------------------------------------------
#                        search 
#  ----------------------------------------------------------------

#  ------->>   venues  <<-------
@app.route('/venues/search', methods=['POST']) 
def search_venues():
  search_term = request.form.get('search_term', '')
  search_venues = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []
  for thevenue in search_venues:
    data.append({
      "id": thevenue.id,
      "name": thevenue.name,
      "numshows": len(db.session.query(Show).filter(Show.start_time > datetime.now()).all())
    })
  response={
    "count": len(search_venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

#  ------->>   artists  <<-------

@app.route('/artists/search', methods=['POST']) 
def search_artists():
  search_term = request.form.get('search_term', '')
  search_venues = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []
  for thevenue in search_venues:
    data.append({
      "id": thevenue.id,
      "name": thevenue.name,
      "numshows": len(db.session.query(Show).filter(Show.start_time > datetime.now()).all())
      # "num_upcoming_shows": len(db.session.query(Show).filter(Show.artist_id == thevenue.id).all()),
    })
  response={
    "count": len(search_venues),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


#  ----------------------------------------------------------------
#                /......./<int:venue_id> 
#  ----------------------------------------------------------------

#  ------->>   venues  <<-------
@app.route('/venues/<int:venue_id>')  
def show_venue(venue_id):
  thevenue = Venue.query.get(venue_id)
  past_shows= []
  upcoming_shows = []
  now_date = datetime.now()
  for show in thevenue.shows:
    artist_at_show = db.session.query(Artist.id, Artist.name, Artist.image_link).filter_by(id = show.artist_id).first()
    if show.start_time < now_date:
      past_shows.append({
        'artist_id': artist_at_show.id,
        'artist_name': artist_at_show.name, 
        'artist_image_link':artist_at_show.image_link,
        'start_time': show.start_time.strftime('%m/%d/%Y')
          })
    elif show.start_time > now_date:
      upcoming_shows.append ({
        'artist_id': artist_at_show.id,
        'artist_name': artist_at_show.name, 
        'artist_image_link': artist_at_show.image_link,
        'start_time': show.start_time.strftime('%m/%d/%Y')
        })
  data = {
    'id': thevenue.id,
    'name': thevenue.name ,
    'address': thevenue.address,
    'city': thevenue.city,
    'state': thevenue.state,
    'phone': thevenue.phone,
    'facebook_link': thevenue.facebook_link,
    'image_link': thevenue.image_link,
    'past_shows': past_shows,
    'past_shows_count' : len(past_shows),
    'upcoming_shows' : upcoming_shows,
    'upcoming_shows_count' : len(upcoming_shows),
    }
  return render_template('pages/show_venue.html', venue=data)


#  ------->>   artists  <<-------
@app.route('/artists/<int:artist_id>')  
def show_artist(artist_id):
  thevenue = Artist.query.get(artist_id)
  past_shows= []
  upcoming_shows = []
  now_date = datetime.now()
  for show in thevenue.shows:
    artist_at_show = db.session.query(Venue.id, Venue.name, Venue.image_link).filter_by(id = show.venue_id).first()
    if show.start_time < now_date:
      past_shows.append({
        'venue_id': artist_at_show.id,
        'venue_name': artist_at_show.name, 
        'venue_image_link': artist_at_show.image_link,
        'start_time': show.start_time.strftime('%m/%d/%Y')
          })
    elif show.start_time > now_date:
      upcoming_shows.append ({
        'venue_id': artist_at_show.id,
        'venue_name': artist_at_show.name, 
        'venue_image_link': artist_at_show.image_link,
        'start_time': show.start_time.strftime('%m/%d/%Y')
        })
  data = {
    'id': thevenue.id,
    'name': thevenue.name ,
    'city': thevenue.city,
    'state': thevenue.state,
    'phone': thevenue.phone,
    'facebook_link': thevenue.facebook_link,
    'image_link': thevenue.image_link,
    'past_shows': past_shows,
    'past_shows_count' : len(past_shows),
    'upcoming_shows' : upcoming_shows,
    'upcoming_shows_count' : len(upcoming_shows),
    }
  return render_template('pages/show_artist.html', artist=data)


#  ----------------------------------------------------------------
#  Create
#  ----------------------------------------------------------------

#  ------->>   venues  <<-------
@app.route('/venues/create', methods=['GET']) 
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST']) 
def create_venue_submission():
  error = False
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  facebook_link = request.form['facebook_link']
  venue = Venue(
    name=name, 
    city=city, 
    state=state, 
    address=address, 
    phone=phone, 
    facebook_link=facebook_link, 
    )
  try:
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    error = True
    db.session.rollback()
    flash('unsuccessfully', sys.exc_info())
  finally:
    db.session.close()
    return render_template('pages/home.html')

#  ------->>   artists  <<-------

@app.route('/artists/create', methods=['GET']) 
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)
@app.route('/artists/create', methods=['POST']) 
def create_artist_submission():
  error = False
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  facebook_link = request.form['facebook_link']
  artist = Artist(
    name=name,
    city=city,
    state=state,
    phone=phone, 
    facebook_link=facebook_link, 
    )
  try:
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    error = True
    db.session.rollback()
    flash('unsuccessfully', sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  ------->>   shows  <<-------

@app.route('/shows/create') 
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)
@app.route('/shows/create', methods=['POST']) 
def create_show_submission():
  error = False
  venue = request.form['venue_id']
  artist = request.form['artist_id']
  start_time = request.form['start_time']
  show = Show(
    venue_id=venue,
    artist_id=artist,
    start_time=start_time 
    )
  try:
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    error = True
    db.session.rollback()
    flash('unsuccessfully', sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

#  ----------------------------------------------------------------
#  Update
#  ----------------------------------------------------------------

#  ------->>   artists  <<-------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist={
    "id": artist_id,
    "name": artist.name,
    "city": artist.citys,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
    }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST']) 
def edit_artist_submission(artist_id):
  error = False
  the_artist = Artist.query.get(artist_id)
  try:
    the_artist.name = request.form['name']
    the_artist.city = request.form['city']
    the_artist.state = request.form['state']
    the_artist.phone = request.form['phone']
    the_artist.facebook_link = request.form['facebook_link']
    db.session.commit()
    flash('successfully')
  except:
    error = True 
    db.session.rollback()
    flash(f'unsuccessfully', sys.exc_info())
  finally: 
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

#  ------->>   venues  <<-------

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  venue={
    "id": venue_id,
    "name": venue.name,
    "address": venue.address,
    "city": venue.citys,
    "state": venue.state,
    "phone": venue.phone,
    "facebook_link": venue.facebook_link,
    "image_link": venue.image_link,
    }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST']) 
def edit_venue_submission(venue_id):
  error = False  
  venue = Venue.query.get(venue_id)
  try:
    venue.name = request.form['name'],
    venue.address = request.form['address']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']   
    venue.facebook_link = request.form['facebook_link']
    db.session.commit()
    flash('success')
  except:
    error = True
    db.session.rollback()
    flash(f'Error.', sys.exc_info())
  finally: 
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))



#----------------------------------------------------------------
# DELETE
#----------------------------------------------------------------

@app.route('/venues/<venue_id>', methods=['DELETE']) 
def delete_venue(venue_id):
  error = False 
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('successfully deleted!')
  except:
    error = True
    db.session.rollback()
    flash('unsuccessfully deleted!')
  finally:
    db.session.close()
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#

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
