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
nbackprob = 0.5
imgext = (".jpg", ".jpeg", ".png", ".gif")
changeinterval = 0.5
root = '/Users/trondarildtjstheim/Dropbox/kode/python/project_course_rhythm'
start = True
logfilename = "data_" + unicode(datetime.datetime.now()) + ".csv"
imgnames=[]
images=[]
dque = collections.deque()
nbacknum=0
fadecounter = 0
imgix = 0
fadestep = 0.15
def writeToLogFile(sentence, logfilename):
	# make logitem
	now = datetime.datetime.now()
	logitem = unicode(now) + "," + sentence
	# write sentence to logfile
	with open(logfilename, "a") as myfile:
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
	
	fadeval = 255*sin(fadecounter)
	tint(255, fadeval)
	fadecounter +=fadestep
	print fadeval
	return map(fadeval, -255, 255, 0, 1)


def setup():
	global imgnames
	imgnames = getImageNames(root)
	# need this to use the global variable
	global images
	images = loadImages(imgnames)
	background(0)
	size(1024, 768, fullscreen=True)

def draw():
	if(start):
		# get a random image, same as nback with prob p
		# fade in
		background(0);
		
		global dque
		global nbacknum
		global imgix

		fadeval = fade()
		print fadeval
		if (fadeval <= 0.01):
			imgix = random.randint(0, len(images)-1)
			# change imageix	
			if len(dque) >= nback:
				nbackix = dque.pop()
				imgix,nbackcnt = getProbIndex(nbackix, nbackprob, len(images))
				nbacknum+=nbackcnt
		print imgix
		print len(images)
		f = images[imgix]
		
		image(f, width/2-f.width/2, height/2-f.height/2)
		# fade out
		if (fadeval>=0.99):
			sleep(changeinterval)
		writeToLogFile(imgnames[imgix]+","+str(nbacknum), logfilename)
		dque.appendleft(imgix)
run()

'''
if __name__ == '__main__':
	writeToLogFile("img-1", logfilename)
	writeToLogFile("img-2", logfilename)
'''
