from aerolyzer import location
from aerolyzer import retrieve_image_data

mytest = RtrvData()
exifdict = mytest.get_exif("/home/aero/Documents/Aerolyzer/Aerolyzer/aerolyzer/images/img1.jpg",True,True)
coords = get_coords(exifdict)
print coords


