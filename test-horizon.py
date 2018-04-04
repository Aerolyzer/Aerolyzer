from horizon import is_sky
import numpy as np
from os import listdir
from os.path import isfile, join
pics = [f for f in listdir("./images/good-images/") if isfile(join("./images/good-images/", f))]
good = 0
bad = 0


for i in pics:
    print "./images/good-images/" + i
    if is_sky(i, "./images/good-images/" + i):
        good = good + 1
    else:
        bad = bad + 1

print 'valid horizon detection is', percent, 'accurate.'

pics = [f for f in listdir("./images/false-images/") if isfile(join("./images/false-images/", f))]

for i in pics:
    print "./images/false-images/" + i
    if is_sky(i, "./images/false-images/" + i):
        bad = bad + 1
    else:
        good = good + 1

percent = float(float(good) / float(good+bad))*100.
print 'invalid horizon detection is', percent, 'accurate.'

