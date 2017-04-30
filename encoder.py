'''
Description: The main file for encoder
##----------------------------------------------------------------------------------------------------------------##
Notes:

'''

##----------------------------------------------------------------------------------------------------------------##
from videoData import videoData
from compression import compression
from segmentation import segmentation
import time, sys, numpy as np, cv2
##----------------------------------------------------------------------------------------------------------------##
def main():
    fileName = sys.argv[1]
    height = 540
    width = 960
    channels = 3
    
    #------------------------------ Construct objects ----------------------------------#
    vidData = videoData(fileName, height, width, channels)
    compressor = compression(vidData);
    searchWin = 16
    segmentor = segmentation(vidData, searchWin)
    #------------------------------- Set numpy format ----------------------------------#
    float_formatter = lambda x: "%.1f" % x
    np.set_printoptions(formatter={'float_kind':float_formatter})
    
    #---------------------- Compress the I frame (1st frame) ---------------------------#
    # time1 = time.time()
    # dct_file = open('DCT.cmp', 'a')
    # compressor.saveToCMP(0, dct_file)
    
    #------------------------- Segment from the 2nd frame ------------------------------#
    prevFrame = vidData.getFrame(0)
    prevFrame = segmentor.YfromRGB(prevFrame)
    for frameNumber in range (1, vidData.totalFrames):
        #---------------- Segment the Nth frame in the segmentor -----------------------#
        currFrame = vidData.getFrame(frameNumber)
        currFrame = segmentor.YfromRGB(currFrame)
        # cv2.imshow('frame', np.uint8(currFrame))
        # cv2.waitKey(0)
        st = time.time()
        segmentor.segmentBlocksInFrame(currFrame, prevFrame, frameNumber)
        print 'Frame ', frameNumber, time.time() - st, 'sec'
        # print vidData.getLabel(frameNumber, 336/8, 192/8)
        #---------------------------- Update prevFrame ---------------------------------#
        prevFrame = currFrame
    #-----------------------------------------------------------------------------------#
    
    compressor.saveCMP()
    #----------------- Compress all the frames using label knowledge -------------------#
    
##----------------------------------------------------------------------------------------------------------------##
if __name__ == '__main__':
    main()
