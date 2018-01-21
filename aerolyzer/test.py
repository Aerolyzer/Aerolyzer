from retrieve_image_data import RtrvData as Data
import location

mytest = Data("./")
exifdict = mytest.get_exif("/home/aero/Documents/Aerolyzer/Aerolyzer/aerolyzer/images/img3.JPG",True,True)
print location.get_coord(exifdict)
print exifdict



