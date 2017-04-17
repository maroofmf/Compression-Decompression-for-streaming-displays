'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
#import Tkinter as tk, threading
#from PIL import Image, ImageTk
import math
from videoData import videoData
import time
import cv2

class videoPlayer(videoData):
	def __init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS):
		videoData.__init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS)
		#self.__fileName = FILENAME



def main():
    
    vidPlayer = videoPlayer('oneperson_960_540.rgb',540, 960, 3)

    for frame in vidPlayer.iterator():
#            print 'hey'
                  
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('h'):
                break
        cv2.destroyAllWindows()



if __name__ == '__main__':
	main()
