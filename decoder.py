'''
Description: The main file for decoder
##----------------------------------------------------------------------------------------------------------------##
Notes:

'''

##----------------------------------------------------------------------------------------------------------------##
from videoPlayer import videoPlayer
from videoData import videoData
from decompression import decompression
import time, sys, numpy as np, cv2
import os
from tempfile import TemporaryFile
import sys

##----------------------------------------------------------------------------------------------------------------##
def parseMetaData():
    metaFile = open('MetaData.txt', 'r')
    metaDataStr = metaFile.read().split('\n')
    width, height, channels, totalFrames, frameRate = map(int, metaDataStr)
    metaFile.close()
    return width, height, channels, totalFrames, frameRate
##----------------------------------------------------------------------------------------------------------------##
def main():

    print('PID: %d',os.getpid())

    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
    gazeControl = int(sys.argv[3])
    width, height, channels, totalFrames, frameRate = parseMetaData()

    # height = 540
    # width = 960
    # channels = 3
    # frameRate = 30

    #------------------------------ Construct objects ----------------------------------#
    #vidPlayer = videoData(fileName, height, width, channels, frameRate)
    decompressor = decompression(n1, n2, totalFrames);

    #------------------------------- Read all the frames -------------------------------#

    decompressor.loadFromCMP() # [DCT BLOCKS, DCT COEFFICIENTS]
    startTime = time.time()
    quantizedDCTVid = decompressor.quantize()
    print('Total deq time: ',time.time()-startTime)
    startTime = time.time()
    rgbVid = decompressor.computeIDCT_Vid(quantizedDCTVid).astype(np.uint8)
    print('total decompress time:',time.time()-startTime)

    #Init a videoData:
    dataInstance = videoData.fromArray(rgbVid,height,width,channels)
    dataInstance.decompressor = decompressor

    #dataInstance.dctValues = DCTVid
    player = videoPlayer.fromVideoFile(dataInstance,20)

##----------------------------------------------------------------------------------------------------------------##
if __name__ == '__main__':
    main()
