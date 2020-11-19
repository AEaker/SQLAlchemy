import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
from flask import Flask, jsonify
from dateutil.relativedelta import relativedelta
import datetime 


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Station = Base.classes.station
Measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    return (
        f"Available routes are :<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/station<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/&lt;start&gt;<br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br>"
        f"Please provide the date in YYYY-MM-DD format."
    )
    

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    
    session.close()
    
    precip = []
    for date, prcp in results:
        precipitationdict = {}
        precipitationdict["Date"] = date
        precipitationdict["Precipitation"] = prcp
        precip.append(precipitationdict)
        
    return jsonify(precip)

@app.route("/api/v1.0/station")
def stations():
    session = Session(engine)
    
    results = session.query(Station.station, Station.name).all()
    
    session.close()
    
    StationList = list(np.ravel(results))
    
    return jsonify(StationList)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    datedata = session.query(Measurement.date).order_by(Measurement.date.desc()).limit(1)
    for d in datedata:
        lastdate = d.date
        
    lastdate = datetime.datetime.strptime(lastdate, "%Y-%m-%d")
    
    yeardata = lastdate - relativedelta(years=1)
   
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= yeardata).all()
    session.close()
    
    tobslist = []
    for date, tobs in results:
        tobsdict = {}
        tobsdict["Date"] = date
        tobsdict["Temp"] = tobs
        tobslist.append(tobsdict)
    
    
    return jsonify(tobslist)
    


@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    
    startdate = datetime.datetime.strptime(start, "%Y-%m-%d")
    
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all()
    session.close()
    
    startlist = []
    for date, min, avg, max in results:
        startdict = {}
        startdict["Date"] = date
        startdict["Min"] = min
        startdict["Avg"] = avg
        startdict["Max"] = max
        startlist.append(startdict)
    
 
    return jsonify(startlist)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    
    startdate = datetime.datetime.strptime(start, "%Y-%m-%d")
    enddate = datetime.datetime.strptime(end, "%Y-%m-%d")
    
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all()
    session.close()
    
    startendlist = []
    for date, min, avg, max in results:
        startenddict = {}
        startenddict["Date"] = date
        startenddict["Min"] = min
        startenddict["Avg"] = avg
        startenddict["Max"] = max
        startendlist.append(startenddict)
        
    return jsonify(startendlist)


if __name__ == '__main__':
    app.run(debug=True)