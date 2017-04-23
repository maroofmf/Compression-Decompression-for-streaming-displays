
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
	block = vidPlayer.getBlock(0,1980,8)
	 
#	print 'Block 1980: ', block_dimention_updated  
	vidPlayer.computeDCT(block,8)     
	#for frame in vidPlayer.iterator():
#	cv2.imshow('frame',block)
#	cv2.waitKey(0)  
#         #print 'hi'     
##        break
#	cv2.destroyAllWindows()
    
if __name__ == '__main__':
	main()
