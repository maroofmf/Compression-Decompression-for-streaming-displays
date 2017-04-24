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
import numpy as np
import cv2
from videoData import videoData
class compression():
    #------------------------------ Constructor ------------------------------#
    def __init__(self, n1, n2, vidData):
        self.quantStepFG = n1
        self.quantStepBG = n2
        self.vidData = vidData

    def computeDCT(self,block3D, block_size):
#        print block3D
        blockType = 0 #To be computed from segmentation
        blockDCTString = "Type " + str(blockType)
        block_dimention_updated = np.einsum('jki->ijk',block3D)
        for channel in range (self.vidData.getNumChannels()):
            block = block_dimention_updated[:][:][channel]
            block_f = np.float32(block)  # float conversion/scale
            dct_coeffs = cv2.dct(block_f)           # the dct
            channelDCTStr = str(dct_coeffs.reshape((1, block_size*block_size)))
            blockDCTString += channelDCTStr
        return blockDCTString

    def computeIDCT(self):
        return

    def loadFromCMP(self):
        return
        # set dctCOEFF

    def saveCMP(self):
        # put DCT into a file
        dct_file = open('DCT.cmp', 'a')
        block = self.vidData.getBlock(0,0,8)
        blockDCTString = self.computeDCT(block,8)     
        dct_file.write(blockDCTString)
        dct_file.close

    def quantize(self):
        return