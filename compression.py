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
import time
from videoData import videoData
class compression():
    #------------------------------ Constructor ------------------------------#
    def __init__(self, vidData):
        self.vidData = vidData
        self.__blockSize = 8

    def computeDCT(self, block3D, block_size, blockType):
        channelDCT = np.zeros(block_size*block_size*3 + 1)
        # block_dimention_updated = np.einsum('jki->ijk',block3D)
        channelDCT[0] = blockType
        for channel in range (self.vidData.getNumChannels()):
            block = block3D[channel, :, :]
            block_f = np.float32(block)  # float conversion/scale
            dct_coeffs = cv2.dct(block_f)           # the dct
            channelDCT[(block_size*block_size*channel)+1:(block_size*block_size*(channel+1))+1] = dct_coeffs.reshape((1, block_size*block_size))
        return channelDCT
        
    def saveCMP(self):
        # put DCT into a file
        # st = time.time()
        iIndices = range(0, self.vidData.getHeight(), self.__blockSize)
        jIndices = range(0, self.vidData.getWidth(), self.__blockSize)
        no_of_blocks = len(iIndices)*len(jIndices)
#        print no_of_blocks
        framesPerCMP = 50
        blockDCT = np.zeros((framesPerCMP*no_of_blocks,(8*8*3 )+ 1))
        
        iIndices[-1] = self.vidData.getHeight() - self.__blockSize
        jIndices[-1] = self.vidData.getWidth() - self.__blockSize
#        self.vidData.totalFrames
        cntr = 0
        cntr_frame = 0
        for frame in range(self.vidData.totalFrames):
            for i in iIndices:
                for j in jIndices:
                    blockType = self.vidData.getLabel(cntr_frame, i/self.__blockSize, j/self.__blockSize)
                    block = self.vidData.getBlock(frame, i, j, self.__blockSize)
                    blockDCT[cntr,:] = self.computeDCT(block, self.__blockSize, blockType)
                    cntr = cntr + 1
            cntr_frame = cntr_frame + 1
            if cntr_frame % framesPerCMP == 0 or cntr_frame==self.vidData.totalFrames:
                np.savetxt('DCT'+str(cntr_frame) + '.cmp', blockDCT[0:cntr,:], fmt='%1.1f')
                cntr = 0
                print 'Wrote', 'DCT'+str(cntr_frame) + '.cmp' 