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


#db.execute("CREATE TABLE mechanic_list1(id SERIAL PRIMARY KEY, name VARCHAR NOT NULL, password VARCHAR NOT NULL, phone VARCHAR NOT NULL, address VARCHAR NOT NULL, latitude FLOAT NOT NULL, longitude FLOAT NOT NULL, email VARCHAR, years SMALLINT NOT NULL, description VARCHAR NOT NULL, oil_change SMALLINT NOT NULL, battery SMALLINT NOT NULL, pads_front SMALLINT NOT NULL, pads_back SMALLINT NOT NULL, starting_problem SMALLINT NOT NULL, check_engine SMALLINT NOT NULL, tune_up SMALLINT NOT NULL, starter SMALLINT NOT NULL, alternator SMALLINT NOT NULL, spark_plugs SMALLINT NOT NULL, valve_cover SMALLINT NOT NULL, air_filter SMALLINT NOT NULL, mobile_mechanic BOOLEAN NOT NULL, air_conditioning BOOLEAN NOT NULL, auto_body BOOLEAN NOT NULL, tire_rotation BOOLEAN NOT NULL, fix_flat BOOLEAN NOT NULL, car_wash BOOLEAN NOT NULL)")
#db.commit()



@app.route("/", methods = ["GET"]) # A decorator; when the user goes to the route `/`, exceute the function immediately below
def index():
	mechanicsD = db.execute("SELECT * FROM mechanic_list1").fetchall()
	print("mechanicsD",mechanicsD)
	print("Databasesuccess")
	for i in mechanicsD:
		print("mechanicsD",i)
		mechanic_data = {
			"name": i.name,
			"phone": i.phone,
			"address": i.address,
			"longitude": i.longitude,
			"latitude": i.latitude,
			"email": i.email,
			"years": i.years,
			"description": i.description,
			"oil_change": i.oil_change,
			"battery": i.battery,
			"pads_front": i.pads_front,
			"pads_back": i.pads_back,
			"starting_problem": i.starting_problem,
			"check_engine": i.check_engine,
			"tune_up": i.tune_up,
			"starter": i.starter,
			"alternator": i.alternator,
			"spark_plugs": i.spark_plugs,
			"valve_cover": i.valve_cover,
			"air_filter": i.air_filter,
			"mobile_mechanic": i.mobile_mechanic,
			"air_conditioning": i.air_conditioning,
			"auto_body": i.auto_body,
			"tire_rotation": i.tire_rotation,
			"fix_flat": i.fix_flat,
			"car_wash": i.car_wash,
			}
		print ("description",i.description)
		print ("years",i.years)
		mechanic_list.append(mechanic_data)

	return render_template("index.html", mechanic_list=mechanic_list)

@app.route("/signup", methods = ["POST"])
def signup():
	return render_template("signup.html")

@app.route("/signup_check", methods = ["POST"])
def signup_check():
	name = request.form.get("name")
	password = request.form.get("password")
	phone = request.form.get("phone")
	street = request.form.get("street")
	city = request.form.get("city")
	state = request.form.get("state")
	zip_code = request.form.get("zip_code")
	email = request.form.get("email")
	years = request.form.get("years")
	description = request.form.get("description")
	oil_change = request.form.get("oil_change")
	battery = request.form.get("battery")
	pads_front = request.form.get("pads_front")
	pads_back = request.form.get("pads_back")
	starting_problem= request.form.get("starting_problem")
	check_engine = request.form.get("check_engine")
	tune_up = request.form.get("tune_up")
	starter = request.form.get("starter")
	alternator = request.form.get("alternator")
	spark_plugs = request.form.get("spark_plugs")
	valve_cover = request.form.get("valve_cover")
	air_filter = request.form.get("air_filter")
	mobile_mechanic = request.form.get("mobile_mechanic")
	air_conditioning = request.form.get("air_conditioning")
	auto_body = request.form.get("auto_body")
	tire_rotation = request.form.get("tire_rotation")
	fix_flat = request.form.get("fix_flat")
	car_wash = request.form.get("car_wash")
	address = street+", "+city+", "+state+", "+zip_code
	print(address)

	if mobile_mechanic=="on":
		mobile_mechanic=True
	else:
		mobile_mechanic=False

	if air_conditioning=="on":
		air_conditioning=True
	else:
		air_conditioning=False

	if auto_body=="on":
		auto_body=True
	else:
		auto_body=False

	if fix_flat=="on":
		fix_flat=True
	else:
		fix_flat=False

	if tire_rotation=="on":
		tire_rotation=True
	else:
		tire_rotation=False

	if car_wash=="on":
		car_wash=True
	else:
		car_wash=False

		#geocode
	params = {
		'address': address,
		'key': 'AIzaSyD9fytSdXXr6kVZdXLddFJyF9HT4JTt-qM',
	}
	res = requests.get(GOOGLE_MAPS_API_URL, params=params)
	response = res.json()
	#print("jsonresonse",response)
	latlng=response['results'][0]['geometry']['location']
	latitude = latlng['lat']
	longitude = latlng['lng']
	print("lat", latlng['lat'])
	print("lng", latlng['lng'])
	db.execute("INSERT INTO mechanic_list1 (name, password, phone, address, latitude, longitude, email, years, description, oil_change, battery, pads_front, pads_back, starting_problem, check_engine, tune_up, starter, alternator, spark_plugs, valve_cover, air_filter, mobile_mechanic, air_conditioning, auto_body, tire_rotation, fix_flat, car_wash) VALUES (:name, :password, :phone, :address, :latitude, :longitude, :email, :years, :description, :oil_change, :battery, :pads_front, :pads_back, :starting_problem, :check_engine, :tune_up, :starter, :alternator, :spark_plugs, :valve_cover, :air_filter, :mobile_mechanic, :air_conditioning, :auto_body, :tire_rotation, :fix_flat, :car_wash)", {"name":name, "password":password, "phone":phone, "address":address, "latitude":latitude, "longitude":longitude, "email":email, "years":years, "description":description, "oil_change":oil_change, "battery":battery, "pads_front":pads_front, "pads_back":pads_back, "starting_problem":starting_problem, "check_engine":check_engine, "tune_up":tune_up, "starter":starter, "alternator":alternator, "spark_plugs":spark_plugs, "valve_cover":valve_cover, "air_filter":air_filter, "mobile_mechanic":mobile_mechanic, "air_conditioning":air_conditioning, "auto_body":auto_body, "tire_rotation":tire_rotation, "fix_flat":fix_flat, "car_wash":car_wash})
	db.commit()
	return "Uploaded to Database"
