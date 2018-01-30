from retrieve_image_data import RtrvData as Data
import location
from image_restriction_functions import imgRestFuncs as imgRestric

mytest = Data("./")
restrictest = imgRestric()
exifdict = mytest.get_exif("/home/aero/Documents/Aerolyzer/Aerolyzer/aerolyzer/images/img3.JPG",True,True)
print exifdict
coord = location.get_coord(exifdict)
print coord
ZIP = location.coord_to_zip(coord)
print ZIP
coord2 = location.zip_to_coord(ZIP)
print coord2
print location.sun_position(exifdict)
