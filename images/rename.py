import os

for filename in os.listdir("."):
		if filename.endswith(".jpg"):
			print "Renaming " + filename + " to "+filename+"A.jpg"
			os.rename(filename, filename+"_A.jpg")	

i = 0
print "Number of images: "+str(len(os.listdir(".")))
for filename in os.listdir("."):
	if (str(i)+".jpg") not in os.listdir("."):
		if filename.endswith(".jpg"):
			print "Renaming " + filename + " to " +str(i)+".jpg"
			os.rename(filename, str(i)+".jpg")
	i+=1