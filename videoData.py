
'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
import time
import numpy as np
import math
#from scipy.fftpack import dct, idct
import cv2
import time
class videoData:
    
    #------------------------------ Constructor ------------------------------#
    def __init__(self, FILE_NAME, HEIGHT, WIDTH, CHANNELS):
        self.__videoFrames = np.fromfile(FILE_NAME, dtype ='uint8')
        self.__width = WIDTH
        self.__height = HEIGHT
        self.__channels = CHANNELS
        self.totalFrames = len(self.__videoFrames)/(WIDTH*HEIGHT*CHANNELS)
        self.blockLabels = np.zeros((self.totalFrames, math.ceil(self.__height/16.0), math.ceil(self.__width/16.0)), dtype=np.int)
        #--- Reshape videoFrame from 1 x (540_rows x 960_cols x 3_channels x 363_frames) --------------------#
        #---------------------- to (363_frames) x (3_channels) x (540_rows) x (960_cols) --------------------#
        self.__videoFrames = self.__videoFrames.reshape((self.totalFrames, self.__channels, self.__height, self.__width))
        
    def getNumChannels(self):
        return self.__channels
        
    def getHeight(self):
        return self.__height
    
    def getWidth(self):
        return self.__width
        
    def getNumBlocks(self,blockSize):
        noOfBlocks =  math.ceil(1.0*self.__width/blockSize) * math.ceil(1.0*self.__height/blockSize)
        #print noOfBlocks
        return int(noOfBlocks)
        
    
    def getFrame(self,frameNumber):
        frame = self.__videoFrames[frameNumber, :,:,:]
		# frame = np.empty((self.__height,self.__width, self.__channels),'uint8')
		# frameOffset = frameNumber*self.__height*self.__width*self.__channels
		# for c in range(self.__channels):
			# channelOffset = self.__height*self.__width*c		
			# startIndex = frameOffset + channelOffset
			# endIndex =  startIndex + self.__height*self.__width
			# frame[:,:,2-c] = np.copy((self.__videoFrames[startIndex:endIndex]).reshape((self.__height,self.__width)))
        return frame


    def iterator(self,startFrame=0):
        for i in range(self.totalFrames):
            yield(self.getFrame(startFrame+i))

    def getBlock(self, frameNumber, i, j, block_size):
        block3D = self.__videoFrames[frameNumber, :, i:i+block_size, j:j+block_size]
        # block = np.empty((block_size,block_size, self.__channels),'uint8')
        # a = np.empty((block_size*block_size),'uint8')
        # frameOffset = frameNumber*self.__height*self.__width*self.__channels
        # no_of_blocks = math.floor((self.__width/block_size))*math.floor((self.__height/block_size))
# #        print no_of_blocks
        # for c in range(self.__channels):
            # channelOffset = self.__height*self.__width*c
            # if blockNumber < no_of_blocks:
                # startIndex = frameOffset + channelOffset + (math.floor((blockNumber) / (self.__width/block_size)) * self.__width * block_size) + ((blockNumber)%(self.__width/block_size) * block_size)
            # else:
                # startIndex = frameOffset + channelOffset + channelOffset - ((((self.__width/block_size) - (blockNumber - no_of_blocks))* block_size)+((block_size-1))*self.__width)
            # for index in range(block_size):

                # b = self.__videoFrames[(self.__width*(index))+startIndex:(self.__width*(index))+startIndex + block_size] 
             
                # a[index*block_size:index*block_size + block_size] = b
            
            # block[:,:,2-c] = np.copy(a.reshape((block_size,block_size)))
#            print block[:,:,2-c]
        return block3D