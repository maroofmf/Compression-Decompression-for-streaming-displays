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
    fileName = 'oneperson_960_540.rgb'
    height = 540
    width = 960
    channels = 3
    
    #------------------------------ Construct objects ----------------------------------#
    vidData = videoData(fileName, height, width, channels)
    compressor = compression(vidData);
    searchWin = 20
    segmentor = segmentation(vidData, searchWin)
    #-----------------------------------------------------------------------------------#
    
    #------------------------------- Set numpy format ----------------------------------#
    float_formatter = lambda x: "%.1f" % x
    np.set_printoptions(formatter={'float_kind':float_formatter})
    startTime = time.time()
    #-----------------------------------------------------------------------------------#
    
    #------------------------- Segment from the 2nd frame ------------------------------#
    print 'Starting segmentation: '
    y_weight = 0.3
    S_weight = 0.7    
    prevFrame = vidData.getFrame(0)
    prevFrame = y_weight*segmentor.YfromRGB(prevFrame) + S_weight*segmentor.SfromRGB(prevFrame)
    for frameNumber in range (1, vidData.totalFrames):
        #---------------- Segment the Nth frame in the segmentor -----------------------#
        currFrame = vidData.getFrame(frameNumber)
        currFrame = y_weight*segmentor.YfromRGB(currFrame) + S_weight*segmentor.SfromRGB(currFrame)
        # cv2.imshow('frame', np.uint8(currFrame))
        # cv2.waitKey(0)
        segmentor.segmentBlocksInFrame(currFrame, prevFrame, frameNumber)
        if frameNumber%10 == 0 or frameNumber==vidData.totalFrames-1:
            print 'Total frames segmented', frameNumber
        # print vidData.getLabel(frameNumber, 336/8, 192/8)
        #---------------------------- Update prevFrame ---------------------------------#
        prevFrame = currFrame
    #-----------------------------------------------------------------------------------#
    
    #----------------- Compress all the frames using label knowledge -------------------#
    print 'Time to segment all frames', time.time()-startTime, 'sec\n\n'
    
    print 'Starting compression: '
    startTime = time.time()
    compressor.saveCMP()
    print 'Time to segment all frames', time.time()-startTime, 'sec\n\n'
    
    #-----------------------------------------------------------------------------------#
##----------------------------------------------------------------------------------------------------------------##
if __name__ == '__main__':
    main()
