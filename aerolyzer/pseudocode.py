# '''
# Aerolyzer - Pseudocode
# Feburary 10, 2017


# Image Restrictions:

# Throughout the upload process, images will be required to meet various
# criteria beforee being accepted for aerosol content analysis. To accomplish this
# requirement, a mulititude of functions will be created, each aimed at verifiying
# that a certain restriction has been met. To ensure the simplicity of Aerolyzer's
# initial development, as well as future adaptations, information regarding image criteria
# will be stored in a single file to be referenced by the various restriction functions
# outlined below.
# '''

# '''
# import libraries
# '''
# import re
# import exifread


# '''
# Purpose:        The purpose of this section is to keep all image criteria specifications located in
#                 one place, for simplicity's sake.
# Inputs:         None
# Outputs:        None
# Returns:        None
# Assumptions:    These values will be populated by a developer.
# '''
# acceptedFileTypes = ["JPEG", "JPG", "PNG"]
# acceptedMobileDevices = ["i5", "i5s", "i6", "i6s", "i7"]
# imgMaxSizeNumber = 200;
# imgMaxSizeBytesShort = "kb"
# imgMaxSizeBytesLong = "kilobytes"
# img_sizes_long =  ['0': 'bytes',
#                     '1': 'kilobytes',
#                     '2': 'gigabytes',
#                     '3': 'megabytes',
#                     '4': 'terrabytes']
# img_sizes_short =    ['0': 'b',
#                         '1': 'kb',
#                         '2': 'gb',
#                         '3': 'mb',
#                         '4': 'tb']
# imgWidthMin = xxx;
# imgHeightMin = xxx;
# imgWidthMax = xxx;
# imgHeightMax = xxx;
# imgRestrictionErrorText =  {'accept_device': 'The image must be a mobile image from a supported device',
#                             'is_edited': 'The image cannot be edited or filtered in any way',
#                             'is_landscape': 'The image must be of a direct landscape with a sky and view',
#                             'accept_size': 'The image must be no larger than 200kb',
#                             'accept_file_type': 'The file type of the image must be .jpg or .png',
#                             'accept_resolution': 'The image must be in the resolution range 1X1-1000X1000',
#                             'is_location_services': 'Location services must be enabled for the camera'}

# '''
# Purpose:        The purpose of this function is to determine whether or not the device the
#                 image was taken on is an accepted mobile device.
# Inputs:         dict exifData, list acceptedMobileDevices
# Outputs:        None
# Returns:        Boolean
# Assumptions:    N/A
# '''
# def accept_device(exifData, acceptedMobileDevices):
#     #check to make sure the key-value pair exists in exifData to prevent errors
#     if ('DEVICE' not in exifData.keys()):
#         return false
    
#     if any(exifData['DEVICE'].lower() in device for device in acceptedMobileDevices):
#         return true
#     else:
#         return false


# '''
# Purpose:        The purpose of this function is to determine whether or not the image was
#                 altered from its original form. I.e. do the modification and creation dates coincide.
# Returns:        Boolean
# Assumptions:    N/A
# '''
# def is_edited(exifData):
#     #check to make sure the key-value pair exists in exifData to prevent errors
#     if ('Create Date' not in exifData.keys() or 'Modify Date' not in exifData.keys()):
#         return false
    
#     if (exifData['Create Date'] == exifData['Modify Date']):
#         return true
#     else:
#         return false

# '''
# Purpose:        The purpose of this function is to determine whether or not the image
#                 contains a direct landscape with sky and view.
# Inputs:         dict exifData, ?
# Outputs:        None
# Returns:        Boolean
# Assumptions:    N/A
# '''
# def is_landscape(exifData, ):
#     #UNKNOWN METHOD

# '''
# Purpose:        The purpose of this function is to determine whether or not the size of
#                 the image is less than or equal to 200kb.
# Inputs:         dict exifData, int imgMaxSize
# Outputs:        None
# Returns:        Boolean
# Assumptions:    N/A
# '''
# def accept_size(exifData, imgMaxSizeNumber, imgMaxSizeBytesShort, imgMaxSizeBytesLong, img_sizes_long, img_sizes_short):
#     #check to make sure the key-value pair exists in exifData to prevent errors
#     if('File Size' not in exifData.keys()):
#         return false
  
#     #parse File Size parameter into a list of the numbers, spaces, and letters
#     file_parameters = parse_file_size(exifData['File Size'])
    
#     #check to make sure parsing was successful
#     if(file_parameters == [] or len(file_parameters) != 3):
#         return false
#     else:
#         #Case 1: File Size has same byte-type as the maximum value
#         if(file_parameters[2].lower() == imgMaxSizeBytesShort or file_parameters[2].lower() == imgMaxSizeBytesLong):
#             if(int(file_parameters[0]) <= imgMaxSize):
#                 return true
#             else:
#                 return false
#         else:                
#             #Determine img byte-size key
#             for key, value in img_sizes_long.iteritems()
#                 if value = file_parameters[2].lower():
#                     img_key = key
            
#             for key, value in img_sizes_short.iteritems()
#                 if value = file_parameters[2].lower():
#                     img_key = key
            
#             #Determine accepted img size byte-size key
#             for key, value in img_sizes_short.iteritems()
#                 if value = imgMaxSizeBytes:
#                     accept_img_key = key

#             #Case 2: File Size byte-type is smaller
#             if(img_key < accept_img_key):
#                 return true

#             #Case 3: File Size byte-type is larger
#             elif(img_key > accept_img_key):
#                 return false

#             #Case 4: File Size byte-type unrecognized
#             else:
#                 return false

# '''
# Purpose:        The purpose of this function  is to determine whether or not the image is
#                 an accepted file type.
# Inputs:         dict exifData, list acceptedFileTypes
# Outputs:        None
# Returns:        Boolean
# Assumptions:    N/A
# '''
# def accept_file_type(exifData, acceptedFileTypes):
#     #check to make sure the key-value pair exists in exifData to prevent errors
#     if('File Type' not in exifData.keys()):
#         return false

#     if any(exifData['File Type'].upper() in fileType for fileType in acceptedFileTypes):
#         return true
#     else:
#         return false

# '''
# Purpose:        The purpose of this function is to determine whether or not the image
#                 exceeds the minimum resolution.
# Inputs:         dict exifData, int imgWidthMin, int imgHeightMin
# Outputs:        None
# Returns:        Boolean
# Assumptions:    N/A
# '''
# def accept_resolution(exifData, imgWidthMin, imgHeightMin, imgWidthMax, imgHeightMax):
#     #check to make sure the key-value pair exists in exifData to prevent errors
#     if('Exif Image Width' not in exifData.keys() or 'Exif Image Height'in exifData.keys()):
#         return false
    
#     if (exifData['Exif Image Width'] >= imgWidthMin and exifData['Exif Image Height'] >= imgHeightMin):
#         if (exifData['Exif Image Width'] <= imgWidthMax and exifData['Exif Image Height'] <= imgHeightMax):
#             return true
#     else:
#         return false

# '''
# Purpose:        The purpose of this function is to determine whether or not the image was
#                 taken by a device with location services enabled for the camera.
# Inputs:         dict exifData
# Outputs:        None
# Returns:        Boolean
# Assumptions:    N/A
# '''
# def is_location_services(exifData):
#     if('GPS Latitude' not in exifData.keys() or 'GPS Longitude' not in exifData.keys()):
#         return false
    
#     if (exifData['GPS Latitude'] != '' and exifData['GPS Longitude'] != ''):
#         return true
#     else:
#         return false

# '''
# Purpose:        The purpose of this function is to parse the file_size value into numbers
#                 and letters.
# Inputs:         string file_size
# Outputs:        None
# Returns:        list file_parameters (digits, spaces, letters)
# Assumptions:    N/A
# '''
# def parse_file_size(file_size):
#     match = re.match(r"([0-9]+)(\s*)([a-z]+)$", file_size, re.I)
#     if match:
#         file_parameters = match.groups()
#     else:
#         file_parameters = []
#     return(file_parameters)


# '''
# Purpose:        The purpose of this function is to determine whether or not an image
#                 restriction was passed, and print out the correct error statement accordingly.
# Inputs:         boolean bool, list imgRestrictionErrorText, key error
# Outputs:        None
# Returns:        Error message or blank message
# Assumptions:    N/A
# '''
# def error_message(boolean, imgRestrictionErrorText, error):
#     if(!boolean):
#         return("Restriction Error: %s." % (imgRestrictionErrorText[error]))
#     else:
#         return('')

# '''
# Purpose:        The purpose of this main function is to check all image restrictions and
#                 produce the correct error message should one occur.
# Inputs:         None
# Outputs:        None
# Returns:        N/A
# Assumptions:    N/A
# '''
# def get_exif(path)
#     img = open(path, 'rb')
#     tags = exifread.process_file(img)
#     return tags

# '''
# Purpose:        The purpose of this main function is to check all image restrictions and
#                 produce the correct error message should one occur.
# Inputs:         None
# Outputs:        None
# Returns:        N/A
# Assumptions:    N/A
# '''
# def main():
#     #Retrieve exif data
#     exifData = get_exif(path)

#     #Call each function and check for false return values
#     error_message(accept_device(exifData, acceptedMobileDevices), imgRestrictionErrorText, 'accept_device')
#     error_message(is_edited(exifData), imgRestrictionErrorText, 'is_edited')
#     error_message(is_landscape(exifData), imgRestrictionErrorText, 'is_landscape')
#     error_message(accept_size(exifData, imgMaxSize), imgRestrictionErrorText, 'accept_size')
#     error_message(accept_file_type(exifData, acceptedFileTypes), imgRestrictionErrorText, 'accept_file_type')
#     error_message(accept_resolution(exifData, imgWidthMin, imgHeightMin, imgWidthMax, imgHeighMax), imgRestrictionErrorText, 'accept_resolution')
#     error_message(is_location_services(exifData), imgRestrictionErrorText, 'is_location_services')




# main()
