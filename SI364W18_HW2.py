## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album_name = StringField('Enter the name of an album:', validators=[Required()])
	button_options = RadioField('How much do you like this album? (1 low, 3 high)', choices = [('1','1'),('2','2'),('3','3')], validators=[Required()])
	submit = SubmitField('Submit')
		



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)
####################################################################################################

@app.route('/artistform')
def artistform():
	return render_template('artistform.html')

@app.route('/artistinfo', methods = ['GET', 'POST'])
def artistinfo():
	artist = request.args.get('artist')
	params = {}
	params['term'] = artist
	params['entity'] = 'musicTrack'
	response = requests.get('https://itunes.apple.com/search', params = params).json()['results']
	songs = []
	for kevin in response:
		songs.append(kevin)
	return render_template('artist_info.html', objects = songs)	

@app.route('/artistlinks')
def artistlinks():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>', methods = ['GET', 'POST'])
def specific_artist(artist_name):
	params = {}
	params['term'] = artist_name
	params['entity'] = 'musicTrack'
	response = requests.get('https://itunes.apple.com/search', params = params).json()['results']
	return render_template('specific_artist.html', results = response)

@app.route('/album_entry')
def album_entry():
	wtform = AlbumEntryForm()
	return render_template('album_entry.html', form = wtform)

@app.route('/album_result', methods = ['GET','POST'])
def album_result():
	form = AlbumEntryForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		album_name = form.album_name.data
		button_options = form.button_options.data
		return render_template('album_data.html', album_name = album_name, button_options = button_options)
		flash('All fields are required!')
	return redirect(url_for('album_entry'))




if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
