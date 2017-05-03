'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
#----------------------------------------------------------------------------------------------------------------#
# Import dependancies:

from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import math
import sys
from videoData import videoData
import time
import os

#----------------------------------------------------------------------------------------------------------------#
# FilePaths:
global playButtonPath
playButtonPath = './metadata/playButton.png'

global playerInitPath
playerInitPath = './metadata/playerInit.jpg'

global pauseButtonPath
pauseButtonPath = './metadata/pauseButton.jpg'

global stopButtonPath
stopButtonPath = './metadata/stopButton.jpg'

global gazeOnButtonPath
gazeOnButtonPath = './metadata/gazeOn.jpg'

global gazeOffButtonPath
gazeOffButtonPath = './metadata/gazeOff.jpg'

#----------------------------------------------------------------------------------------------------------------#
class videoPlayer():

    # Constructor: Initialize GUI
    def __init__(self,FILENAME,HEIGHT,WIDTH,CHANNELS,FRAMERATE = 30,videoFile=None):

        # Initialize videoData:
        if(videoFile):
            self.videoData = videoFile
        else:
            self.videoData = videoData(self,FILENAME,HEIGHT,WIDTH,CHANNELS)

        # Init root
        self.root = Tk()
        self.root.geometry('960x600')

        # Self init;
        self.currentJob = None
        self.frameRate = FRAMERATE
        self.playButtonImage = ImageTk.PhotoImage(Image.open(playButtonPath).resize((40,40),1))
        self.pauseButtonImage = ImageTk.PhotoImage(Image.open(pauseButtonPath).resize((40,40),1))
        self.stopButtonImage = ImageTk.PhotoImage(Image.open(stopButtonPath).resize((40,40),1))
        self.gazeOnButtonImage = ImageTk.PhotoImage(Image.open(gazeOnButtonPath).resize((40,40),1))
        self.gazeOffButtonImage = ImageTk.PhotoImage(Image.open(gazeOffButtonPath).resize((40,40),1))
        self.init_img = ImageTk.PhotoImage(Image.open(playerInitPath).resize((960,540)))

        # Initialize state of player:
        self.playing = False
        self.gazeControl = False
        self.mouseCoordinates = [None,None]
        # Init frames
        self.imageFrame = Frame(self.root)
        self.imageFrame.pack()
        self.buttonFrame = Frame(self.root)
        self.buttonFrame.pack(side=BOTTOM)

        # Initlaize iteratior:
        self.forwardIterator = self.videoData.iterator()

        # Initialize panels
        self.imagePanel = Label(self.imageFrame,image = self.init_img)
        self.imagePanel.pack()
        self.buttonsInit()
        self.mouseStatusInit()
        self.currentBlock_i = None
        self.currentBlock_j = None
        self.currentBlock = None

        # Start program
        self.playJob = None # Play job_id
        self.freezeJob = None # Freeze job_id
        print('\033[1;33m[Status]:Player initialized with PID:%d\033[0m'%(os.getpid()))
        print('\033[1;33m[Status]:Details: Width: %d, Height: %d, FrameRate: %d\033[0m'%(self.videoData.width,self.videoData.height,self.frameRate))
        self.root.bind('<Motion>',self.motion) # Update mouse activities
        self.root.mainloop() # Main loop for GUI

#-----------------------------------------------------------------------------------------------#
# Initialize from videoData instance:

    @classmethod
    def fromVideoFile(cls,dataInstance,FRAMERATE=30):
        return cls(dataInstance.fileName,dataInstance.height,dataInstance.width,dataInstance.channels,FRAMERATE,dataInstance)

#-----------------------------------------------------------------------------------------------#
# Initialize mouse status:

    def mouseStatusInit(self):

        # Set Text Bar:
        self.mouseStatusDisplay = Label(self.buttonFrame,text='Coords: %d,%d'%(0,0))
        self.mouseStatusDisplay.pack(side = LEFT)

#-----------------------------------------------------------------------------------------------#
# Initialize buttons:

    def buttonsInit(self):

        # Play/Pause button:
        self.playButton = Button(self.buttonFrame,image=self.playButtonImage, command = self.playVideo)
        self.playButton.pack(side=LEFT)

        # Stop button:
        self.stopButton = Button(self.buttonFrame,image=self.stopButtonImage, command = self.stopVideo)
        self.stopButton.pack(side =LEFT)

        # Gaze control button
        self.gazeButton = Button(self.buttonFrame,image =self.gazeOffButtonImage ,command = self.gazeToggle)
        self.gazeButton.pack(side = LEFT)


#-----------------------------------------------------------------------------------------------#
# Update mouse:

    def motion(self,event):

        # Set mouse coordinates:
        self.mouseCoordinates[0] = event.x
        self.mouseCoordinates[1] = event.y

        # Filter mouse pointers:
        if(self.mouseCoordinates[0]<0 or self.mouseCoordinates[0]>960):
            self.mouseCoordinates[0] = -1
            self.mouseCoordinates[1] = -1


        if(self.mouseCoordinates[1]<0 or self.mouseCoordinates[1]>540):
            self.mouseCoordinates[0] = -1
            self.mouseCoordinates[1] = -1

        # Get the blocks:
        if(self.mouseCoordinates[0]>-1 or self.mouseCoordinates[1]>-1):
            self.currentBlock_i = self.mouseCoordinates[0]-self.mouseCoordinates[0]%8
            self.currentBlock_j = self.mouseCoordinates[1]-self.mouseCoordinates[1]%8
            self.currentBlock = (self.currentBlock_i//8)+(self.currentBlock_j//8)*(self.videoData.width//8)

        # Update display
        self.mouseStatusDisplay.config(text='Coords: %d,%d,%d'%( self.currentBlock_i, self.currentBlock_j,self.currentBlock))

#-----------------------------------------------------------------------------------------------#
# Toggle gaze control:

    def gazeToggle(self):

        if(self.gazeControl):
            print('\033[0;32m[Status]:Disable Gaze Control\033[0m')
            self.gazeControl = False
            self.gazeButton.config(image=self.gazeOffButtonImage)
            self.gazeButton.pack()
        else:
            print('\033[0;32m[Status]:Enable Gaze Control\033[0m')
            self.gazeControl = True
            self.gazeButton.config(image=self.gazeOnButtonImage)
            self.gazeButton.pack()

#-----------------------------------------------------------------------------------------------#
# Stop button callback function:

    def stopVideo(self):

        # Stop and reset video display:
        print('\033[0;32m[Status]:Stopping the video\033[0m')
        if(self.freezeJob):
            self.root.after_cancel(self.freezeJob)
            self.freezeJob = None

        if(self.playJob):
            self.root.after_cancel(self.playJob)
            self.playJob = None

        # Change button of the pause player;
        self.playing = False
        self.playButton.config(image=self.playButtonImage)
        self.playButton.pack()

        # Refresh the player:
        self.imagePanel.config(image = self.init_img)
        self.imagePanel.pack()
        self.videoData.iteratorIndex = 0

#-----------------------------------------------------------------------------------------------#
# Play/Pause button callback function:

    def playVideo(self):

        if self.playing:
            print('\033[0;32m[Status]:Pausing the video\033[0m')
            self.playing = False
            self.playButton.config(image=self.playButtonImage)
            self.playButton.pack()
            self.freezeFrame()
        else:
            print('\033[0;32m[Status]:Playing the video\033[0m')
            self.playing=True
            self.playButton.config(image=self.pauseButtonImage)
            self.playButton.pack()
            self.sync()

#-----------------------------------------------------------------------------------------------#
# Freeze frame and perform processing:

    def freezeFrame(self):

        if(self.playing):
            self.root.after_cancel(self.freezeJob)
            self.freezeJob = None
            return

        self.img = ImageTk.PhotoImage(Image.fromarray(self.videoData.currentFrame()))
        self.imagePanel.config(image = self.img)
        self.imagePanel.pack()

        # Pause the video
        self.freezeJob = self.root.after(100,self.freezeFrame)

#-----------------------------------------------------------------------------------------------#
# Sync the video:

    def sync(self):

        # Calculate function time for sync
        startTime = time.time()

        self.root.update_idletasks()

        # Check player status:
        if(not self.playing):
            self.root.after_cancel(self.playJob)
            self.playJob = None
            return

        # Update image and pack:
        self.img = ImageTk.PhotoImage(Image.fromarray((next(self.forwardIterator))))
        self.imagePanel.config(image = self.img)
        self.imagePanel.pack()

        # Caluculate Delay
        delay = (1.0/self.frameRate)-(time.time()-startTime)

        #print(delay)
        # Assert to ensure positive delay:
        assert delay>0,'\033[0;31m[AssertionError]==> Cannot run at the given frame rate\033[0m'

        # Synchronize the video
        #self.playJob = self.root.after(int(math.ceil(delay*1000)),self.sync)
        self.playJob = self.root.after(int(delay*1000),self.sync)

#-----------------------------------------------------------------------------------------------#
# Boilerplate code (For testing only):

if __name__ == '__main__':
    #a = videoPlayer('oneperson_960_540.rgb',540,960,3,30)
    a = videoData('oneperson_960_540.rgb',540,960,3)
    b = videoPlayer.fromVideoFile(a,20)
