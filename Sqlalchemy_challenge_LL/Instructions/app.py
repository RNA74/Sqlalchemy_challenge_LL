import numpy as np
import sqlalchemy
import datetime as dt
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

##############################
# Database Setup
##############################
engine = create_engine('sqlite:///hawaii.sqlite')

##############################
#Reflect an existing database into a new model
##############################
Base = automap_base()

#Reflect the tables
Base.prepare(engine, reflect=True)

#Save refrence into tables
Measurement = Base.classes.measurement
Station = Base.classes.station
print(Base.classes.keys())
session = Session(engine)
app = Flask(__name__)
################################
# Creating a flask
################################
@app.route("/")
def welcome():
    """List all available API routes"""
    return (
        f"Available Routes:br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
       
    )
    
#################################
#Calculate the date one year from the last date in data set.
#################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_tweleve_months = dt.date(2017,8,23)- dt.timedelta(days=365)
 #################################  
 #Query the dates and temperature observations of the most active station for the last year of data.
 ################################  
    p_s_data= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=last_tweleve_months).all()
    return jsonify(p_s_data) 

###################################
#Return the JSON representation of your dictionary.
###################################

@app.route("/api/v1.0/stations")
def stations():
    total_s= session.query(func.count(Station.station)).all()
    
#Return a JSON list of temperature observations (TOBS) for the previous year.
    stations = list(np.ravel(total_s))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_m():

    last_tweleve_m_t= dt.date(2017,8,23)- dt.timedelta(days=365)

#Query the last 12 months of temperature observation data for this station 
t_s_tweleve_m = session.query(Measurement.station,Measurement.tobs).\
    filter(Measurement.station == "USC00519281").filter(Measurement.date >=last_tweleve_m_t).all()





if __name__== "__main__":
  app.run(debug=True) 

    

