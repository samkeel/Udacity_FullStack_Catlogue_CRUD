#! /usr/bin/env python2.7

from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   jsonify,
                   flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalogue, Item, Users
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Read and assign client ID generated by google
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "movie_catalogues"


engine = create_engine('sqlite:///movies.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Udacity provided code to connect to Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
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
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Custom User login and ID
    user_id = retrieve_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;' \
              'border-radius: 150px;-webkit-border-radius: ' \
              '150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


"""User login function.
Check to see if user exists by email. If User doesnt exist then create
new user entry and return unique user ID, if user is found return
existing user ID. Store user ID in login_session variable.
"""


def retrieve_user(login_session):
    user = session.query(Users).filter_by(email=login_session['email']).first()
    if user is None:
        # Create new user
        new_user = Users(username=login_session['username'],
                         email=login_session['email'])
        session.add(new_user)
        session.commit()
        # Retrieve new users unique ID
        user = session.query(Users).filter_by(
            email=login_session['email']).first()
        return user.user_id
    else:
        return user.user_id


# Udacity provided code to disconnect from google
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps
                                 ('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %\
          login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("You have been logged out")
        return redirect(url_for('showMain'))
    else:
        flash("You were not logged out")
        return redirect(url_for('showMain'))


# JSON Routing

# JSON route to show category listing in JSON format
@app.route('/categories/JSON')
def categoriesJSON():
    cats = session.query(Catalogue).all()
    return jsonify(Catalogues=[i.serialize for i in cats])


# JSON route to show all items in the database in JSON format
@app.route('/items/JSON')
def itemsJSON():
    movies = session.query(Item).all()
    return jsonify(Movies=[i.serialize for i in movies])


# HTML Routing

# Main page
@app.route('/')
@app.route('/main/')
def showMain():
    side_nav = session.query(Catalogue).all()
    return render_template('main.html', side_nav=side_nav)


# Movie listings for selected genre
@app.route('/subcategory/<int:id>')
def subCat(id):
    side_nav = session.query(Catalogue).all()
    subs = session.query(Item).filter_by(catalogue_id=id).all()
    new_title = session.query(Catalogue).filter_by(cat_id=id).first()
    return render_template('subcat.html', side_nav=side_nav, subs=subs,
                           newtitle=new_title)


# Selected movie summary: including title, description,
# posted user and links to edit.
@app.route('/subcategory/item/<int:id>')
def itemDetails(id):
    if 'username' not in login_session:
        flash('Please login to edit.')
    side_nav = session.query(Catalogue).all()
    subs = session.query(Item).filter_by(item_id=id).first()
    user_post = session.query(Users).filter_by(
        user_id=subs.userpost_id).first()
    return render_template('items.html', side_nav=side_nav,
                           subs=subs, user_post=user_post)


# New movie Genre form
@app.route('/catalogue/new/', methods=['GET', 'POST'])
def newCatalogue():
    if 'username' not in login_session:
        flash('Please login to make new Genre listings.')
    side_nav = session.query(Catalogue).all()
    if request.method == 'POST':
        newCat = Catalogue(cat_name=request.form['usergenre'])
        session.add(newCat)
        session.commit()
        return redirect(url_for('showMain'))
    else:
        return render_template('newCategory.html', side_nav=side_nav)


# Edit item form
@app.route('/subcategory/item/edit/<int:id>', methods=['GET', 'POST'])
def itemEdit(id):
    if 'username' not in login_session:
        flash('Please login to edit.')
        return redirect('/main')
    side_nav = session.query(Catalogue).all()
    itemValue = session.query(Item).filter_by(item_id=id).first()
    if login_session['user_id'] != itemValue.userpost_id:
        flash("Only the items creator can edit the item")
        return redirect('/main')
    if request.method == 'POST':
        if request.form['usergenre']:
            itemValue.catalogue_id = request.form['usergenre']
        if request.form['usersynopsis']:
            itemValue.movie_description = request.form['usersynopsis']
        if request.form['usertitle']:
            itemValue.movie_title = request.form['usertitle']
        session.add(itemValue)
        session.commit()
        return redirect(url_for('itemDetails', id=itemValue.item_id))
    else:
        return render_template('itemedit.html', side_nav=side_nav,
                               item=itemValue)


# Delete an item
@app.route('/subcategory/item/delete/<int:id>', methods=['GET', 'POST'])
def delItem(id):
    if 'username' not in login_session:
        flash('Please login to delete your entries.')
        return redirect('/main')
    side_nav = session.query(Catalogue).all()
    itemToDelete = session.query(Item).filter_by(item_id=id).first()
    if login_session['user_id'] != itemToDelete.userpost_id:
        flash("Only the items creator can delete the item")
        return redirect('/main')
    if request.method == 'GET':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('subCat', id=itemToDelete.catalogue_id))
    else:
        return render_template('itemedit.html', side_nav=side_nav,
                               item=itemToDelete)


# New item form
@app.route('/subcategory/new/', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        flash('Please login to make new movie listings.')
    side_nav = session.query(Catalogue).all()
    if request.method == 'POST':
        newEntry = Item(catalogue_id=request.form['usergenre'],
                        userpost_id=login_session['user_id'],
                        movie_title=request.form['usertitle'],
                        movie_description=request.form['usersynopsis'])
        session.add(newEntry)
        session.commit()
        # Refreshes the form to allow multiple new entries.
        return render_template('newItem.html', side_nav=side_nav)
    else:
        return render_template('newItem.html', side_nav=side_nav)


# Program start
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
app.run(host='0.0.0.0', port=5000)
