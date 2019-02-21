#export FLASK_APP=application.py
#export DATABASE_URL="postgres://ayjxjjxhgpzlnl:f150cc319da46e38a1fb398ee335d98fa5468668d0d8aa3da415aed475d08f9b@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d9prh5mib7dh2p"
#key: 0S6vFxQgJiRIw2CZbc2Yg
#secret: 0kmzCjBS62odOXkfg4EcYnoBND3IM28ANuEFlTlWig
#import datetime
from flask import Flask, render_template, request, session, jsonify# Import the class `Flask` from the `flask` module, written by someone else.
from flask_session import Session
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pprint import pprint
#import csv
import json #for Python to Javascript
import requests #for JSON

app = Flask(__name__) # Instantiate a new web application called `app`, with `__name__` representing the current file

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session (app)

engine = create_engine("postgres://ayjxjjxhgpzlnl:f150cc319da46e38a1fb398ee335d98fa5468668d0d8aa3da415aed475d08f9b@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d9prh5mib7dh2p")
#talk to datbase wiTh SQL. Object used to manage connections to database.
#Sending data to and from database
db = scoped_session(sessionmaker(bind=engine)) # for individual sessions

mechanic_list=[]

#db.execute("CREATE TABLE mechanic(id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, phone VARCHAR NOT NULL, address VARCHAR NOT NULL, latitude FLOAT NOT NULL, longitude FLOAT NOT NULL, email VARCHAR, oil_change SMALLINT NOT NULL, battery SMALLINT NOT NULL, pads_front SMALLINT NOT NULL, pads_back SMALLINT NOT NULL, starting_problem SMALLINT NOT NULL, check_engine SMALLINT NOT NULL, tune_up SMALLINT NOT NULL, starter SMALLINT NOT NULL, alternator SMALLINT NOT NULL, spark_plugs SMALLINT NOT NULL, valve_cover SMALLINT NOT NULL, air_filter SMALLINT NOT NULL, mobile_mechanic BOOLEAN NOT NULL, air_conditioning BOOLEAN NOT NULL, auto_body BOOLEAN NOT NULL, tire_rotation BOOLEAN NOT NULL, fix_flat BOOLEAN NOT NULL, car_wash BOOLEAN NOT NULL)")
#db.commit()
mechanicsD = db.execute("SELECT * FROM mechanic").fetchall()
print("mechanicsD",mechanicsD)
@app.route("/", methods = ["GET"]) # A decorator; when the user goes to the route `/`, exceute the function immediately below
def index():
	for i in mechanicsD:
		print("mechanicsD",i)
		mechanic_data = {
			"name": i.name,
			"phone": i.phone,
			"address": i.address,
			"longitude": i.longitude,
			"latitude": i.latitude,
			"email": i.email,
			}
		mechanic_list.append(mechanic_data)
	return render_template("index.html", mechanic_list=mechanic_list)

@app.route("/signup", methods = ["POST"])
def signup():
	return render_template("signup.html")
