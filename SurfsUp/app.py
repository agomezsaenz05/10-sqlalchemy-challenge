# Dependencies 
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import session

from flask import Flask, jsonify

# Databe Setup
engine = create_engine("sqlite:///Resources\hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
#home
@app.route("/")
def home():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
#precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    latest_date = session.query(func.max(Measurement.date)).scalar()
    last_year = (dt.datetime.strptime(latest_date, '%y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    results = session.query(Measurement.date,Measurement.prcp)\
                    .filter(Measurement.date >= last_year)\
                    .order_by(Measurement.date).all()
    session.close()

    prcp_dict = {}
    for date, prcp in results:
        prcp_dict[date] = prcp
    return jsonify(prcp_dict)

#stations
@app.route("/api/v1.0/stations") 
def stations():
    results = session.query(Station.name).all()
    station_details = list(np.ravel(results))

    return jsonify(station_details)

#tobs
@app.route("/api/v1.0/tobs") 
def tobs():
    most_active_st = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()
    latest_date = session.query(Measurement.station).\
        filter(Measurement.station == most_active_st[0]).\
        order_by(Measurement.date.desc()).first()
    
    latest_date = dt.datetime.strptime(latest_date[0], "%Y-%m-%d")
    last_year = latest_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= last_year).all()

    tobs_dict = {}
    for results in results:
        tobs_dict[result[0]] = result[1]
    return jsonify(tobs_dict)

#start
@app.route("/api/v1.0/<start>") 
def start_date(start):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs)func.max(Measurement.tobs))\
                    .filter(Measurement.date >= start_date)\
                    .all()
    temps_dict = {'TMIN': results[0][0], 'TAVG': round(results[0][1], 2), 'TMAX': results[0][2]}
    return jsonify(temps_dict)

#start/end
@app.route("/api/v1.0/<start>/<end>") 
def start_end_date(start, end):
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")
        results = session.query.(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date)\
        .filter(Measuerement <= end_date)\
        .all()
        temps_dict = {'TMIN': results[0][0], 'TAVG': round(results[0][1], 2), 'TMAX': results[0][2]}
        return jsonify(temps_dict)

if __name__ == ' __main__':
     app.run(debug=True)





    

  



