
'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
import numpy as np
import math
#from scipy.fftpack import dct, idct
import cv2
class videoData:
    
    #------------------------------ Constructor ------------------------------#
    def __init__(self, FILE_NAME, HEIGHT, WIDTH, CHANNELS):
	self.__videoFrames = np.fromfile(FILE_NAME, dtype ='uint8')
	self.__width = WIDTH
	self.__height = HEIGHT
	self.__channels = CHANNELS
	self.totalFrames = len(self.__videoFrames)/(WIDTH*HEIGHT*CHANNELS)
	
    def getNumChannels(self):
        return self.__channels
    
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
        no_of_blocks = math.floor((self.__width/block_size))*math.floor((self.__height/block_size))
#        print no_of_blocks
        for c in range(self.__channels):
            channelOffset = self.__height*self.__width*c
            if blockNumber < no_of_blocks:
                startIndex = frameOffset + channelOffset + (math.floor((blockNumber) / (self.__width/block_size)) * self.__width * block_size) + ((blockNumber)%(self.__width/block_size) * block_size)
            else:
                startIndex = frameOffset + channelOffset + channelOffset - ((((self.__width/block_size) - (blockNumber - no_of_blocks))* block_size)+((block_size-1))*self.__width)
            for index in range(block_size):

                b = self.__videoFrames[(self.__width*(index))+startIndex:(self.__width*(index))+startIndex + block_size] 
             
                a[index*block_size:index*block_size + block_size] = b
            
            block[:,:,2-c] = np.copy(a.reshape((block_size,block_size)))
#            print block[:,:,2-c]
        return block
        
        
        
        
    def computeDCT(self,block3D, block_size):
#        print block3D
        block_dimention_updated = np.einsum('jki->ijk',block3D)
        dct_file = open('DCT.cmp', 'a')
        for channel in range (self.__channels):
             block = block_dimention_updated[:][:][2-channel]
#             print 'Block',block
             block_f = np.float32(block)  # float conversion/scale
             dct_coeffs = cv2.dct(block_f)           # the dct
             str1 = "Type "
             for i in range(block_size):
                 str1 = str1 + str(dct_coeffs[i][0:])
             dct_row_str = str1.replace("\n", "")
             
                 
             dct_file.write(dct_row_str)
        dct_file.close
#        myFile.write("\n")   
        
        
    def YfromRGB(self,frame):
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)        
        return gray
#class compression(videoData):
#
#     def __init(self):
#         self.__blockSize = 8
#
#     def computeDCT(self, block3D):
#         
#         for channel in range (self.__channels):
#             block = block3D[:][:][channel]
#             block_f = np.float32(block)  # float conversion/scale
#             dct_coeffs = cv2.dct(block_f)           # the dct
#             str1 = "Type "
#             for i in range(self.__blockSize):
#                 str1 = str1 + str(dct_coeffs[i][0:])
#             dct_row_str = str1.replace("\n", "")
#             with open('DCT.cmp', 'w') as myFile:
#                 
#                 myFile.write(dct_row_str)
#         myFile.write("\n")
#         
#
#     def computeIDCT(self):
#         imgcv1 = cv2.idct(dst)
#     def loadFromCMP(self):
#         # set dctCOEFF
#
#     def saveCMP(self):
#         # put DCT into a file
#
#     def quantize(self):
#

