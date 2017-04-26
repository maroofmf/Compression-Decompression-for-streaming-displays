'''
Description: The main file for encoder
##----------------------------------------------------------------------------------------------------------------##
Notes:

'''

##----------------------------------------------------------------------------------------------------------------##
from videoData import videoData
from compression import compression
from segmentation import segmentation
import time, sys, numpy as np
##----------------------------------------------------------------------------------------------------------------##
def main():
    fileName = 'oneperson_960_540.rgb' #sys.argv[1]
    height = 540
    width = 960
    channels = 3
    
    #------------------------------ Construct objects ----------------------------------#
    vidData = videoData(fileName, height, width, channels)
    compressor = compression(1,1,vidData);
    searchWin = 32
    segmentor = segmentation(vidData, searchWin)
    #------------------------------- Set numpy format ----------------------------------#
    float_formatter = lambda x: "%.1f" % x
    np.set_printoptions(formatter={'float_kind':float_formatter})
    
    #---------------------- Compress the I frame (1st frame) ---------------------------#
    time1 = time.time()
    dct_file = open('DCT.cmp', 'a')
    compressor.saveToCMP(0, dct_file)
    
    #--------------- Segment from the 2nd frame and continue to compress ---------------#
    prevFrame = vidData.getFrame(0)
    prevFrame = segmentor.YfromRGB(prevFrame)
    for frameNumber in range (1, vidData.totalFrame):
        if frameNumber%10==0:
            print 'Frame ', frameNumber
        #---------------- Segment the Nth frame in the segmentor -----------------------#
        # currFrame = vidData.getFrame(frameNumber)
        # currFrame = segmentor.YfromRGB(currFrame)
        # segmentor.segmentBlocksInFrame(currFrame, prevFrame)
        
        #--------------- Compress the Nth frame in the compressor ----------------------#
        compressor.saveToCMP(frameNumber, dct_file)
        
        #---------------------------- Update prevFrame ---------------------------------#
        #prevFrame = currFrame
    #-----------------------------------------------------------------------------------#
    dct_file.close
    print time.time()-time1
##----------------------------------------------------------------------------------------------------------------##
if __name__ == '__main__':
    main()
