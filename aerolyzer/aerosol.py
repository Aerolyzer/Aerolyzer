'''
Aerosol Analysis Class
Description: This file contains the AeroData class which takes an image and analyses the colors present.
'''
import math
import scipy.stats as stats
import retrieve_image_data
import wavelength as wave

class AeroData(object):
    'Class containing all aerosol analysis functions'

    def __init__(self, pathname):
        '''
        Class Constructor
        Inputs: pathname(location of the image being analyzed)
        '''
        self.imagePath = pathname
        self.imager = retrieve_image_data.RtrvData(pathname)
        pass

    def scoreSize(target, minS, maxS):
        '''
        Purpose:        returns the p-score of a value in a given range.
        Inputs:         target(a fraction of the wavelength), minS(smallest size of aerosol type), maxS(largest size of aerosol type)
        Outputs:        a percentage based on the target wavelength's position in a normal distribution between minS and maxS
        Returns:        prob
        Assumptions:    all inputs are floats
        '''
        rangeS = (maxS - minS)
        median = minS + (rangeS / 2.0)
        stddev = rangeS/3.0
        zscore = math.fabs((target - median) / stddev)
        pscore = stats.norm.sf(zscore)
        zscore2 = math.fabs(((target / 10.0) - median) / stddev)
        pscore2 = stats.norm.sf(zscore2)
        prob = math.fabs(pscore - pscore2)
        return prob

    def analyzeWavelength(self, wavelength):
        '''
        Purpose:        Returns relative likelihood of an aerosol's presence given a wavelength.
        Inputs:         wavelength which is a float
        Outputs:        List of tuples in the form (aerosol type, likelihood, anthropogenic)
        Returns:        aerosolList
        Assumptions:    N/A
        '''
        aerosolList = []
        aerosolOut = []
        scatter = wavelength / 1000.0
        aerosolList.append(("fog", self.scoreSize(scatter, .1, 200.0), False))
        aerosolList.append(("cloud", self.scoreSize(scatter, 2.0, 80.0), False))
        aerosolList.append(("cement", self.scoreSize(scatter, 3, 100.0), True))
        aerosolList.append(("seasalt", self.scoreSize(scatter, .02, .5), False))
        aerosolList.append(("coal", self.scoreSize(scatter, 1.0, 100.0), True))
        aerosolList.append(("oilsmoke", self.scoreSize(scatter, .025, 1), True))
        aerosolList.append(("machining", self.scoreSize(scatter, .1, 80.0), True))
        aerosolList.append(("tobacco", self.scoreSize(scatter, .08, 1.4), True))
        aerosolList.append(("diesel", self.scoreSize(scatter, .02, .1), True))
        aerosolList.append(("nuclei", self.scoreSize(scatter, .007, .03), False))
        aerosolList.append(("dust", self.scoreSize(scatter, .05, 1000.0), False))
        aerosolList.append(("biomass", self.scoreSize(scatter, .001, 1.0), True))
        return aerosolList

    def aerolyzeImage(self):
        '''
        Purpose:        Returns information of the aerosol data in the provided image.
        Inputs:         None
        Outputs:        List of the aerosol types sorted from most likely to least likely
        Returns:        aerosolSum
        Assumptions:    this instance of AeroData has been correctly initialized
        '''
        numtypes = 12
        cumulative = []
        pixArray = self.imager.get_hsv(self.imagePath)
        #wave = wavelength.Wavelength()
        for i in pixArray:
            cumulative.append(self.analyzeWavelength(wave.get_wavelength(i, 1)))
        aerosolSum = reduce((lambda x, y: [(x[0][0], x[0][1] + y[0][1], x[0][2]), (x[1][0], x[1][1] + y[1][1], x[1][2]), (x[2][0], x[2][1] + y[2][1], x[2][2]), (x[3][0], x[3][1] + y[3][1], x[3][2]), (x[4][0], x[4][1] + y[4][1], x[4][2]), (x[5][0], x[5][1] + y[5][1], x[5][2]), (x[6][0], x[6][1] + y[6][1], x[6][2]), (x[7][0], x[7][1] + y[7][1], x[7][2]), (x[8][0], x[8][1] + y[8][1], x[8][2]), (x[9][0], x[9][1] + y[9][1], x[9][2]), (x[10][0], x[10][1] + y[10][1], x[10][2]), (x[11][0], x[11][1] + y[11][1], x[11][2])]), cumulative)
        aerosolSum = sorted(aerosolSum, key=lambda aerosol: aerosol[1], reverse=True)
        return aerosolSum
