from aerolyzer.retrieve_image_data import RtrvData as Data
import os

mytest = Data("./")
exifdict = mytest.get_exif("/home/aero/Documents/Aerolyzer/Aerolyzer/aerolyzer/images/img1.jpg",True,True)
lat = 0.0
if 'GPSLatitudeRef' in exifdict:
    if 'GPSLatitude' in exifdict:
        d = exifdict['GPSLatitude'][0]
        m = exifdict['GPSLatitude'][1]
        s = exifdict['GPSLatitude'][2]
        lat = d + m/60 + s/3600
        if tags['GPSLatitudeRef'] == 'S':
            lat = lat*(-1)
    else:
        print "GPSLatitude not found: ", sys.exc_info()[0]
        lat = 0.0
print lat


