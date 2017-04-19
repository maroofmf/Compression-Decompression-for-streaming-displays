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
        self.getNextBlock()

    def computeIDCT(self):

    def loadFromCMP(self):
        # set dctCOEFF

    def saveCMP(self):
        # put DCT into a file

    def quantize(self):
