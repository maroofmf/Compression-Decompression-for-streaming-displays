
'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
import math
from videoData import videoData
from compression import compression
#import segmentation
import cv2
import numpy as np

class videoPlayer(videoData):
    def __init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS):
        videoData.__init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS)


def main():
    vidData = videoData('oneperson_960_540.rgb', 540, 960, 3)
#	seg = segmentation()
    #frame = vidPlayer.getFrame(0)
    compressor = compression(1,1,vidData)
    compressor.saveCMP()
#	print 'Block 1980: ', block_dimention_updated
#    vidData.computeDCT(block,8)     
    #for frame in vidPlayer.iterator():
#    gray = vidData.YfromRGB(frame)
#    print gray.shape 
#	cv2.imshow('frame',gray)
#	cv2.waitKey(0)  
#         #print 'hi'     
##        break
#	cv2.destroyAllWindows()
#    

    
    #for frame in vidPlayer.iterator():
    #gray = vidPlayer.YfromRGB(frame)
    
    # cv2.imshow('frame',gray)
    # cv2.waitKey(0)
    # #print 'hi'     
# #        break
	# cv2.destroyAllWindows()
    

if __name__ == '__main__':
    main()
