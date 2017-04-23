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
class compression(segmentation):
    #------------------------------ Constructor ------------------------------#
    def __init__(self, n1, n2):
        self.quantStepFG = n1
		self.quantStepBG = n2

    def computeDCT(self,block3D, block_size):
#        print block3D
        block_dimention_updated = np.einsum('jki->ijk',block3D)
        dct_file = open('DCT.cmp', 'a')
        for channel in range (self.__channels):
             block = block_dimention_updated[:][:][channel]
             print 'Block',block
             block_f = np.float32(block)  # float conversion/scale
             dct_coeffs = cv2.dct(block_f)           # the dct
             str1 = "Type "
             for i in range(block_size):
                 str1 = str1 + str(dct_coeffs[i][0:])
             dct_row_str = str1.replace("\n", "")
             
                 
             dct_file.write(dct_row_str)
        dct_file.close
         

    def computeIDCT(self):

    def loadFromCMP(self):
        # set dctCOEFF

    def saveCMP(self):
        # put DCT into a file

    def quantize(self):
