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

    def computeDCT(self):
        for channel in range (self.__channels):
             block = block3D[:][:][channel]
             block_f = np.float32(block)  # float conversion/scale
             dct_coeffs = cv2.dct(block_f)           # the dct
             str1 = "Type "
             for i in range(self.__blockSize):
                 str1 = str1 + str(dct_coeffs[i][0:])
             dct_row_str = str1.replace("\n", "")
             with open('DCT.cmp', 'w') as myFile:
                 
                 myFile.write(dct_row_str)
        myFile.write("\n")
         

    def computeIDCT(self):

    def loadFromCMP(self):
        # set dctCOEFF

    def saveCMP(self):
        # put DCT into a file

    def quantize(self):
