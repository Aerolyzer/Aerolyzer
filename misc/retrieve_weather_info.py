'''
 Purpose:        The purpose of this script is to retrieve meteorological data 
                 of a given city/state, city/country, or comma-separated latitude and longitute 
				 coordinates via the wunderground API.
 Inputs:         city: string representing name of city, None if using coordinates.
				 stateOrCountry: string representing name of U.S. state or name of country
				 associated with city, None if using coordinates, required if city is given.
				 coord: string representing comma-separated coordinates, None if using city.
 Outputs:        weatherData: tuple of city, country, temp in F, sunrise time, sunset time.
 Returns:        tuple with 5 strings.
 Assumptions:    The wunderground API key is valid.
 '''
import urllib2, json, sys, os, argparse

def getData(city, stateOrCountry, coord):
    weatherData = ('n/a','n/a','n/a','n/a','n/a')
    if city is not None:
        city = city.replace(" ", "_")
        stateOrCountry = stateOrCountry.replace(" ", "_")
        stateOrCountry = stateOrCountry.upper()
        name = stateOrCountry + '/' + city + '.json'
    elif coord is not None:
        coord = coord.replace(" ", "")
        name = coord + '.json'
        
    try:
        f = urllib2.urlopen('http://api.wunderground.com/api/622ff5c1b6d14ee0/geolookup/conditions/q/' + name)
        m = urllib2.urlopen('http://api.wunderground.com/api/622ff5c1b6d14ee0/astronomy/q/' + name);

        conditions = f.read()
        parsedConditions = json.loads(conditions)
        astronomy = m.read()
        parsedAstronomy = json.loads(astronomy)
        
        city = parsedConditions['location']['city']
        country = parsedConditions['location']['country']
        temp_f = parsedConditions['current_observation']['temp_f']
        sunrise_min = parsedAstronomy['moon_phase']['sunrise']['minute']
        sunrise_hr = parsedAstronomy['moon_phase']['sunrise']['hour']
        sunrise = sunrise_hr + ":" + sunrise_min
        sunset_min = parsedAstronomy['moon_phase']['sunset']['minute']
        sunset_hr = parsedAstronomy['moon_phase']['sunset']['hour']
        sunset = sunset_hr + ":" + sunset_min
        #angle of sun?

        weatherData = (city, country, temp_f, sunrise, sunset)
        
    except Exception:
        print "Unable to retrieve data: ", sys.exc_info()[0]

    finally:
        m.close()
        f.close()
        return weatherData
		
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--city', help='city to retrieve weather data about')
    parser.add_argument('-s', '--state', help='U.S. state or country city is located in, required if using city')
    parser.add_argument('-l', '--coords', help='comma-separated coordinates to retrieve weather data about')
    args = parser.parse_args()
    if args.city is not None:
        city = args.city
        stateOrCountry = args.state
        coord = None
    elif args.coords is not None:
        city = None
        stateOrCountry = None
        coord = args.coords
    else:
        parser.print_help()
        sys.exit(2)
    weatherData = getData(city, stateOrCountry, coord)
    print "City: %s" % weatherData[0]
    print "Country: %s" % weatherData[1]
    print "Current temp: %s" % weatherData[2]
    print "Sunrise: %s" % weatherData[3]
    print "Sunset: %s" % weatherData[4]

        
