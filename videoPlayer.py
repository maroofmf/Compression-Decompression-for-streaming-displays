'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
import math
from videoData import videoData
import time
import cv2
import numpy as np

class videoPlayer(videoData):
	def __init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS):
		videoData.__init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS)


def main():
	vidPlayer = videoPlayer('oneperson_960_540.rgb',540, 960, 3)
	for frame in vidPlayer.iterator():
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('h'):
			break

if __name__ == '__main__':
	main()
