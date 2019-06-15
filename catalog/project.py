# Imports
from flask import Flask, render_template, \
    url_for, request, redirect,\
    flash, jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import *
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os
import random
import string
import datetime
import json
import httplib2
import requests
# Import login_required from login_decorator.py
from login_decorator import login_required

# Flask instance
app = Flask(__name__)


# GConnect CLIENT_ID

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

# Connect to database
engine = create_engine('sqlite:///team.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine
# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Login - Create anti-forgery state token


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# GConnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Gathers data from Google Sign In API and places
    it inside a session variable.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is'
                                            'already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    # data = answer.json()
    data = json.loads(answer.text)
    try:
        login_session['username'] = data['name']
        login_session['picture'] = data['picture']
        login_session['email'] = data['email']
    except psycopg2.OperationalError as e:
        login_session['username'] = "Google User"
        login_session['picture'] = "http://tiny.cc/lz6m2y"
        login_session['email'] = "Google Email"

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    ' -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    try:
        result['status'] == '200'
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = redirect(url_for('showCatalog'))
        flash("You are now logged out.")
        return response
    except Exception as e:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'+e, 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show home page
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    teams = session.query(Team).order_by(asc(Team.name))
    captains = session.query(Captain).order_by(desc(Captain.date))
    if 'username' not in login_session:
        return render_template('publiccatalog.html',
                               teams=teams, captains=captains)
    else:
        return render_template('catalog.html', teams=teams, captains=captains)


# Add a new genre
@app.route('/catalog/newteam', methods=['GET', 'POST'])
@login_required
def newTeam():
    if request.method == 'POST':
        addingTeam = Team(name=request.form['name'],
                            user_id=login_session['user_id'])
        session.add(addingTeam)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newTeam.html')


# Edit a genre
@app.route('/catalog/<team_name>/edit', methods=['GET', 'POST'])
@login_required
def editTeam(team_name):
    teamToEdit = session.query(Team).filter_by(name=team_name).one()

    """Prevent logged-in user to edit other user's genre"""
    if teamToEdit.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert(' You are not authorized"\
                "to edit this genre."\
                "Please create your own " \
               "genre " \
               "in order to edit.');}</script><body onload='myFunction()'>"

    """Save edited genre to the database"""
    if request.method == 'POST':
        teamToEdit.name = request.form['name']
        session.add(teamToEdit)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('editTeam.html', team=teamToEdit)

# Delete a genre


@app.route('/catalog/<team_name>/delete', methods=['GET', 'POST'])
@login_required
def deleteTeam(team_name):
    teamToDelete = session.query(Team).filter_by(name=team_name).one()

    """Prevent logged-in user to delete other user's genre"""
    if teamToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
            "to delete this genre. Please create your own " \
               "genre " \
               "in order to delete.');}</script><body onload='myFunction()'>"

    """Delete genre from the database"""
    if request.method == 'POST':
        session.delete(teamToDelete)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteTeam.html', team=teamToDelete)


# Show all books in a genre
@app.route('/catalog/<team_name>/captains')
def showTeamCaptains(team_name):
    teams = session.query(Team).order_by(asc(Team.name))
    chosenTeam = session.query(Team).filter_by(name=team_name).one()
    captains = session.query(Captain).filter_by(
        team_id=chosenTeam.id).order_by(asc(Captain.name))
    creator = getUserInfo(chosenTeam.user_id)
    if 'username' not in login_session or\
       creator.id != login_session['user_id']:
        return render_template('publicTeamCaptains.html',
                               teams=teams,
                               chosenTeam=chosenTeam,
                               captains=captains)
    else:
        return render_template('showTeamCaptains.html',
                               teams=teams,
                               chosenTeam=chosenTeam,
                               captains=captains)


# Show information of a specific book
@app.route('/catalog/<team_name>/<captain_name>')
def showCaptain(team_name, captain_name):
    team = session.query(Team).filter_by(name=team_name).one()
    captain = session.query(Captain).filter_by(name=captain_name, team=team).one()
    creator = getUserInfo(captain.user_id)
    if 'username' not in login_session or\
       creator.id != login_session['user_id']:
        return render_template('publiccaptains.html', captain=captain)
    else:
        return render_template('showCaptain.html', captain=captain)


# Add a new book
@app.route('/catalog/newcaptain', methods=['GET', 'POST'])
@login_required
def newCaptain():
    teams = session.query(Team).order_by(asc(Team.name))
    if request.method == 'POST':
        addingTeam = Captain(
            name=request.form['name'],
            role=request.form['role'],
            runs=request.form['runs'],
            wickets=request.form['wickets'],
            description=request.form['description'],
            image=request.form['image'],
            team=session.query(
                Team).filter_by(name=request.form['team']).one(),
            date=datetime.datetime.now(),
            user_id=login_session['user_id'])
        session.add(addingTeam)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCaptain.html',
                               teams=teams)

# Edit a book


@app.route('/catalog/<team_name>/<captain_name>/edit', methods=['GET', 'POST'])
@login_required
def editCaptain(team_name, captain_name):
    teams = session.query(Team).order_by(asc(Team.name))
    editingCaptainTeam = session.query(Team).filter_by(name=team_name).one()
    editingCaptain = session.query(Captain).filter_by(
        name=captain_name, team=editingCaptainTeam).one()

    """Prevent logged-in user to edit book which belongs to other user"""
    if editingCaptain.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
                "to edit this book. Please create your own book " \
               "in order to edit.');}</script><body onload='myFunction()'>"

    """Save edited book to the database"""
    if request.method == 'POST':
        if request.form['name']:
            editingCaptain.name = request.form['name']
        if request.form['role']:
            editingCaptain.role = request.form['role']
        if request.form['runs']:
            editingCaptain.runs = request.form['runs']
        if request.form['wickets']:
            editingCaptain.wickets = request.form['wickets']
        if request.form['description']:
            editingCaptain.description = request.form['description']
        if request.form['team']:
            editingCaptain.team = session.query(Team).filter_by(
                name=request.form['team']).one()
        session.add(editingCaptain)
        session.commit()
        return redirect(url_for('showCaptain', team_name=editingCaptainTeam.name,
                                captain_name=editingCaptain.name))
    else:
        return render_template('editCaptain.html', teams=teams,
                               editingCaptainTeam=editingCaptainTeam,
                               captain=editingCaptain)

# Delete a book


@app.route('/catalog/<team_name>/<captain_name>/delete', methods=['GET', 'POST'])
@login_required
def deleteCaptain(team_name, captain_name):
    team = session.query(Team).filter_by(name=team_name).one()
    deletingCaptain = session.query(Captain).filter_by(
        name=captain_name, team=team).one()

    """Prevent logged-in user to delete book which belongs to other user"""
    if deletingCaptain.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
                "to delete this book. Please create your own book " \
               "in order to delete.');}</script><body onload='myFunction()'>"

    """Delete book from the database"""
    if request.method == 'POST':
        session.delete(deletingCaptain)
        session.commit()
        return redirect(url_for('showTeamCaptains', team_name=team.name))
    else:
        return render_template('deleteCaptain.html', captain=deletingCaptain)

# Json End-Points
# API endpoints for all genres and books.


@app.route('/catalog.json')
def catalogJSON():
    teams = session.query(Team).all()
    captains = session.query(Captain).all()
    return jsonify(Teams=[c.serialize for c in teams],
                   captains=[i.serialize for i in captains])

# API endpoints for all genres.


@app.route('/teams.json')
def teamsJSON():
    teams = session.query(Team).all()
    return jsonify(Teams=[c.serialize for c in teams])

# API endpoints for all books of a specific genre.


@app.route('/<team_name>/captains.json')
def captainsJSON(team_name):
    team = session.query(Team).filter_by(name=team_name).one()
    captains = session.query(Captains).filter_by(team=team).all()
    return jsonify(Captains=[i.serialize for i in captains])


if __name__ == '__main__':
    app.secret_key = 'APP_SECRET_KEY'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
