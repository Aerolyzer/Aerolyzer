from horizon import is_sky
from os import listdir
from os.path import isfile, join
pics = [f for f in listdir("./images/good-images/") if isfile(join("./images/good-images/", f))]
good = 0
bad = 0
for i in pics:
    if is_sky(i, "./images/good-images/" + i):
        good = good + 1
    else:
        bad = bad + 1

percent = float(float(good) / float(good+bad))*100.
print 'horizon detection is', percent, 'accurate.'
