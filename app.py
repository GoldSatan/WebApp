# ---------------------------------------------------------------------- #
# The main file of the Python type, from which the entire                #
# functionality will proceed and which will actually                     #
# launch our site with the python -m flask run command in the terminal.  #
# ---------------------------------------------------------------------- #
# Here we will use the flask_sqlalchemy module                           #
# to create tables for our database.                                     #
# Decorators will be created to navigate through our pages.              #
# ---------------------------------------------------------------------- #

# linked libraries and modules
from datetime import datetime
from flask import Flask, render_template
from flask import request, redirect, url_for
from flask import flash, abort, session
import pymysql
from flask_sqlalchemy import SQLAlchemy

from parseBots.create_select import main as m

# connect to mysql using flask_sqlalchemy

conn = 'mysql+pymysql://root:0000@localhost/our_users'

# main flask variable and its settings for the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'abcdefg'


db = SQLAlchemy(app)

# DB - table 
# Table:
# id    title    type_transport   Color      Transmission            Mileage   Occasion   Price   Image     Engine      Note
#  1    1        Some             red        Manual / Mechanics      100       full       1000    ...       ...         ...
#  2    2        Some2            black      Manual                  200       front      2000    ...       ...         ...
#  3    3        Some3            green      Mechanics               300       rear       3000    ...       ...         ...
class Item(db.Model):   
    id = db.Column(db.Integer, primary_key = True,autoincrement=True) 
    title = db.Column(db.String(100))
    type_transport = db.Column(db.String(30))
    color = db.Column(db.String(15))
    transmission = db.Column(db.String(30))
    mileage = db.Column(db.Integer)
    occasion = db.Column(db.String(30))
    price = db.Column(db.String(20))
    image = db.Column(db.Text)
    engine = db.Column(db.String(50))
    note = db.Column(db.Text)

    def __repr__(self):
        return self.title

# table for old 
class Users(db.Model):
    
    # primary_key for Users table
    id = db.Column(db.Integer, primary_key = True) 
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Cascading change of tables Users and Profiles
    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f'<users {self.id}>'
 
# table for newly created users
class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(50), nullable=False)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    # ForeignKey for Users table 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<profiles {self.id}>'

# the start-page 
@app.route('/')
def index():
    return render_template('index.html')

# main serch page where the search will be performed
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "POST":

        # Sorting and filtering options from 
        # the form if the search button has been clicked
        type_ = request.form['type_search']
        sort = request.form['sorting']

        # Selection of elements is carried out by type filtering and sorting
        if type_ != '0' and sort != '0':
            return render_template('search.html', tables=m(f"SELECT * FROM item WHERE type_transport='{type_}' ORDER BY {sort};"))
        
        # Selection of elements is carried out by type filtering
        if type_ != '0' and sort == '0':
            return render_template('search.html', tables=m(f"SELECT * FROM item WHERE type_transport='{type_}';"))
        
        # Selection of elements is carried out by sorting
        if type_ == '0' and sort != '0':
            return render_template('search.html', tables=m(f"SELECT * FROM item  ORDER BY {sort};"))

    # The button was not pressed, so we return it without filtering and sorting
    return render_template('search.html', tables=m("SELECT * FROM item"))


# A registration page that will accept form values
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        if len(request.form['name']) > 2:
            
            try:  
                # creating an entry in the table Users  
                u = Users(email=request.form['email'], psw=request.form['psw']) 
                # add record ib session
                db.session.add(u)     
                db.session.flush()

                # creating an entry in the table Profiles
                p = Profiles(name=request.form['name'], old=request.form['old'],
                            city=request.form['city'], user_id=u.id)
                # add record ib session
                db.session.add(p)
                db.session.commit()

            except:
                # If an error occurred, 
                # we return the session and display an error message
                db.session.rollback()
                print("Error add in DATABASE")

    return render_template('register.html')


# the page on which we will add new transport to the database
@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        if len(request.form['title']) > 2:
            # flash message about the successful submission of the form
            flash('Form submit successfully!', category='success')
        else:
            # flash message about unsuccessful form submission
            flash('Submiting error', category='error')

        # variables from form fields
        title = request.form['title']
        type_transport= request.form['type_transport']
        color = request.form['color']
        transmission = request.form['transmission']
        mileage = request.form['mileage']
        occasion = request.form['occasion']
        price = request.form['price']
        image = request.form['image']
        engine = request.form['engine']
        note = request.form['note']

        try:
            # creating an element for the table Item
            item = Item(title=title, type_transport=type_transport,color=color, transmission=transmission,mileage=mileage,occasion=occasion, price=price, image=image, engine=engine, note=note)
            # add to session
            db.session.add(item)
            db.session.commit()
            
            return redirect('/')

        except:
            # if not added to the session, we display an error message
            print('Very long traceback')
        
    return render_template('create.html')

# page of your chosen transport
@app.route('/search/<page>', methods=['POST', 'GET'])
def searchTr(page):
    try:
        # We perform the appropriate request and return the page template
        table=m(f'SELECT * FROM item WHERE title="{page}";')
        return render_template('res.html', table=table[0])

    except:
        return render_template('page404.html')


# if necessary, can be used for the future page 
# of each user who will register and be in the database
'''
@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
'''

# profile login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    # may be used in the future*
    # checking if the given user is in 
    # an existing session i.e. checking 
    # if he is logged into the account from the database or not
    '''
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    '''
    return render_template('login.html')


# 404 error page when the url for the page is entered incorrectly
@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html')


if __name__ == "__name__":
    app.run(debug=True)