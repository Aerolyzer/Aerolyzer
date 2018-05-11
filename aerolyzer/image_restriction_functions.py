'''
Image Restriction Function File
Description: This file contains all functions for the verifying image restrictions.
'''
import os
import re
import cv2
import yaml
from datetime import datetime
import exifread
import numpy as np

class imgRestFuncs(object):
    'Class containing all image restriction functions'


    def __init__(self, confPath):
        restrict_conf = {'imgLengthMax': 6000, 'imgWidthMin': 100, 'acceptedFileTypes': ['.jpeg', '.jpg', '.png', '.JPG'], 'acceptedMobileDevices': ['iPhone 5', 'iPhone 5s', 'iPhone 6', 'iPhone 6s', 'DROIDX', 'SM-G730V', 'iPhone SE', 'SM-G920V'], 'imgMaxSizeNumber': 4000000, 'imgWidthMax': 6000, 'imgLengthMin': 100}
        if os.path.exists(confPath + "/config/image_restriction_conf.yaml"):
            self.criteria = self._import_yaml(confPath + "/config/image_restriction_conf.yaml")
        else:
            if not os.path.exists(confPath + "/config/"):
                os.makedirs(confPath + "/config/")
            with open(confPath + "/config/image_restriction_conf.yaml", 'w') as outfile:
                yaml.dump(restrict_conf, outfile, default_flow_style=False)
        self.criteria = self._import_yaml(confPath + "/config/image_restriction_conf.yaml")


    def sigm(self, x):
        '''
        Purpose:        sigmoid function that takes in a value and returns a value from 0 to 1
        Inputs:         float
        Outputs:        None
        Returns:        Float between 0, 1
        Assumptions:    N/A
        '''
        return 1 / (1 + np.exp(-x))

    def is_device(self, device):
        '''
        Purpose:        The purpose of this function is to determine whether or not the device the
                        image was taken on is an accepted mobile device.
        Inputs:         string device
        Outputs:        None
        Returns:        Boolean
        Assumptions:    N/A
        '''
        if device in self.criteria['acceptedMobileDevices']:
            return True
        else:
            return False



    def is_edited(self, modified, created):
        '''
        Purpose:        The purpose of this function is to determine whether or not the image was
                        altered from its original form. I.e. do the modification and creation dates coincide.
        Inputs:         datetime created, datetime modified
        Outputs:        None
        Returns:        Boolean
        Assumptions:    N/A
        '''
        if (created == modified):
            return True
        else:
            return False


    def is_landscape(self, pathname):
        '''
        Purpose:        The purpose of this function is to determine whether or not the image
                        contains a direct landscape with sky and view.
        Inputs:         pathname for image 
        Outputs:        None
        Returns:        Boolean
        Assumptions:    N/A
        '''
        img = cv2.imread(pathname,1)
        return self._is_sky(img)


    def is_size(self, fileSize):
        '''
        Purpose:        The purpose of this function is to determine whether or not the size of
                        the image is less than or equal to 200kb.
        Inputs:         dict exifData, int imgMaxSize, int imgMaxSizeBytesShort,
                        string fileSize
        Outputs:        None
        Returns:        Boolean
        Assumptions:    N/A
        '''
        if(fileSize > self.criteria['imgMaxSizeNumber']):
            return False
        else:
            return True


    def is_type(self, fileType):
        '''
        Purpose:        The purpose of this function  is to determine whether or not the image is
                        an accepted file type.
        Inputs:         string fileType
        Outputs:        None
        Returns:        Boolean
        Assumptions:    N/A
        '''
        if fileType in self.criteria['acceptedFileTypes']:
            return True
        else:
            return False


    def is_res(self, imageWidth, imageLength):
        '''
        Purpose:        The purpose of this function is to determine whether or not the image
                        exceeds the minimum resolution.
        Inputs:         int imageWidth, int imageLength
        Outputs:        None
        Returns:        Boolean
        Assumptions:    N/A
        '''
        if (imageWidth >= self.criteria['imgWidthMin']) and (imageLength >= self.criteria['imgLengthMin']):
            if (imageWidth <= self.criteria['imgWidthMax']) and (imageLength <= self.criteria['imgLengthMax']):
                return True
        else:
            return False


    def _is_sky(self, img):
        '''
        Purpose:        The purpose of this function is to determine whether or not the image contains
                        a valid sky or not. 
        Inputs:         numpy.ndarray (loaded image information)
        Outputs:        None
        Returns:        Boolean (valid or invalid image)
        Assumptions:    N/A
        '''

        syn0 = np.array([[0.6106635051820115, -1.2018987127529588, -10.344605820189082, 1.1911213385074928, -6.818421664371254, 0.7888012143578024, 0.1930026599192343, 2.3468732267729644, -0.8629627172245428, -4.855127665505846, -8.782456796605247, -6.495787542595586, -1.42453153150294, -0.91145196348796, -0.34523737705411006],
[-1.3963274415314406, -1.4612339780784143, -2.9000212540397685, -3.9905541370795463, -3.4490261869089287, -4.30542395055999, -2.6069427860345145, 7.201038210239841, -2.205826668689026, -2.493364425571145, -1.9813891706545306, -2.235792731073901, -7.475941696773453, -2.68683663270719, 4.173252030927632], 
[-0.5585916670209942, 0.3126863684210608, 2.142283443670229, 0.6422582372446218, 0.8699959804142926, 1.2677877625877656, 0.697665181045127, -4.116900256696914, 0.8735456225659666, -0.842712533453469, 1.1200739327640843, -0.703797233889045, 3.3491098693459187, 1.1383933429060538, -1.1608021413621255], 
[-0.0272945986039962, 1.3810803094898392, -0.3000751044667501, 0.530598483693932, -0.25230337237162953, 1.227322205409595, 0.7475404385595492, -4.708759516668004, 1.5170799948290143, -1.309427991379729, 0.13045771401578515, -1.2421270434590852, 5.141812566546993, 1.7478932634716013, -1.230678486397662], 
[-1.5471106279095554, -2.524731157065115, 1.0015792402542971, -3.649008251507766, -0.43193380458921354, -3.64779032623984, -1.2585955585366164, 7.075627752142407, -2.3434697661076553, -0.17324616725164094, 0.012324380796953634, 0.1201495802730507, -6.468182569926108, -1.0450745719122267, 3.1541002784637886], 
[0.5316498085997584, 1.8187154828158774, 0.6800840386512677, 3.154341773471645, -0.633596948312113, 2.770528037922082, 0.22043514814321089, -7.246507554283216, 1.3361606503168058, -1.8011391721619912, -0.7156002807301286, -0.37783520885870486, 6.373115811402003, 0.22971478266471973, -2.857966397739584]])
        syn1 = np.array([[5.177044095570317], 
[6.5898220063556], 
[-20.881638524287233], 
[8.880383432994854], 
[-14.676726398416983], 
[9.192745916291782], 
[5.80497325212264], 
[-16.424434027307676], 
[6.820380663953862], 
[-9.664844259044122], 
[-17.73177812938899], 
[-11.809681114121691], 
[14.747050641950713], 
[6.009983025197835], 
[-9.571035518824162]])
        mask = np.zeros(img.shape[:2], np.uint8)
        mask[0:(img.shape[0] / 2), 0:img.shape[1]] = 255
        masked_img = cv2.bitwise_and(img, img, mask = mask)

        # Create histograms with 16 bins in range 0-255
        color = ('b', 'g', 'r')
        b, g, r = cv2.split(img)
        dimy, dimx = img.shape[:2]

        largest = [0, 0]
        it = dimy / 200 #iterations = total number of rows(pixels) / 200
        for i in range(dimy / 6, (dimy / 6) * 5, it):   #only looking at the middle half of the image
            ravg = (sum(r[i]) / float(len(r[i])))
            gavg = (sum(g[i]) / float(len(g[i])))
            bavg = (sum(b[i]) / float(len(b[i])))
            avg = (ravg + gavg + bavg) / 3
            pravg = (sum(r[i - it]) / float(len(r[i - it])))
            pgavg = (sum(g[i - it]) / float(len(g[i - it])))
            pbavg = (sum(b[i - it]) / float(len(b[i - it])))
            pavg = (pravg + pgavg + pbavg) / 3
            diff = pavg - avg
            if diff > largest[0]:   #only getting the largest intensity drop.
                largest = [diff,i-(it/2)]
        sky = img[0:largest[1], 0:dimx]#cropping out landscape
        h1 = sky[0:(sky.shape[0] / 2), 0:dimx]#top half of sky
        h2 = sky[(sky.shape[0] / 2):(sky.shape[0]), 0:dimx]#bottom half
        mask1 = np.zeros(h1.shape[:2], np.uint8)
        mask1[0:(h1.shape[0] / 2), 0:h1.shape[1]] = 255
        hist1 = [0,0,0]
        hist2 = [0,0,0]
        max1 = [0,0,0]
        max2 = [0,0,0]
        for i,col in enumerate(color):
            hist1[i] = cv2.calcHist([h1], [i], mask1, [255], [0, 255])
            max1[i] = np.argmax(hist1[i][6:250])
    
        mask2 = np.zeros(h2.shape[:2], np.uint8)
        mask2[0:(h2.shape[0] / 2), 0:h2.shape[1]] = 255
        for j,col in enumerate(color):
            hist2[j] = cv2.calcHist([h2], [j], mask2, [255], [0, 255])
            max2[j] = np.argmax(hist2[j][6:250])
        X = np.array([float(max1[0])/255., float(max1[1])/255., float(max1[2])/255., float(max2[0])/255., float(max2[1])/255., float(max2[2])/255.])
        l1dup = self.sigm(np.dot(X,syn0))
        l2dup = self.sigm(np.dot(l1dup,syn1))
        if float(l2dup) >= 0.5:
            return True
        return False 



    def _import_yaml(self, confFile):
        '''
        Purpose:        The purpose of this function is to import the contents of the configuration file.
        Inputs:         string conf_file
        Outputs:        None
        Returns:        reference to configuration file
        Assumptions:    N/A
        '''
        with open(confFile, 'r') as f:
            doc = yaml.load(f)
            f.close()
        return doc
