'''
Description: Compression class
-> Obtains 8x8 blocks of the raw video and obtains dct coefficients
-> Can do the reverse as well

-> videoData class used to inherit block accessor
-> segmentation class used to obtain block's type
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
import time
import numpy as np
import cv2
from videoData import videoData
class compression():
    #------------------------------ Constructor ------------------------------#
    def __init__(self, n1, n2, vidData):
        self.quantStepFG = n1
        self.quantStepBG = n2
        self.vidData = vidData
        self.__blockSize = 8

    def computeDCT(self, block3D, block_size):
#        print block3D
        blockType = 0 #To be computed from segmentation
        blockDCTString = "" + str(blockType) + " "
        # block_dimention_updated = np.einsum('jki->ijk',block3D)
        for channel in range (self.vidData.getNumChannels()):
            block = block3D[channel, :, :]
            block_f = np.float32(block)  # float conversion/scale
            dct_coeffs = cv2.dct(block_f)           # the dct
            channelDCTStr = str(np.around(dct_coeffs.reshape((1, block_size*block_size)),decimals=1))
            blockDCTString += channelDCTStr + " "
        blockDCTString = blockDCTString.replace("\n", "")
        blockDCTString = blockDCTString.replace("[", "")
        blockDCTString = blockDCTString.replace("]", "")
        return blockDCTString

    def computeIDCT(self):
        return

    def loadFromCMP(self):
        return
        # set dctCOEFF

    def saveCMP(self):
        # put DCT into a file
        dct_file = open('DCT.cmp', 'a')
        float_formatter = lambda x: "%.1f" % x
        np.set_printoptions(formatter={'float_kind':float_formatter})
        
        # noOfBlocks = self.vidData.getNumBlocks(block_size)
        iIndices = range(0, self.vidData.getHeight(), self.__blockSize)
        jIndices = range(0, self.vidData.getWidth(), self.__blockSize)
        
        iIndices[-1] = self.vidData.getHeight() - self.__blockSize
        jIndices[-1] = self.vidData.getWidth() - self.__blockSize
        for i in iIndices:
            for j in jIndices:
                block = self.vidData.getBlock(0, i, j, self.__blockSize)
                blockDCTString = self.computeDCT(block, self.__blockSize)
                dct_file.write(blockDCTString + "\n")
        dct_file.close

    def quantize(self):
        return