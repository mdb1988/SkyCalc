"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
from skyfield.api import load, now
import datetime
from skyfield.timelib import JulianDate
import pytz
import json


class Moment:
    def __init__(self, altitude, azimuth, au,date):
        self.altitude = altitude
        self.azimuth = azimuth
        self.au = au
        self.date = date


    def as_json(self):
        return dict(
            altitude = str(self.altitude),
            azimuth = str(self.azimuth),
            au = str(self.au),
            date =  self.date.strftime("%d-%m-%Y %H:%M"))


def Print(position, stri,date):
 altitude, azimuth, distance = position.apparent().altaz()
 return Moment(altitude,azimuth,distance,date) 

def Calculate(earth,planet,stri,lat,long):
    #boston = earth.topos('50.833639 N', '4.018829 E')
    boston = earth.topos(lat+' N', long+' E')
    startDate = datetime.datetime( 2015, 11, 1,22,00,00,0, pytz.UTC )
    endDate = datetime.datetime( 2016, 4, 1,22,00,00,0, pytz.UTC )
    dayDelta = datetime.timedelta( days=1 )
    momentList = []
    while startDate < endDate:
        startDate += dayDelta
        date =  JulianDate(startDate)
        position = boston.at(date).observe(planet)
        momentList.append(Print(position,stri,date.utc_datetime()))
    return momentList


def formatandreturn(planet,lat,long):
    planets = load('de421.bsp')
    earth = planets['earth']
    mars = planets[planet]
    return Calculate(earth,mars,"Venus",lat,long) 


@app.route('/')
@app.route('/getPlanetPosition/<planet>/<lat>/<long>')
def getPlanetPosition(planet,lat,long):
    """Renders the home page."""    
    new = str(planet).replace('%20',' ')    
    var = formatandreturn(new,lat,long)
    results = [ob.as_json() for ob in var]   
    return json.dumps(results)    


