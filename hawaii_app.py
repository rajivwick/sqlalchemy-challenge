import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"""/api/v1.0/(start)<br/>"""
        f"/api/v1.0/(start)/(end)"
    )

# Return date and precipitation values as a json.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Retrieve the date and prcp
    query = [Measurements.date,Measurements.prcp]
    # Store the results
    weather_data = session.query(*query).all()
    # Create dictionary with date as the key and precipitation as the value.
    all_weather_dict = []
    for date, prcp in weather_data:
        weather_dict = {}
        weather_dict[date] = prcp
        all_weather_dict.append(weather_dict)

    session.close()

    return jsonify(all_weather_dict)

# Return a list of stations 
@app.route("/api/v1.0/stations")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Stations.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)


# Return the last years worth of tobs data for the most active station (USC00519281)
@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    st_date = dt.date(2017,8,18)- dt.timedelta(days=365)
    query4 = [Measurements.date, Measurements.tobs]

    USC00519281_data = session.query(*query4).\
    filter(Measurements.station == 'USC00519281').\
    filter(Measurements.date >= st_date).all()

    USC00519281 = list(np.ravel(USC00519281_data))

    return jsonify(USC00519281)

# When a start date is entered, return the min, average and max tobs values using the starting date.
@app.route("/api/v1.0/<start>")
def start_stats(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    query = [func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)]

    start_summary = session.query(*query).\
    filter(Measurements.date >= start).all()
    summary = list(np.ravel(start_summary))
    
    return jsonify(summary)

# When a start and end data is entered, return the min, average and max tobs values between the two date used.
@app.route("/api/v1.0/<start>/<end>")
def startend_stats(start,end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    query = [func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)]

    startend_summary = session.query(*query).\
    filter(Measurements.date >= start).\
    filter(Measurements.date <= end).all()
    summary = list(np.ravel(startend_summary))
    
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)
