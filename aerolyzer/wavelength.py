import math
import cv2


def comparisonArray(mode):
    img = cv2.imread('./images/Spectrum1pixel.png')
    bgr = []
    hsv = []
    i = 0
    if mode == 0:
        while i < (img.shape[1]):
            bgr.append(img[0, i])
            i += 1
        return bgr
    else:
        hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        while i < (hsvimg.shape[1]):
            hsv.append(hsvimg[0, i])
            i += 1
        return hsv

def get_wavelength(abc, mode):
    a_diff = 0
    b_diff = 0
    c_diff = 0
    dist = 0
    best_dist = 2555
    best = 0
    i = 0
    min_wavelength = 380
    ValArray = comparisonArray(mode)
    while i < (len(ValArray) - 1):
        a_diff = math.fabs(ValArray[i][0] - abc[0])
        b_diff = math.fabs(ValArray[i][1] - abc[1])
        c_diff = math.fabs(ValArray[i][2] - abc[2])
        if mode == 1:
            a_diff = a_diff*6
        dist = math.sqrt((a_diff*a_diff)+(b_diff*b_diff)+(c_diff*c_diff))

        if dist < best_dist:
            best = i
            best_dist = dist
        i += 1
    return float(best + min_wavelength)
