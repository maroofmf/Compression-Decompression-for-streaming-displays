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
#        print block3D
        # blockType = 0.0 #To be computed from segmentation
        
#        blockDCTString = "" + str(blockType) + " "
        # float_formatter = lambda x: "%.1f" % x
        # np.set_printoptions(formatter={'float_kind':float_formatter})
        channelDCT = np.zeros(block_size*block_size*3 + 1)
        # block_dimention_updated = np.einsum('jki->ijk',block3D)
        channelDCT[0] = blockType
        for channel in range (self.vidData.getNumChannels()):
            block = block3D[channel, :, :]
            block_f = np.float32(block)  # float conversion/scale
            dct_coeffs = cv2.dct(block_f)           # the dct
            channelDCT[(block_size*block_size*channel)+1:(block_size*block_size*(channel+1))+1] = np.around(dct_coeffs.reshape((1, block_size*block_size)),1)
#            blockDCTString += channelDCTStr + " "
#        blockDCTString = blockDCTString.replace("\n", "")
#        blockDCTString = blockDCTString.replace("[", "")
#        blockDCTString = blockDCTString.replace("]", "")
        return channelDCT
        
    # def computeIDCT(self,dequantised_coef):
        # rgb_frames = np.zeros(self.vidData.totalFrames,3,self.vidData.getWidth(),self.vidData.getHeight())
        # iIndices = range(0, self.vidData.getHeight(), 8)
        # jIndices = range(0, self.vidData.getWidth(), 8)
        # iIndices[-1] = self.vidData.getHeight() - self.__blockSize
        # jIndices[-1] = self.vidData.getWidth() - self.__blockSize
        
        # for frame in range(self.vidData.totalFrames):
            # cntr = 0
            # for i in iIndices:
                # for j in jIndices:
                    # for channel in range (self.vidData.getNumChannels()):
                        # rgb_frames[frame,channel,i:i+8,j:j+8] = cv2.idct((dequantised_coef[self.vidData.getNumBlocks*frame+cntr,(channel*64)+1:((channel+1)*64)+1].reshape(8,8)))
                    # cntr = cntr + 1
                
        # return

    # def loadFromCMP(self):
        # cntr = 0
        # cntr2=0
        # no_of_frames = 10
        # Dct_array = np.zeros((self.vidData.getNumBlocks(8)*self.vidData.totalFrames,193))
        # for file_sel in range(int(math.floor(self.vidData.totalFrames/no_of_frames))):
            # f = open('C:/Users/aggar/Desktop/gaze_control/DCT'+str((file_sel+1) * no_of_frames)+'.cmp')
            # cntr1 = 0    
            # for y in f.read().split('\n'):   
                # x = []
                # cntr = 0
                # for z in y.split(' '):
            # #            print z
                    # if cntr == 193:
                        # break
                    # x.append(float(z))
                    # cntr = cntr + 1
                # Dct_array[cntr2,:] = x
                # cntr1 = cntr1 + 1
                # cntr2 = cntr2 + 1
                # if cntr1 == self.vidData.getNumBlocks(8)*no_of_frames:
                    # break
        # return Dct_array
        # # set dctCOEFF

    def saveCMP(self):
        # put DCT into a file
        st = time.time()
#        dct_file = open('DCT.cmp', 'a')
#        float_formatter = lambda x: "%.1f" % x
#        np.set_printoptions(formatter={'float_kind':float_formatter})
        
        # noOfBlocks = self.vidData.getNumBlocks(block_size)
#        self.vidData.totalFrames = 50
        iIndices = range(0, self.vidData.getHeight(), self.__blockSize)
        jIndices = range(0, self.vidData.getWidth(), self.__blockSize)
        no_of_blocks = len(iIndices)*len(jIndices)
        # print no_of_blocks
        blockDCT = np.zeros((10*no_of_blocks,(8*8*3 )+ 1))
        
        iIndices[-1] = self.vidData.getHeight() - self.__blockSize
        jIndices[-1] = self.vidData.getWidth() - self.__blockSize
#        self.vidData.totalFrames
        cntr = 0
        cntr_frame = 0
        for frame in range(self.vidData.totalFrames):
            for i in iIndices:
                for j in jIndices:
                    blockType = self.vidData.getLabel(cntr_frame, i/8, j/8)
                    block = self.vidData.getBlock(frame, i, j, self.__blockSize)
                    
                    blockDCT[cntr,:] = self.computeDCT(block, self.__blockSize, blockType)
#                    print blockDCT[cntr,:]
                    cntr = cntr + 1
            cntr_frame = cntr_frame + 1
            if cntr_frame % 10 == 0:
                np.savetxt('DCT'+str(cntr_frame) + '.cmp', blockDCT, fmt='%1.1f')
                cntr = 0
                print time.time() - st
                        
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
#        np.savetxt('DCT.cmp', blockDCT, fmt='%1.1f')
#        dct_file.close
        print time.time() - st

    # def quantize(self):
        # DCT_matrix = loadFromCMP()
        # n1 = 2
        # n2 = 3    
        # for i in range(self.vidData.getNumBlocks(8)*self.vidData.totalFrames):
            # if (DCT_matrix[i,0] == 0.0):
                # DCT_matrix[i,1:] = [int(a / n1)*n1 for a in DCT_matrix[i,1:]]
            # else:
                # DCT_matrix[i,1:] = [int(a / n2)*n2 for a in DCT_matrix[i,1:]]
        # return DCT_matrix
