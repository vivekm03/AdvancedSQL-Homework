import numpy as np
import pandas as pd
import datetime as dt
from datetime import date, datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/<start>` and `/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
# Calculate the date 1 year ago from the last data point in the database where station is Honolulu
    all_lastdt = session.query(func.max(Measurement.date)).scalar()
    all_yearago=datetime.strptime(all_lastdt, '%Y-%m-%d').date() - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
# Save the query results as a Pandas DataFrame and set the index to the date column
# Sort the dataframe by date
    res_prcp=session.query(Measurement.date, Measurement.prcp).filter(Measurement.prcp != "")\
    .filter(Measurement.date>=all_yearago).all()   

    # Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
    all_prcp = []
    for pr in res_prcp:
        prcp_dict = {}
        prcp_dict= {pr.date : pr.prcp}
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all Station names"""
    res_st=session.query(Measurement.station).distinct().all()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(res_st))

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point."""
# Calculate the date 1 year ago from the last data point in the database where station is Honolulu
    all_lastdt = session.query(func.max(Measurement.date)).scalar()
    all_yearago=datetime.strptime(all_lastdt, '%Y-%m-%d').date() - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
# Save the query results as a Pandas DataFrame and set the index to the date column
# Sort the dataframe by date
    res_temp=session.query(Measurement.date, Measurement.tobs).filter(Measurement.tobs != "")\
    .filter(Measurement.date>=all_yearago).all()   

    # Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
    all_tobs = []
    for temp in res_temp:
        temp_dict = {}
        temp_dict= {temp.date : temp.tobs}
        all_tobs.append(temp_dict)

    return jsonify(all_tobs)



if __name__ == '__main__':
    app.run(debug=True)
