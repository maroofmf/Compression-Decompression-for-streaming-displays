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
import os
##----------------------------------------------------------------------------------------------------------------##
def main():
    print('PID: %d'%(os.getpid()))
    #fileName = 'oneperson_960_540.rgb'
    fileName = sys.argv[1]
    height = 540
    width = 960
    channels = 3

    #------------------------------ Construct objects ----------------------------------#
    vidData = videoData(fileName, height, width, channels)
    vidData.writeMetaData()
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
    print('Starting segmentation: ')
    y_weight = 0.8
    H_weight = 0.1
    S_weight = 0.1
    prevFrame = vidData.getFrame(0)
    prevFrame = y_weight*segmentor.YfromRGB(prevFrame) + H_weight*segmentor.HfromRGB(prevFrame) + S_weight*segmentor.SfromRGB(prevFrame)

    SAD_Thresh_list = range(5000, 12001, 1000)
    threshIndex = 1

    for frameNumber in range (1, vidData.totalFrames):
        #---------------- Segment the Nth frame in the segmentor -----------------------#
        currFrame = vidData.getFrame(frameNumber)
        currFrame = y_weight*segmentor.YfromRGB(currFrame) + H_weight*segmentor.HfromRGB(currFrame) + S_weight*segmentor.SfromRGB(currFrame)
        # cv2.imshow('frame', np.uint8(currFrame))
        # cv2.waitKey(0)

        foregroundCount = segmentor.segmentBlocksInFrame(currFrame, prevFrame, frameNumber, SAD_Thresh_list[threshIndex])
        #print SAD_Thresh_list[threshIndex]

        if(foregroundCount>100):
            threshIndex += 1
            threshIndex = min(len(SAD_Thresh_list)-1, threshIndex)
        elif(foregroundCount<20):
            threshIndex -= 1
            threshIndex = max(0, threshIndex)

        if frameNumber%10 == 0 or frameNumber==vidData.totalFrames-1:
            print('Total frames segmented', frameNumber)
        # print vidData.getLabel(frameNumber, 336/8, 192/8)
        #---------------------------- Update prevFrame ---------------------------------#
        prevFrame1 = vidData.getFrame(frameNumber)
        prevFrame1 = y_weight*segmentor.YfromRGB(prevFrame1) + H_weight*segmentor.HfromRGB(prevFrame1) + S_weight*segmentor.SfromRGB(prevFrame1)
        prevFrame = prevFrame1
    #-----------------------------------------------------------------------------------#

    #----------------- Compress all the frames using label knowledge -------------------#
    print('Time to segment all frames', time.time()-startTime, 'sec\n\n')

    print('Starting compression: ')
    startTime = time.time()
    compressor.saveCMP()
    print('Time to compress all frames', time.time()-startTime, 'sec\n\n')

    #-----------------------------------------------------------------------------------#
##----------------------------------------------------------------------------------------------------------------##
if __name__ == '__main__':
    main()
