'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
import numpy as np

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
			frame[:,:,2-c] = (self.__videoFrames[startIndex:endIndex]).reshape((self.__height,self.__width))		       			    
		return frame


    def iterator(self,startFrame=0):
        for i in range(self.totalFrames):
            yield(self.getFrame(startFrame+i))

    # def getNextBlock:


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


