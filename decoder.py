'''
Description: The main file for decoder
##----------------------------------------------------------------------------------------------------------------##
Notes:

'''

##----------------------------------------------------------------------------------------------------------------##
from videoPlayer import videoPlayer
from decompression import decompression
import time, sys, numpy as np, cv2
##----------------------------------------------------------------------------------------------------------------##
def parseMetaData():
    metaFile = open('MetaData.txt', 'r')
    metaDataStr = metaFile.read().split('\n')
    width, height, channels, totalFrames, frameRate = map(int, metaDataStr)
    metaFile.close()
    return width, height, channels, totalFrames, frameRate
##----------------------------------------------------------------------------------------------------------------##
def main():

    n1 = 1#int(sys.argv[1])
    n2 = 100#int(sys.argv[2])
    gazeControl = 0#int(sys.argv[3])
    width, height, channels, totalFrames, frameRate = parseMetaData()
    
    # height = 540
    # width = 960
    # channels = 3
    # frameRate = 30

    #------------------------------ Construct objects ----------------------------------#
    #vidPlayer = videoData(fileName, height, width, channels, frameRate)
    decompressor = decompression(n1, n2, totalFrames);
    
    #------------------------------- Read all the frames -------------------------------#
    
    DCTVid = decompressor.loadFromCMP()
    quantizedDCTVid = decompressor.quantize(DCTVid)
    rgbVid = decompressor.computeIDCT_Vid(quantizedDCTVid)
    img = np.zeros((height, width, channels), dtype = np.uint8)
    for i in range(channels):
        img[:,:,2-i] = np.uint8(rgbVid[3, i,:,:])
    cv2.imshow('img', img)
    cv2.waitKey(0)
    videoFrames = np.empty(totalFrames*channels*height*width,'uint8')
    videoFrames = rgbVid.reshape((totalFrames*channels*height*width))
#    print videoFrames.shape
##----------------------------------------------------------------------------------------------------------------##
if __name__ == '__main__':
    main()
