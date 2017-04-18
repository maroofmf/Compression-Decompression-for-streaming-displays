
'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
import numpy as np
import math
from scipy.fftpack import dct, idct
class videoData:
    
    #------------------------------ Constructor ------------------------------#
    def __init__(self, FILE_NAME, HEIGHT, WIDTH, CHANNELS):
	self.__videoFrames = np.fromfile(FILE_NAME, dtype ='uint8')
	self.__width = WIDTH
	self.__height = HEIGHT
	self.__channels = CHANNELS
	self.totalFrames = len(self.__videoFrames)/(WIDTH*HEIGHT*CHANNELS)
	
    def getFrame(self,frameNumber):
		frame = np.empty((self.__height,self.__width, self.__channels),'uint8')
		frameOffset = frameNumber*self.__height*self.__width*self.__channels
		for c in range(self.__channels):
			channelOffset = self.__height*self.__width*c		
			startIndex = frameOffset + channelOffset
			endIndex =  startIndex + self.__height*self.__width
			frame[:,:,2-c] = np.copy((self.__videoFrames[startIndex:endIndex]).reshape((self.__height,self.__width)))
		return frame


    def iterator(self,startFrame=0):
        for i in range(self.totalFrames):
            yield(self.getFrame(startFrame+i))

    def getBlock(self, frameNumber, blockNumber, block_size):
        block = np.empty((block_size,block_size, self.__channels),'uint8')
        a = np.empty((block_size*block_size),'uint8')
        frameOffset = frameNumber*self.__height*self.__width*self.__channels
        for c in range(self.__channels):
            channelOffset = self.__height*self.__width*c		
            startIndex = frameOffset + channelOffset + (math.floor((blockNumber) / (self.__width/block_size)) * (self.__width/block_size) * block_size * block_size) + ((blockNumber)%(self.__width/block_size) * block_size)
            
            for index in range(block_size):

                b = self.__videoFrames[(self.__width*(index))+startIndex:(self.__width*(index))+startIndex + block_size] 
             
                a[index*block_size:index*block_size + block_size] = b
            
            block[:,:,2-c] = np.copy(a.reshape((block_size,block_size)))
            print block[:,:,2-c]
        return block
# class compression(videoData):

#     def __init(self):
#         self.dctCOEFF = [[],[],[],[],[].....]

#     def computeDCT(self):
#         self.getNextBlock()

#     def computeIDCT(self):

#     def loadFromCMP(self):
#         # set dctCOEFF

#     def saveCMP(self):
#         # put DCT into a file

#     def quantize(self):


