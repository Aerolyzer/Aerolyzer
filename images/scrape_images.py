"""modules"""
import sys
import urllib
from collections import namedtuple
import time
import re
from bs4 import BeautifulSoup

RETRIEVE_FROM = 'https://www.wunderground.com/wximage/imagegallery'
P_TAGS = "(<p>|<\/p>)"
IMAGE_TYPE = ".jpg"

if __name__ == '__main__':
    print "Starting retrieval"
    if len(sys.argv) > 1:
        RETRIEVE_FROM = sys.argv[1]
    ImageData = namedtuple('ImageData', 'img, link, date')
    DATA_LIST = []
    URL = urllib.urlopen(RETRIEVE_FROM).read()
    soup = BeautifulSoup(URL, "lxml")
    links = soup.findAll('a', class_='photo-link')
    print "Following image links"
    print "     Found %d links" % (len(links))
    for link in links:
        full_link = "https://www.wunderground.com/" + link.get('href')
        URL = urllib.urlopen(full_link).read()
        soup = BeautifulSoup(URL, "lxml")
        images = soup.findAll('img')
        date = soup.findAll('p')[4]
        full_date = re.sub(P_TAGS, "", str(date))
        for image in images:
            full_image = image.get('data-interchange')
            if full_image is not None:
                full_image = "https:" + image.nextSibling.nextSibling.img['src']
                # print "     %s" % (full_image)
                data = ImageData(full_image, full_link, full_date)
                DATA_LIST.append(data)
    print "Writing to file and downloading images"
    DATA_FILE = open('image_data' + str(int(time.time())) + ".txt", 'w')
    DATA_FILE.write("Date taken\tFilename\tImage source\tPage link\n")
    i = 1
    for data in DATA_LIST:
        filename = str(int(time.time())) + "_" + str(i) + "_" + data.img.split('/')[-1]
        if filename.endswith(IMAGE_TYPE):
            # print "     " + filename
            urllib.urlretrieve(data.img, filename)
            DATA_FILE.write(data.date + "\t" + filename + "\t" + data.img + "\t" + data.link + "\n")
            i = i + 1
    DATA_FILE.close()
    print "Done"
