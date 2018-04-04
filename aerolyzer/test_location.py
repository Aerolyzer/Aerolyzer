from retrieve_image_data import RtrvData as Data
import location
import image_restriction_main
Google_API = "AIzaSyD0SIrsNBNbE9-hSnfa6gMHALCdLZWJ6uI"

def test_location_all():
        filepath = input("Input File Path for Test Image: ")
        testspassed  = 0
        if(test_get_coord(filepath)==0):
                print "test_get_coord passed\n"
                testspassed+=1
        else:
                print "test_get_coord failed\n"

        if(test_coord_to_zip(filepath)==0):
                print "test_coord_to_zip passed\n"
                testspassed+=1
        else:
                print "test_coord_to_zip failed\n"

        if(test_zip_to_coord(filepath)==0):
                print "test_zip_to_coord passed\n"
                testspassed+=1
        else:
                print "test_zip_to_coord failed\n"

        if(test_sun_position(filepath)==0):
                print "test_sun_position passed\n"
                testspassed+=1
        else:
                print "test_sun_position failed\n"

        print "Number of Tests passed "+ str(testspassed) +"/4\n"


def test_get_coord(filename):
        if(image_restriction_main.check_image(filename)):
                imagedata = Data(filename)
                exifData = imagedata.get_exif(filename, True, False)
                coords = location.get_coord(exifData)
                print "\tOriginal image data: ("+exifData['gps gpslatitude'][1:-1]+","+exifData['gps gpslongitude'][1:-1]+")\n"
                print "\tConverted image data: ("+str(coords[0])+","+str(coords[1])+")\n"
                return 1
                
        else:
                print "\tImage failed a restriction test.\n"
                return 0

def test_coord_to_zip(filename):
        if(image_restriction_main.check_image(filename)):
                imagedata = Data(filename)
                exifData = imagedata.get_exif(filename, True, False)
                coords = location.get_coord(exifData)
                zipcode = location.coord_to_zip(coords,Google_API)
                print "\tOriginal image data: ("+exifData['gps gpslatitude'][1:-1]+","+exifData['gps gpslongitude'][1:-1]+")\n"
                if(zipcode=="99999"):
                        print "\tError fetching ZIP Code\n"
                        return 0
                else:
                        print "\tFetched image data: ZIP = "+zipcode+"\n"
                        return 1 
        else:
                print "\tImage failed a restriction test.\n"
                return 0

def test_zip_to_coord(filename):
        if(image_restriction_main.check_image(filename)):
                imagedata = Data(filename)
                exifData = imagedata.get_exif(filename, True, False)
                coords = location.get_coord(exifData)
                zipcode = location.coord_to_zip(coords,Google_API)
                print "\tOriginal image data: ("+exifData['gps gpslatitude'][1:-1]+","+exifData['gps gpslongitude'][1:-1]+")\n"
                secondcoords = location.zip_to_coord(zipcode,Google_API)
                print "\tOriginal Coordinates: (" + str(coords[0]) + "," + str(coords[1]) + ")\n"
                print "\tFetched Coordinates: (" + str(secondcoords[0]) + "," + str(secondcoords[1]) + ")\n"
                if(secondcoords==(0.0,0.0)):
                        print "\tError fetching Coordinates\n"
                        return 0
                else:
                        if( ( (coords[0] > (secondcoords[0]+0.5)) | (coords[0] < (secondcoords[0]-0.5))) & ( (coords[1] > (secondcoords[1]+0.5)) | (coords[1] < (secondcoords[1]-0.5) ) )  ):
                                print "\tFetched Coordinates are not within +-0.5 accuracy to Original Coordinates"
                                return 0
                        else:
                                print "\tFetched Coordinates are within +-0.5 accuracy to Original Coordinates"
                                return 1
        else:
                print "Image failed a restriction test.\n"
                return 0

def test_sun_position(filename):
        if(image_restriction_main.check_image(filename)):
                imagedata = Data(filename)
                exifData = imagedata.get_exif(filename, True, False)
                print "\tThe sun's position indicates it's : "+location.sun_position(exifData)
                return 1
        else:
                print "\tImage failed a restriction test.\n"
                return 0

