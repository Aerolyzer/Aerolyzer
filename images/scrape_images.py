"""modules"""
import sys
import urllib.request, urllib.parse, urllib.error
from collections import namedtuple
import time
import re
import json
from bs4 import BeautifulSoup

RETRIEVE_FROM = 'https://www.wunderground.com/wximage/'
P_TAGS = "(<p>|<\/p>)"
IMAGE_TYPE = ".jpg"

if __name__ == '__main__':
    print("Starting retrieval")
    if len(sys.argv) > 1:
        RETRIEVE_FROM = sys.argv[1]
    ImageData = namedtuple('ImageData', 'file, img, link, date, categories')
    IMG_FIELDS = ['file', 'img', 'link', 'date', 'categories']
    DATA_LIST = []
    URL = urllib.request.urlopen(RETRIEVE_FROM).read()
    soup = BeautifulSoup(URL, "lxml")
    links = soup.findAll('a', class_='photo-link')
    print("Following image links")
    print("     Found %d links" % (len(links)))
    i = 1
    for link in links:
        full_link = "https://www.wunderground.com/" + link.get('href')
        URL = urllib.request.urlopen(full_link).read()
        soup = BeautifulSoup(URL, "lxml")
        images = soup.findAll('img')
        date = soup.findAll('p')[4]
        categories = soup.findAll('a', class_="panel category radius")
        full_category = ""
        for category in categories:
            full_category = full_category + category.text + ","
        full_date = re.sub(P_TAGS, "", str(date))
        for image in images:
            full_image = image.get('data-interchange')
            if full_image is not None:
                full_image = "https:" + image.nextSibling.nextSibling.img['src']
                # print "     %s" % (full_image)
                filename = str(int(time.time())) + "_" + str(i) + "_" + full_image.split('/')[-1]
                if filename.endswith(IMAGE_TYPE):
                    i = i + 1
                    data = ImageData(filename, full_image, full_link, full_date, full_category[:-1])
                    DATA_LIST.append(data)
    print("Writing to file and downloading images")
    DATA_FILE = open('image_data' + str(int(time.time())) + ".txt", 'w')
    for data in DATA_LIST:
        # print "     " + data.file
        urllib.request.urlretrieve(data.img, data.file)
        DATA_FILE.write(json.dumps(dict(list(zip(IMG_FIELDS, data))), sort_keys=True, indent=4))
    DATA_FILE.close()
    print("Done")
