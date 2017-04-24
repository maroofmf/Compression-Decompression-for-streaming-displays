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
ROW = 0
COL = 1
R_CHANNEL = 0
G_CHANNEL = 1
B_CHANNEL = 2
class segmentation(videoData):
    #------------------------------ Constructor ------------------------------#
    def __init__(self, vidData, k):
        self.__blockSize = 16
        self.__vidData = vidData
        self.__searchWin = k
    
    def segmentBlocksInFrame(self, frame, prevFrame):
        #------------- Indices to traverse in the rows and cols ---------------#
        iIndices = range(0, self.__vidData.getHeight(), self.__blockSize)
        jIndices = range(0, self.__vidData.getWidth(), self.__blockSize)
        
        #------ Handle the boundary cases by overlapping blocks, i.e.,---------# 
        #---------shifting the last index to up/left appropriately-------------#
        iIndices[-1] = self.__vidData.getHeight() - self.__blockSize
        jIndices[-1] = self.__vidData.getWidth() - self.__blockSize
        
        height = self.__vidData.getHeight()
        width = self.__vidData.getWidth()
        k = self.__searchWin
        for i in iIndices:
            for j in jIndices:
                block = frame[i:i+self.__blockSize, j:j+self.__blockSize]
                topLeft = [max((i-k), 0), max((j-k),0)]
                bottomRight = [min(i+k+self.__blockSize, height), min(j+k+self.__blockSize, width)]
                searchSpace = prevFrame[topLeft[ROW]:bottomRight[ROW], topLeft[COL]:bottomRight[COL]]
                dx, dy = computeMotionVector(searchSpace, block)
    
    def computeMotionVector(self, searchSpace, block):
        return dx, dy

    # Can't use cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) since frame is of size (3, rows, cols)
    # and not (rows, cols, 3) as needed in cvtColor. So using the formula for YUV to RGB
    # Source: http://www.pcmag.com/encyclopedia/term/55166/yuv-rgb-conversion-formulas
    def YfromRGB(self,frame):
        gray = 0.299*frame[R_CHANNEL, :, :] + 0.587*frame[G_CHANNEL, :, :] + 0.114*frame[B_CHANNEL, :, :]
        return gray

    # returns a label indicating the block type
    def computeLayer(self, dx, dy):
        # Uses computeMotionVector
        return