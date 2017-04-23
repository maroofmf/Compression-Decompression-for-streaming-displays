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
import math
import sys
from videoData import videoData
import time

#----------------------------------------------------------------------------------------------------------------#
# FilePaths:
global playButtonPath
playButtonPath = './metadata/playButton.png'

global playerInitPath
playerInitPath = './metadata/playerInit.jpg'

global pauseButtonPath
pauseButtonPath = './metadata/pauseButton.jpg'

#----------------------------------------------------------------------------------------------------------------#
class videoPlayer(videoData):

    # Constructor: Initialize GUI
    def __init__(self,FILENAME,HEIGHT,WIDTH,CHANNELS,FRAMERATE = 30):

        # Super Init:
        videoData.__init__(self,FILENAME,HEIGHT,WIDTH,CHANNELS)

        # Init root
        self.root = Tk()
        self.root.geometry('960x600')

        # Self init;
        self.currentJob = None
        self.frameRate = FRAMERATE
        self.playButtonImage = ImageTk.PhotoImage(Image.open(playButtonPath).resize((40,40),1))
        self.pauseButtonImage = ImageTk.PhotoImage(Image.open(pauseButtonPath).resize((40,40),1))
        self.init_img = ImageTk.PhotoImage(Image.open(playerInitPath).resize((960,540)))
        self.playing = False

        # Init frames
        self.imageFrame = Frame(self.root)
        self.imageFrame.pack()
        self.buttonFrame = Frame(self.root)
        self.buttonFrame.pack(side=BOTTOM)

        # Initialize panels
        self.imagePanel = Label(self.imageFrame,image = self.init_img)
        self.imagePanel.pack()
        self.buttonsInit()
        self.index = 0
        # Start program
        self.root.mainloop()

#-----------------------------------------------------------------------------------------------#
# Initialize buttons:

    def buttonsInit(self):

        # Play/Pause button:
        self.playButton = Button(self.buttonFrame,image=self.playButtonImage, command = self.playVideo)
        self.playButton.pack(side=LEFT)

        '''
        # Stop button:
        stopButton = Button(self.buttonFrame,text = 'stop',command = self.stopVideo)
        stopButton.pack(side =LEFT)

        # Gaze control button
        gazeButton = Button(self.buttonFrame,text = 'Gaze_control',command = self.action)
        gazeButton.pack(side = LEFT)
        '''

#-----------------------------------------------------------------------------------------------#
# Play/Pause button callback function:

    def playVideo(self):

        if self.playing:
            self.playing = False
            self.playButton.config(image=self.playButtonImage)
            self.playButton.pack()
            self.freezeFrame()
        else:
            self.playing=True
            self.playButton.config(image=self.pauseButtonImage)
            self.playButton.pack()
            self.sync()

#-----------------------------------------------------------------------------------------------#
# Freeze frame and perform processing:

    def freezeFrame(self):

        if(self.playing):
            return

        self.img = ImageTk.PhotoImage(Image.fromarray(self.getFrame(self.index)))
        self.imagePanel.config(image = self.img)
        self.imagePanel.pack()

        # Pause the video
        self.root.after(100,self.freezeFrame)

#-----------------------------------------------------------------------------------------------#
# Sync the video:

    def sync(self):

        if not self.playing:
            return

        startTime = time.time()
        if(self.index ==self.totalFrames):
            sys.exit(0)
        self.img = ImageTk.PhotoImage(Image.fromarray(self.getFrame(self.index)))
        self.imagePanel.config(image = self.img)
        self.imagePanel.pack()
        self.index +=1

        # Caluculate Delay
        delay = (1.0/self.frameRate)-(time.time()-startTime)

        # Assert to ensure positive delay:
        assert delay>0,'\033[0;31m[AssertionError]==> Cannot run at the given frame rate\033[0m'

        # Synchronize the video
        self.root.after(int(delay*1000),self.sync)

#-----------------------------------------------------------------------------------------------#
# Boilerplate code (For testing only):

if __name__ == '__main__':
	a = videoPlayer('oneperson_960_540.rgb',540,960,3,30)
