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
    def __init__(self, n1, n2, vidData):
        self.__quantStepFG = n1
        self.__quantStepBG = n2
        self.__vidData = vidData
        self.__blockSize = 8

    def computeDCT(self, block3D, block_size):
#        print block3D
        blockType = 0.0 #To be computed from segmentation
#        blockDCTString = "" + str(blockType) + " "
        float_formatter = lambda x: "%.1f" % x
        np.set_printoptions(formatter={'float_kind':float_formatter})
        channelDCT = np.zeros(block_size*block_size*3 + 1)
        # block_dimention_updated = np.einsum('jki->ijk',block3D)
        channelDCT[0] = blockType
        for channel in range (self.__vidData.getNumChannels()):
            block = block3D[channel, :, :]
            block_f = np.float32(block)  # float conversion/scale
            dct_coeffs = cv2.dct(block_f)           # the dct
            channelDCT[(block_size*block_size*channel)+1:(block_size*block_size*(channel+1))+1] = np.around(dct_coeffs.reshape((1, block_size*block_size)),1)
#            blockDCTString += channelDCTStr + " "
#        blockDCTString = blockDCTString.replace("\n", "")
#        blockDCTString = blockDCTString.replace("[", "")
#        blockDCTString = blockDCTString.replace("]", "")
        return channelDCT

    def computeIDCT(self):
        return

    def loadFromCMP(self):
        return
        # set dctCOEFF

    def saveToCMP(self, frameNumber, dct_file):
        # put DCT into a file
        st = time.time()
#        dct_file = open('DCT.cmp', 'a')
#        float_formatter = lambda x: "%.1f" % x
#        np.set_printoptions(formatter={'float_kind':float_formatter})
        
        # noOfBlocks = self.vidData.getNumBlocks(block_size)
#        self.vidData.totalFrames = 1
        iIndices = range(0, self.__vidData.getHeight(), self.__blockSize)
        jIndices = range(0, self.__vidData.getWidth(), self.__blockSize)
        no_of_blocks = len(iIndices)*len(jIndices)
        #print no_of_blocks
        blockDCT = np.zeros((self.__vidData.totalFrames*no_of_blocks,(self.__blockSize*self.__blockSize*self.__vidData.getNumChannels())+ 1))
        
        iIndices[-1] = self.__vidData.getHeight() - self.__blockSize
        jIndices[-1] = self.__vidData.getWidth() - self.__blockSize
#        self.vidData.totalFrames
        cntr = 0
        for frame in range(self.__vidData.totalFrames):
            for i in iIndices:
                for j in jIndices:
                    block = self.__vidData.getBlock(frame, i, j, self.__blockSize)
                    blockDCT[cntr,:] = self.computeDCT(block, self.__blockSize)
#                    print blockDCT[cntr,:]
                    cntr = cntr + 1
    #                print blockDCTString
    #                dct_file.write(blockDCTString)
            
#        blockDCTString  = map(str, blockDCT)
#        blockDCTString  = str(blockDCT)
#        print blockDCTString
#        dct_file.write(blockDCTString)
#        for row in zip(blockDCT):
#            blockDCTString = ( ' [%s]' % ( ' '.join('%03s' % i for i in row)))
#            blockDCTString = blockDCTString.replace("\n", "")
#            blockDCTString = blockDCTString.replace("[", "")
#            blockDCTString = blockDCTString.replace("]", "")
#            dct_file.write (blockDCTString)
#            dct_file.write('\n')
        np.savetxt('DCT.cmp', blockDCT, fmt='%1.1f')
#        dct_file.close
        print time.time() - st

    def quantize(self):
        return