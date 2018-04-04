import urllib2
import json
import sys
import os
import wunderData

def get_coord(exifdict):
    '''
    Purpose:        The purpose of this script is to extract the Latitude and Longitude from the EXIF data
    Inputs:         exifdict: structure storing the image's EXIF data.
    Outputs:        coords: A tuple of the Latitude and Longitude in Decimal form
    Returns:        (lat,lon)
    Assumptions:    The EXIF data is valid.
    '''
    values = exifdict['gps gpslatitude'][1:-1].split(", ")
    s = values[2]
    df = float(values[0])
    mf = float(values[1])
    smath = s.split("/")
    sf = float(smath[0])/float(smath[1])
    lat = df + mf/60 + sf/3600
    if exifdict['gps gpslatituderef'] == 'S':
        lat = lat*(-1)

    values = exifdict['gps gpslongitude'][1:-1].split(", ")
    s = values[2]
    df = float(values[0])
    mf = float(values[1])
    smath = s.split("/")
    sf = float(smath[0])/float(smath[1])
    lon = df + mf/60 + sf/3600
    if exifdict['gps gpslongituderef'] == 'W':
        lon = lon*(-1)

    return (lat,lon)



def coord_to_zip(coord,googlegeokey):
    '''
    Purpose:        The purpose of this script is to convert Latitude and Longitude to a ZIP Code
    Inputs:         coord: tuple holding latitude and longitude, googlegeokey: The Google geocoding API
    Outputs:        string of 5 digit long ZIP code.
    Returns:        zipcode
    Assumptions:    The EXIF data is valid.
    '''

    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(coord[0])+","+str(coord[1])+"&key="+googlegeokey
        c = urllib2.urlopen(url)
        response = c.read()
        parsedResults = json.loads(response)
        zipcode = parsedResults['results'][0]['address_components'][-1]['long_name']

    except Exception:
        print "Unable to retrieve data: ", sys.exc_info()[0]
        zipcode = "99999"

    finally:
        return zipcode



def zip_to_coord(zipcode,googlegeokey):
    '''
    Purpose:        The purpose of this script is to convert ZIP Code to a Latitude and Longitude
    Inputs:         zipcode: 5 digit long ZIP code.
    Outputs:        coord: tuple holding latitude and longitude
    Returns:        (lat,lon)
    Assumptions:    The EXIF data is valid.
    '''
    try:
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+zipcode+'&key='+googlegeokey
        c = urllib2.urlopen(url)
        results = c.read()
        parsedResults = json.loads(results)
	lat = float(parsedResults['results'][0]['geometry']['location']['lat'])
        lon = float(parsedResults['results'][0]['geometry']['location']['lng'])

    except Exception:
        print "Unable to retrieve data: ", sys.exc_info()[0]
        (lat,lon) = (0.0,0.0)

    finally:
        return (lat,lon)


def sun_position(exifdict):
    '''
    Purpose:        Identify whether an image was taken during sunrise or sunset.
    Inputs:         exifdict: structure storing the image's EXIF data.
    Outputs:        string
    Returns:        sunrise,sunset,night,day
    Assumptions:    N/A
    '''
    coord = get_coord(exifdict)
    wData = wunderData.get_data(str(coord[0])+","+str(coord[1]))
    sunriseTime = wData['sunrise'].split(':')
    sunsetTime = wData['sunset'].split(':')
    sunriseTarget = (int(sunriseTime[0])*60)+int(sunriseTime[1])
    sunsetTarget = (int(sunsetTime[0])*60)+int(sunsetTime[1])

    hoursTime = (str(exifdict['exif datetimeoriginal']).split(' '))[1].split(':')
    pictureTime = (int(hoursTime[0])*60)+int(hoursTime[1])+int(float(hoursTime[2])/60)

    if ((pictureTime >= (sunriseTarget - 15)) & (pictureTime <= (sunriseTarget + 30))):
        return 'sunrise'
    elif ((pictureTime >= (sunsetTarget - 15)) & (pictureTime <= (sunsetTarget + 30))):
        return 'sunset'
    elif ((pictureTime > (sunsetTarget + 15))|(pictureTime < (sunriseTarget - 15))):
        return 'night'
    else:
        return 'day'


