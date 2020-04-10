#Import Flask
from flask import Flask, jsonify

#Create dictionary for precipitation values



#Create dictionary for station values



#Create dictionary for temperature values



#Create an app
app = Flask(__name__)

#Define routes
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome! Data includes Precipitation, Stations, and Temperatures"


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data as json"""

    return jsonify()

@app.route("/api/v1.0/stations")
def stations():
    """Return station data as json"""

    return jsonify()

@app.route("/api/v1.0/tobs")
def temperatures():
    """Return temperatures data as json"""

    return jsonify()

