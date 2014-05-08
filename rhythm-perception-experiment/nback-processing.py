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
logheader = "time,image,nback,sessionid"
# difference in alpha value for each fade step
fadestep = 0.15
startimgname = "startimage.png"
startimage = loadImage(startimgname)
fullscreen = True
# globals
imgnames=[]
images=[]
dque = collections.deque()
start = False
nbacknum=0
fadecounter = 0
imgix = 0
imgchanged = False
sessionid = 0

SPACE=32
RETURN=13
ENTER=10

def writeToLogFile(sentence, logfilename, timestamp=True):
	# make logitem
	logitem = ""
	if timestamp:
		now = datetime.datetime.now().strftime(timeformatstr)
		logitem = now + "," 
	logitem += sentence
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
	writeToLogFile(logheader, logfilename, timestamp=False)
	writeToLogFile(imgnames[imgix] + "," + str(nbacknum) + "," + str(sessionid), logfilename)
	background(0)
	size(1024, 768, fullscreen=fullscreen)

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

			writeToLogFile(imgnames[imgix] + "," + str(nbacknum) + "," + str(sessionid), logfilename)
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
		x = width/2
		y = height/2
		tint(255,255)
		image(startimage, x - startimage.width/2, y - startimage.height/2)
		textSize(32);
		fill(127)
		sessionstr = "Next session id = " + str(sessionid+1)
		strwidth = textWidth(sessionstr)
		text(sessionstr, x - strwidth/2, y + startimage.height); 

def keyPressed():
	if(key.code == SPACE or key.code == ENTER or key.code == RETURN):
		if not start:
			global sessionid
			sessionid += 1
			
			global fadecounter
			fadecounter = 0
			
			print "starting session " + str(sessionid)
		global start
		start = not start


run()

'''
if __name__ == '__main__':
	#print loadImages(getImageNames(root))
	writeToLogFile(logheader, logfilename, False)
	writeToLogFile("img-2", logfilename)

	#while fadecounter<20:
	#	fade()
'''
