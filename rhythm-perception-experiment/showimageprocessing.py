#
# use pyprocessing
#

from pyprocessing import *
import datetime
import os
import random
from time import sleep
import numpy as np
import collections

# parameters
nback = 2
# probability of changing to a new image or using the n-back image
nbackprob = 0.5
imgext = (".jpg", ".jpeg", ".png", ".gif")
changeinterval = 0.5

# 
imgroot = "./images/"

timeformatstr = "%Y-%m-%d_%H:%M:%S"
logfilename = "data_" + datetime.datetime.now().strftime(timeformatstr) + ".csv"
logfiledir = "./logs"
# difference in alpha value for each fade step
fadestep = 0.15
startimgname = "startimage.png"
startimage = loadImage(startimgname)

# globals
imgnames=[]
images=[]
dque = collections.deque()
start = False
nbacknum=0
fadecounter = 0
imgix = 0
imgchanged = False

SPACE=32
RETURN=13
ENTER=10

def writeToLogFile(sentence, logfilename):
	# make logitem
	now = datetime.datetime.now().strftime(timeformatstr)
	logitem = now + "," + sentence
	# write sentence to logfile
	with open(os.path.join(logfiledir,logfilename), "a") as myfile:
		myfile.write(logitem+"\n")

def getImageNames(root):
	imagenames=[]
	for path, subdirs, files in os.walk(root):
		for name in files:
			if name.endswith(imgext):
				imagenames.append(os.path.join(path, name))
	return imagenames

def loadImages(imagenames):
	# load all images in path
	retval = []
	for name in imagenames:
		retval.append(loadImage(name))
	return retval

def getProbIndex(default, prob, max):
	# return default with probability prob,
	# or a random number from 0 to max
	dodefault = np.random.multinomial(1, [prob, 1-prob])[0]
	# make a list to draw from which doesnt contain default
	lst = [i for i in range(max) if i!=default]

	if dodefault:
		return default, 1
	else:
		return random.choice(lst), 0

def fade():
	# global transparency
	global fadecounter
	
	fadeval = 255*map(sin(fadecounter), -1,1,0,1)
	#print fadeval
	tint(255, fadeval)
	fadecounter +=fadestep
	return map(fadeval, 0, 255, 0, 1)


def setup():
	global imgnames
	imgnames = getImageNames(imgroot)
	# need this to use the global variable
	global images
	images = loadImages(imgnames)
	
	# initialize first image and add to nback queue
	global imgix
	imgix = random.randint(0, len(images)-1)
	global dque
	dque.appendleft(imgix)
	writeToLogFile(imgnames[imgix]+","+str(nbacknum), logfilename)
	background(0)
	size(1024, 768, fullscreen=False)

def draw():
	background(0);

	if(start):
		# get a random image, same as nback with prob p
		# fade in
		
		global dque
		global nbacknum
		global imgix
		global imgchanged

		fadeval = fade()
		#print fadeval
		if fadeval <= 0.01 and not imgchanged :			
			# change imageix	
			if len(dque) >= nback:
				# pop from right side of queue
				nbackix = dque.pop()
				imgix,nbackcnt = getProbIndex(nbackix, nbackprob, len(images))
				nbacknum += nbackcnt
				imgchanged = True
			else:
				imgix = random.randint(0, len(images)-1)

			writeToLogFile(imgnames[imgix]+","+str(nbacknum), logfilename)
			# image changed so append to queue
			dque.appendleft(imgix)
		elif imgchanged and fadeval >= 0.01:
			imgchanged = False

		#print imgix
		f = images[imgix]
		
		image(f, width/2-f.width/2, height/2-f.height/2)
		# fade out
		if (fadeval>=0.99 and not imgchanged):
			sleep(changeinterval)
	else:
		image(startimage, width/2-startimage.width/2, height/2-startimage.height/2)

def keyPressed():
	if(key.code == SPACE or key.code == ENTER or key.code == RETURN):
		print "starting"
		global start
		start = True


run()

'''
if __name__ == '__main__':
	#print loadImages(getImageNames(root))
	writeToLogFile("img-1", logfilename)
	writeToLogFile("img-2", logfilename)

	#while fadecounter<20:
	#	fade()
'''