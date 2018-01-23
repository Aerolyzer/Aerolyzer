import urllib2
import json
import sys
import os

'''
 Purpose:        The purpose of this script is to extract the Latitude and Longitude from the EXIF data
 Inputs:         tags: structure storing the image's EXIF data.
 Outputs:        coords: A tuple of the Latitude and Longitude in Decimal form
 Returns:        (lat,lon)
 Assumptions:    The EXIF data is valid.
 '''

def get_coord(tags):
    if 'gps gpslatituderef' in tags:
        if 'gps gpslatitude' in tags:
            values = tags['gps gpslatitude'][1:-1].split(", ")
            d = values[0]
            m = values[1]
            s = values[2]
	    df = float(d)
            mf = float(m)
            smath = s.split("/")
            sf = float(smath[0])/float(smath[1])
            lat = df + mf/60 + sf/3600
            if tags['gps gpslatituderef'] == 'S':
                lat = lat*(-1)
        else:
            print "gps gpslatitudeatitude not found: ", sys.exc_info()[0]
            lat = 0.0
    else:
        print "gps gpslatitudeatituderef not found: ", sys.exc_info()[0]
        lat = 0.0

    if 'gps gpslongituderef' in tags:
        if 'gps gpslongitude' in tags:
            values = tags['gps gpslongitude'][1:-1].split(", ")
            d = values[0]
            m = values[1]
            s = values[2]
	    df = float(d)
            mf = float(m)
            smath = s.split("/")
            sf = float(smath[0])/float(smath[1])
            lon = df + mf/60 + sf/3600
            if tags['gps gpslongituderef'] == 'W':
                lon = lon*(-1)
        else:
            print "gps gpslongitude not found: ", sys.exc_info()[0]
            lon = 0.0
    else:
        print "gps gpslongituderef not found: ", sys.exc_info()[0]
        lon = 0.0

    return (lat,lon)


'''
 Purpose:        The purpose of this script is to convert Latitude and Longitude to a ZIP Code
 Inputs:         coord: tuple holding latitude and longitude
 Outputs:        ZIP: 5 digit long ZIP code.
 Returns:        
 Assumptions:    The EXIF data is valid.
 '''

#def coord_to_zip(coord):

#    try:
#        c = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng='+coord[0]+','+coord[1]'&key=AIzaSyD0SIrsNBNbE9-hSnfa6gMHALCdLZWJ6uI')
#        results = c.read()
#        parsedResults = json.loads(results)
#	ZIP = parsedResults['address_components']['postal_code']['long_name']

#    except Exception:
#        print "Unable to retrieve data: ", sys.exc_info()[0]
#        ZIP = "99999"

#    finally:
#        return ZIP

