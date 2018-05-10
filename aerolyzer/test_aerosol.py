'Aerosol.py tests'
import time
import numpy as np
import aerosol
aero = aerosol.AeroData("./images/img6.jpg")

def test_all():
    '''
    Purpose:        runs all test functions
    Inputs:         None
    Outputs:        Prints the number of tests that were passed
    Returns:        None
    Assumptions:    N/A
    '''
    testspassed = 0
    numtests = 0
    if test_analyzeWavelength() == 1:
        print "test_analyzeWavelength() passed\n"
        testspassed += 1
        numtests += 1
    else:
        numtests += 1
        print "test_analyzeWavelength() failed\n"
    if test_aerolyzeImage() == 1:
        print "test_aerolyzeImage() passed\n"
        testspassed += 1
        numtests += 1
    else:
        numtests += 1
        print "test_aerolyzeImage() failed\n"
        print "Number of Tests passed " + str(testspassed) + "/" + str(numtests) + "\n"

def test_analyzeWavelength():
    '''
    Purpose:        Calls analyzeWavelength
    Inputs:         None
    Outputs:        Prints the result of analyzeWavelength
    Returns:        1 if passed
    Assumptions:    N/A
    '''
    rand = np.random.random() * 1000.0
    wavelength = 300.0 + rand
    print aero.analyzeWavelength(wavelength)
    return 1

def test_aerolyzeImage():
    '''
    Purpose:        Calls aerolyzeImage
    Inputs:         None
    Outputs:        Prints the result of aerolyzeImage, Prints the runtime of aerolyzeImage
    Returns:        1 if passed
    Assumptions:    N/A
    '''
    t0 = time.time()
    print aero.aerolyzeImage()
    t1 = time.time()
    total_n = t1 - t0
    print "readHazeLayer runtime: " + str(total_n)
    return 1

test_all()
