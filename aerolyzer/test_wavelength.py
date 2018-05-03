import math
import cv2
import numpy as np
import wavelength
import time


def test_all():
    testspassed = 0
    numtests  = 0
    if test_comparisonArray() == 1:
        print "test_comparisonArray() passed\n"
        testspassed += 1
        numtests += 1
    else:
        numtests += 1
        print "test_comparisonArray() failed\n"
    if test_get_wavelength() == 1:
        print "test_get_wavelength() passed\n"
        testspassed += 1
        numtests += 1
    else:
        numtests += 1
        print "test_get_wavelength() failed\n"
    if compare_bgr_hsv()==1:
        print "compare_bgr_hsv() passed\n"
        testspassed += 1
        numtests += 1
    else:
        numtests += 1
        print "compare_bgr_hsv() failed\n"

    print "Number of Tests passed "+ str(testspassed) +"/"+str(numtests)+"\n"


def test_comparisonArray():
    BGR = wavelength.comparisonArray(0)
    HSV = wavelength.comparisonArray(1)
    Duplicount = 0
    for i in range(len(BGR)):
        if(BGR[i][0] == HSV[i][0]):
            if(BGR[i][1] == HSV[i][1]):
                if(BGR[i][2] == HSV[i][2]):
                    print "["+str(i)+"][0]: "+str(BGR[i][0])+" ["+str(i)+"][1]: "+str(BGR[i][1])+" ["+str(i)+"][2]: "+str(BGR[i][2])
                    Duplicount += 1
                    print "Duplicount: "+str(Duplicount)
    if (Duplicount > 20): return 0
    return 1

def test_get_wavelength():
    targetWave = 504
    waveRange = 400
    BGR = wavelength.get_wavelength([97, 255, 0], 0)
    print ""
    HSV = wavelength.get_wavelength([71, 255, 255], 1)
    print "Target Wavelength: " + str(targetWave)
    print "BGR Wavelength: " + str(BGR) + " HSV wavelength: " + str(HSV)
    BGRAccuracy = (1-((math.fabs(BGR - targetWave))/waveRange))*100
    HSVAccuracy = (1-((math.fabs(HSV - targetWave))/waveRange))*100
    print "BGR Accuracy: " + str(BGRAccuracy) + "%   HSV Accuracy: " + str(HSVAccuracy) + "%"
    diff = math.fabs(BGR-HSV)
    if (diff<15):
        return 1
    return 0

def compare_bgr_hsv():
    n = 10000
    testBGRColors = []
    testHSVColors = []
    BGRResult = []
    HSVResult = []
    for k in range(n):
        testBGRColors.append([(k%255), ((k+(k*2))%255), ((k+(k*3))%255)])
        testHSVColors.append([(k%180), ((k+(k*2))%255), ((k+(k*3))%255)])
    t0 = time.time()
    for i in range(n): BGRResult.append(wavelength.get_wavelength(testBGRColors[i], 0))
    t1 = time.time()
    total_n = t1-t0
    BGRtime = total_n

    t2 = time.time()
    for j in range(n): HSVResult.append(wavelength.get_wavelength(testHSVColors[j], 1))
    t3 = time.time()
    total_n = t3-t2
    HSVtime = total_n

    print "BGR 10000x run time: "+ str(BGRtime) +"\n"+"HSV 10000x run time: "+ str(HSVtime) +"\n"
    if(BGRtime != HSVtime):
        return 1
    return 0
