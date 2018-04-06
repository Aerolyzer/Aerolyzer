import urllib2
import json
import sys
import os

#def get_wunderkey()

def get_data(coord):
    '''
    Purpose:        The purpose of this script is to retrieve meteorological data 
    of a given comma-separated latitude and longitute coordinates via the
    wunderground API.
    Inputs:         coord: string representing comma-separated coordinates.
    Outputs:        weatherData: tuple of city, country, temp in F, sunrise time, sunset time.
    Returns:        dictionary with 5 keys.
    Assumptions:    The wunderground API key is valid.
    '''

    name = coord + '.json'

    try:
        f = urllib2.urlopen('http://api.wunderground.com/api/3b566c79c371f7f4/geolookup/conditions/q/' + name)
        m = urllib2.urlopen('http://api.wunderground.com/api/3b566c79c371f7f4/astronomy/q/' + name)

        conditions = f.read()
        parsedConditions = json.loads(conditions)
        astronomy = m.read()
        parsedAstronomy = json.loads(astronomy)

        city = parsedConditions['location']['city']
        country = parsedConditions['location']['country']
        temp = parsedConditions['current_observation']['temp_f']
        sunriseMin = parsedAstronomy['moon_phase']['sunrise']['minute']
        sunriseHr = parsedAstronomy['moon_phase']['sunrise']['hour']
        sunrise = sunriseHr + ":" + sunriseMin
        sunsetMin = parsedAstronomy['moon_phase']['sunset']['minute']
        sunsetHr = parsedAstronomy['moon_phase']['sunset']['hour']
        sunset = sunsetHr + ":" + sunsetMin

        weatherData = {'city': city, 'country': country, 'temp': temp, 'sunrise': sunrise, 'sunset': sunset}

    except Exception:
        print ("Unable to retrieve data: ", sys.exc_info()[0])
        weatherData = None

    finally:
        return weatherData
