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
    return (f"Available Routes:<br/><br/>"
        f"Precipitation Data for One Year<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"List of Stations:<br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"List of Temperatures for 2017:<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"Min, Max, and Avg Temperatures from start date yyyy-mm-dd:<br/>"
        f"/api/v1.0/<start><br/><br/>"
        f"Min, Max, and Avg Temperatures from start to end date: yyyy-mm-dd/yyyy-mm-dd<br/>"
        f"/api/v1.0/<start>/<end><br/>"
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


    #Retrieve date and precipitation values from query results
    #Create dictionary and append values to empty list
    
    precipitation_data = []
    for date, prcp in prcp_data:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        precipitation_data.append(precipitation_dict)

    #Render precipitation data in json format
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    
    #Create session to link database to Python
    session = Session(engine)

    #Query results of the list of stations
    stations = session.query(Measurement.station).\
    group_by(Measurement.station).\
    order_by(Measurement.station).all()

    #Retrieve stations data from query results, create dictionary, and append to empty list
    stations_list = []
    for station in stations:
        station_dict = {}
        station_dict["station"] = station
        stations_list.append(station_dict)

    #Render station data in json format thru app
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

    #Retrieve date and temp values from query results, create dictionary, and append to empty list
    temps_list = []
    for date, temperature in stations_temp:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = temperature
        temps_list.append(temp_dict)

    #Render temp values in json format thru app
    return jsonify(temps_list)

@app.route("/api/v1.0/<start>")
def start_date(start):

    #Create session to link database to Python
    session = Session(engine)

    #Design query to return min, max, and avg temperatures for any date entered
    temp = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    #Retrieve min, max, and avg temp results from query, create dictionary, and append to empty list
    temp_values_date = []
    for min_temp, max_temp, avg_temp in temp:
        temp_value_dict = {}
        temp_value_dict["min temperature"] = min_temp
        temp_value_dict["max temperature"] = max_temp
        temp_value_dict["avg temperature"] = avg_temp
        temp_values_date.append(temp_value_dict)
    
    #Render temp values in json format thru app
    return jsonify(temp_values_date)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    #Create session to link database to Python
    session = Session(engine)

    #Design query to return min, max, and avg temperatures for all applicable start and end date range entered
    temp_date_range = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start, Measurement.date <= end).all()

    #Retrieve min, max, and avg temp values from query results, create dictionary, and append to empty list
    temp_values_date_range = []
    for min_temp, max_temp, avg_temp in temp_date_range:
        temp_value_range_dict = {}
        temp_value_range_dict["min temperature"] = min_temp
        temp_value_range_dict["max temperature"] = max_temp
        temp_value_range_dict["avg temperature"] = avg_temp
        temp_values_date_range.append(temp_value_range_dict)
    
    #Render temp values in json format thru app
    return jsonify(temp_values_date_range)


if __name__ == '__main__':
    app.run(debug=True)