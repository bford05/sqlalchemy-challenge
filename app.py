#Import required packages

import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

#Setup Database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect the database into a new model
Base = automap_base()

#Reflect tables from the database
Base.prepare(engine, reflect=True)

#Save references to tables from the database
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create an app
app = Flask(__name__)

#Setup Flask routes
@app.route("/")
def home():
    print("List all available api routes")
    return (f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session to link Database to Python
    session = Session(engine)

    #Query results of precipitation data
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').\
    order_by(Measurement.date).all()


    #Create dictionary and append date and precipitation values from query
    #Return json format of precipitation data
    
    precipitation_data = []
    for date, prcp in prcp_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    
    #Create session to link database to Python
    session = Session(engine)

    #Query results of the list of stations
    stations = session.query(Measurement.station).\
    group_by(Measurement.station).\
    order_by(Measurement.station).all()

    #Return list of stations in json format
    stations_list = []
    for station in stations:
        station_dict = {}
        station_dict["station"] = station
        stations_list.append(station_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def temperatures():
    
    #Create session to link database to Python
    session = Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data.
    stations_temp = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= '2017-01-01').\
    filter(Measurement.date <= '2017-12-31').\
    group_by(Measurement.date).all()

    #Return temperature observations for the most active station for the last year in json format
    temps_list = []
    for date, tobs in stations_temp:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temps_list.append(temp_dict)

    return jsonify(temps_list)

if __name__ == '__main__':
    app.run(debug=True)