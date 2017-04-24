'''
Description: Segmentation class. 
-> Obtains 16x16 blocks of the raw video and computes motion vectors.
-> videoData class used to inherit block accessor
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''

import cv2
from videoData import videoData

class segmentation(videoData):
#    #------------------------------ Constructor ------------------------------#
    def __init__(self):
        return
#	
    # def computeMotionVector(self):
		# # Uses YfromRGB
        
# #		
    # def YfromRGB(self,frame):
        # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)        
        # return gray
# #	
# #	# returns a label indicating the block type
    # def computeLayer(self):
		# # Uses computeMotionVector
        