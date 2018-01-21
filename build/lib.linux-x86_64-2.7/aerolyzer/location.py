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
    if 'GPSLatitudeRef' in tags:
        if 'GPSLatitude' in tags:
            d = tags['GPSLatitude'][0]
            m = tags['GPSLatitude'][1]
            s = tags['GPSLatitude'][2]
            lat = d + m/60 + s/3600
            if tags['GPSLatitudeRef'] == 'S':
                lat = lat*(-1)
        else:
            print "GPSLatitude not found: ", sys.exc_info()[0]
            lat = 0.0
    else:
        print "GPSLatitudeRef not found: ", sys.exc_info()[0]
        lat = 0.0

    if 'GPSLongitudeRef' in tags:
        if 'GPSLongitude' in tags:
            d = tags['GPSLongitude'][0]
            m = tags['GPSLongitude'][1]
            s = tags['GPSLongitude'][2]
            lon = d + m/60 + s/3600
            if tags['GPSLongitudeRef'] == 'W':
                lon = lon*(-1)
        else:
            print "GPSLongitude not found: ", sys.exc_info()[0]
            lon = 0.0
    else:
        print "GPSLongitudeRef not found: ", sys.exc_info()[0]
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
#        c = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng='+coord[0]+','+coord[1]'&key=YOUR_API_KEY')
#        results = c.read()
#        parsedResults = json.loads(results)
#	ZIP = parsedResults['address_components']['postal_code']['long_name']

#    except Exception:
#        print "Unable to retrieve data: ", sys.exc_info()[0]
#        ZIP = "99999"

#    finally:
#        return ZIP

