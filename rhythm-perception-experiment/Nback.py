# -*- coding: utf-8 -*-
"""
Created on Wed May 07 13:01:56 2014

@author: Fisksallad
"""
from psychopy import core, event, visual
from PIL import Image 
import time
import numpy as np
import random

#Varibles used
interval = 1.5
N = 2
chance = 0.3
trials = 10

def Nback(interval, N, chance, trials):
   # Creating arrays for control data
   pictureData = np.zeros(trials)  # This will contain the data of all pictures presented
   Nnumber = 0  # This will show the number of positive N-backs
   
   #These will be used for fixing fade in and fade out timing
   frequency = 60  # This is the refresh rate of the computer screen, this is needed because the fade-in and fade-out requires a change of value per refresh
   frames = interval*frequency
   fadeInFrame = frames/4
   opacityFrame = 1.0/ fadeInFrame
   fadeInFrame = int(round(fadeInFrame))
   
   # Creating a text file to record
   data = open("data " + time.strftime("%m%d%I%M") + ".txt","w") 
   
   # Creating a window and loading image stimuli, right now I just have three.
   win = visual.Window(size=(1280, 1024), 
      fullscr = True , 
      color = (0.5,0.5,0.5)) 
   pic1 = Image.open("./goalie.jpeg")
   pic2 = Image.open("./img-2.png")
   pic3 = Image.open("./img-3.png")
   image = [0,0,0]
   image[0] = visual.ImageStim(win, image = pic1, opacity = 0)
   image[1] = visual.ImageStim(win, image = pic2, opacity = 0)
   image[2] = visual.ImageStim(win, image = pic3, opacity = 0)
   
   # Defining initial instruction
   instruktion = visual.TextStim(win, text="Tryck space for att starta!")
   
   # Drawing the window and instructions
   instruktion.draw()
   win.flip()
   
   # Waiting for start button
   event.waitKeys()
       
   # Actual loop
   for i in range(0,trials):
       sample = random.randint(0, 2)
       timer = core.CountdownTimer(interval)
       while  timer.getTime() > 0:
           while image[sample].opacity < 1:
               image[sample].opacity += opacityFrame 
               image[sample].draw()
               win.flip()
           for n in range(0,fadeInFrame*2):
               image[sample].opacity = 1
               image[sample].draw()
               win.flip()       
           while image[sample].opacity > 0:
               image[sample].opacity -= opacityFrame
               image[sample].draw()
               win.flip()
       image[sample].opacity = 0
       image[sample].draw()
       win.flip()
       pictureData[i] = sample
       if i >= 2 and pictureData[i] == pictureData[i - 2]:
           Nnumber = Nnumber + 1
       data.write(str(sample) + "   " + str(Nnumber))  # The first value is the type of picture, the second shows the cumulative number of positive N-backs
       data.write("\n")
       core.wait(0.5)
   win.close() 
   core.quit()
   

Nback(interval,N,chance, trials)
