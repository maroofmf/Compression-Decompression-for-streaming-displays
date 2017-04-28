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
import numpy as np
from videoData import videoData
import matplotlib.pyplot as plt
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
    
    def segmentBlocksInFrame(self, frame, prevFrame, frameNumber):
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
        motionVectors = np.zeros((len(iIndices)*len(jIndices), 2))
        blockCounter = 0
        for i in iIndices:
            for j in jIndices:
                block = frame[i:i+self.__blockSize, j:j+self.__blockSize]
                topLeft = [max((i-k), 0), max((j-k),0)]
                bottomRight = [min(i+k+self.__blockSize-1, height-1), min(j+k+self.__blockSize-1, width-1)]
                # print topLeft, bottomRight
                searchSpace = prevFrame[topLeft[ROW]:bottomRight[ROW]+1, topLeft[COL]:bottomRight[COL]+1] # +1 so that bottomRight is included too
                dx, dy = self.computeMotionVectorPyramid(searchSpace, block, [i-topLeft[ROW], j-topLeft[COL]])
                motionVectors[blockCounter] = dx, dy
                self.setLabel(dx, dy, frameNumber, blockCounter)
                print i,j, motionVectors[blockCounter]
                
                # if (i == 336 and j == 192):
                    # print 'block', block
                    # print 'searchSpace', searchSpace
                    # cv2.imshow('block', np.uint8(block))
                    # cv2.waitKey(0)
                    # cv2.imshow('searchSpace', np.uint8(searchSpace))
                    # cv2.waitKey(0)
                    # np.savetxt('block.txt', block, fmt='%d')
                    # np.savetxt('searchSpace.txt', searchSpace, fmt='%d')
                    # # exit(0)
                blockCounter += 1
        # fig = plt
        # fig.plot(motionVectors[:,0], motionVectors[:,1], 'b*')
        # fig.grid()
        # fig.show()
    
    def computeMotionVector(self, searchSpace, block, blockTopLeft, k):
        rows = searchSpace.shape[0]
        cols = searchSpace.shape[1]
        blockSize = block.shape[ROW] # or COL; same thing
        SADvals = np.zeros((rows-blockSize+1, cols-blockSize+1))
        for i in range(0, SADvals.shape[0]):
            for j in range(0, SADvals.shape[1]):
                localNeighbor = searchSpace[i:i+blockSize, j:j+blockSize]
                SADvals[i][j] = np.sum(np.sum(np.abs(localNeighbor-block)))
        minSAD_pos = np.where(SADvals == SADvals.min())
        minSAD_TopLeft = [minSAD_pos[ROW].tolist()[0], minSAD_pos[COL].tolist()[0]]
        # print 'blockTopLeft', blockTopLeft, '\t minSAD_TopLeft', minSAD_TopLeft, 'minSAD_pos', minSAD_pos
        # np.savetxt('SADvals.txt', SADvals, fmt='%d')
        dx = minSAD_TopLeft[0]-blockTopLeft[0]
        dy = minSAD_TopLeft[1]-blockTopLeft[1]
        return dx, dy
     
    def computeMotionVectorPyramid(self, searchSpace, block, blockTopLeft):
        
        # -----------Level 3------------ #
        blockLevel3 = block[0:-1:4, 0:-1:4]
        searchSpaceLevel3 = searchSpace[0:-1:4, 0:-1:4]
        k = self.__searchWin/4
        blockTopLeftLevel3 = [blockTopLeft[ROW]/4, blockTopLeft[COL]/4]
        dxLevel3, dyLevel3 = self.computeMotionVector(searchSpaceLevel3, blockLevel3, blockTopLeftLevel3, k)
        
        # -----------Level 2------------ #
        dxLevel2, dyLevel2 = dxLevel3*2, dyLevel3*2
        searchSpaceLevel2 = searchSpace[0:-1:2, 0:-1:2]
        blockLevel2 = block[0:-1:2, 0:-1:2]
        k = self.__searchWin/2
        n = block.shape[ROW]/2
        blockTopLeftLevel2 = [blockTopLeft[ROW]/2, blockTopLeft[COL]/2]
        refinedSearchSpaceTopLeft = [max(blockTopLeftLevel2[ROW]-1, 0), max(blockTopLeftLevel2[COL]-1, 0)]
        refinedSearchSpaceBotRight = [blockTopLeftLevel2[ROW]+n+1, blockTopLeftLevel2[COL]+n+1]
        refinedSearchSpace = searchSpaceLevel2[refinedSearchSpaceTopLeft[ROW]:refinedSearchSpaceBotRight[ROW]+1, refinedSearchSpaceTopLeft[COL]:refinedSearchSpaceBotRight[COL]+1]
        dxRefined, dyRefined = self.computeMotionVector(refinedSearchSpace, blockLevel2, blockTopLeftLevel2, k)
        dxLevel2 += dxRefined
        dyLevel2 += dyRefined
        
        # -----------Level 1------------ #
        dxLevel1, dyLevel1 = dxLevel2*2, dyLevel2*2
        k = self.__searchWin
        n = block.shape[ROW]
        refinedSearchSpaceTopLeft = [max(blockTopLeft[ROW]-1, 0), max(blockTopLeft[COL]-1, 0)]
        refinedSearchSpaceBotRight = [blockTopLeft[ROW]+n+1, blockTopLeft[COL]+n+1]
        refinedSearchSpace = searchSpace[refinedSearchSpaceTopLeft[ROW]:refinedSearchSpaceBotRight[ROW]+1, refinedSearchSpaceTopLeft[COL]:refinedSearchSpaceBotRight[COL]+1]
        dxRefined, dyRefined = self.computeMotionVector(refinedSearchSpace, block, blockTopLeft, k)
        dx = dxLevel1+dxRefined
        dy = dxLevel1+dyRefined
        
        return dx, dy

    # Can't use cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) since frame is of size (3, rows, cols)
    # and not (rows, cols, 3) as needed in cvtColor. So using the formula for YUV to RGB
    # Source: http://www.pcmag.com/encyclopedia/term/55166/yuv-rgb-conversion-formulas
    def YfromRGB(self,frame):
        gray = np.empty((frame.shape[1], frame.shape[2]), dtype = 'uint8')
        gray = 0.299*frame[R_CHANNEL, :, :] + 0.587*frame[G_CHANNEL, :, :] + 0.114*frame[B_CHANNEL, :, :]
        return np.int16(gray)

    def setLabel(self, dx, dy, frameNumber, blockCounter):
        label = 1
        r = blockCounter/60
        c = blockCounter%60
        # print blockCounter, r, c
        self.__vidData.blockLabels[frameNumber][2*r][2*c] = label
        self.__vidData.blockLabels[frameNumber][2*r][2*c+1] = label
        self.__vidData.blockLabels[frameNumber][2*r+1][2*c] = label
        self.__vidData.blockLabels[frameNumber][2*r+1][2*c+1] = label