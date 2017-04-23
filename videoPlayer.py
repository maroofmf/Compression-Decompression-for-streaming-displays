'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
from tkinter import *
from PIL import Image, ImageTk
import math
import sys
from videoData import videoData
import time

class videoPlayer(videoData):

    # Constructor:
    def __init__(self,FILENAME,HEIGHT,WIDTH,CHANNELS):
        videoData.__init__(self,FILENAME,HEIGHT,WIDTH,CHANNELS)
        self.root = Tk()
        self.imageFrame = Frame(self.root)
        self.imageFrame.pack()
        self.panel = Label(self.imageFrame)
        self.root.after(1000,self.nextFrame)
        self.index = 0
        self.root.mainloop()

#-----------------------------------------------------------------------------------------------#
    def nextFrame(self):

        if(self.index ==self.totalFrames):
            sys.exit(0)
        self.img = ImageTk.PhotoImage(Image.fromarray(self.getFrame(self.index)))
        self.panel.config(image = self.img)
        self.panel.pack()
        self.index +=1
        self.root.after(33,self.nextFrame)

#-----------------------------------------------------------------------------------------------#
# Boilerplate code:

if __name__ == '__main__':
	a = videoPlayer('oneperson_960_540.rgb',540,960,3)
