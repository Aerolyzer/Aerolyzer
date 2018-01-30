import urllib2
import json
import sys
import os
import wunderData

'''
 Purpose:        The purpose of this script is to extract the Latitude and Longitude from the EXIF data
 Inputs:         tags: structure storing the image's EXIF data.
 Outputs:        coords: A tuple of the Latitude and Longitude in Decimal form
 Returns:        (lat,lon)
 Assumptions:    The EXIF data is valid.
 '''

def get_coord(tags):
    values = tags['gps gpslatitude'][1:-1].split(", ")
    s = values[2]
    df = float(values[0])
    mf = float(values[1])
    smath = s.split("/")
    sf = float(smath[0])/float(smath[1])
    lat = df + mf/60 + sf/3600
    if tags['gps gpslatituderef'] == 'S':
        lat = lat*(-1)

    values = tags['gps gpslongitude'][1:-1].split(", ")
    s = values[2]
    df = float(values[0])
    mf = float(values[1])
    smath = s.split("/")
    sf = float(smath[0])/float(smath[1])
    lon = df + mf/60 + sf/3600
    if tags['gps gpslongituderef'] == 'W':
        lon = lon*(-1)

    return (lat,lon)


'''
 Purpose:        The purpose of this script is to convert Latitude and Longitude to a ZIP Code
 Inputs:         coord: tuple holding latitude and longitude
 Outputs:        ZIP: 5 digit long ZIP code.
 Returns:        
 Assumptions:    The EXIF data is valid.
 '''

def coord_to_zip(coord):

    try:
#"+str(coord[0])+","+str(coord[1])+"
        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(coord[0])+","+str(coord[1])+"&key=AIzaSyD0SIrsNBNbE9-hSnfa6gMHALCdLZWJ6uI"
        c = urllib2.urlopen(url)
        response = c.read()
        parsedResults = json.loads(response)
        ZIP = parsedResults['results'][0]['address_components'][-1]['long_name']

    except Exception:
        print "Unable to retrieve data: ", sys.exc_info()[0]
        ZIP = "99999"

    finally:
        return ZIP

'''
 Purpose:        The purpose of this script is to convert ZIP Code to a Latitude and Longitude
 Inputs:         ZIP: 5 digit long ZIP code.
 Outputs:        coord: tuple holding latitude and longitude
 Returns:        
 Assumptions:    The EXIF data is valid.
 '''

def zip_to_coord(zip):

    try:
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+zip+'&key=AIzaSyD0SIrsNBNbE9-hSnfa6gMHALCdLZWJ6uI'
        c = urllib2.urlopen(url)
        results = c.read()
        parsedResults = json.loads(results)
	lat = parsedResults['results'][0]['geometry']['location']['lat']
        lon = parsedResults['results'][0]['geometry']['location']['lng']

    except Exception:
        print "Unable to retrieve data: ", sys.exc_info()[0]
        (lat,lon) = (0.0,0.0)

    finally:
        return (lat,lon)

    '''
    Purpose:        The purpose of this function is to determine whether or not the I and
                    II quadrants of the image have rgb values indicitive of a sky
    Inputs:         list of lists red_sky, list of lists green_sky, list of lists blue_sky
                    Note: Each inner list contains rgb for each pixel in a horizontal row
    Outputs:        None
    Returns:        0,1,2
    Assumptions:    N/A
    '''
def sun_position(exifdict):
    coord = get_coord(exifdict)
    data = wunderData.get_data(str(coord[0])+","+str(coord[1]))
    sunriseTime = data['sunrise'].split(':')
    sunsetTime = data['sunset'].split(':')
    sunriseTarget = (int(sunriseTime[0])*60)+int(sunriseTime[1])
    sunsetTarget = (int(sunsetTime[0])*60)+int(sunsetTime[1])

    hoursTime = (exifdict['exif datetimeoriginal'].split(' '))[1].split(':')
    pictureTime = (int(hoursTime[0])*60)+int(hoursTime[1])+int(float(hoursTime[2])/60)

    #print sunriseTarget
    #print sunsetTarget
    #print pictureTime
    if ((pictureTime >= (sunriseTarget - 15)) & (pictureTime <= (sunriseTarget + 30))):
        return 'sunrise'
    elif ((pictureTime >= (sunsetTarget - 30)) & (pictureTime <= (sunsetTarget + 15))):
        return 'sunset'
    elif ((pictureTime > (sunsetTarget + 15))|(pictureTime < (sunriseTarget - 15))):
        return 'night'
    else:
        return 'day'


