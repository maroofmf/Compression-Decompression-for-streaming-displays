
'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
from videoData import videoData
from compression import compression
#import segmentation
import cv2
import numpy as np

class videoPlayer(videoData):
    def __init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS, FRAMERATE):
        videoData.__init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS)
        self.__frameRate = FRAMERATE
	
    def sync(self, systemTime):
        time.sleep((1.0/self.__frameRate) - systemTime)
