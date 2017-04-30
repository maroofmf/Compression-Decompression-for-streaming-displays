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
def main():
    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
    gazeControl = int(sys.argv[3])

    height = 540
    width = 960
    channels = 3
    frameRate = 30
    totalFrames = 30
    #------------------------------ Construct objects ----------------------------------#
    #vidPlayer = videoData(fileName, height, width, channels, frameRate)
    decompressor = decompression(n1, n2, totalFrames);
    
    #------------------------------- Read all the frames -------------------------------#
    DCTVid = decompressor.loadFromCMP()
    quantizedDCTVid = decompressor.quantize(DCTVid)
    rgbVid = decompressor.computeIDCT(quantizedDCTVid)
##----------------------------------------------------------------------------------------------------------------##
if __name__ == '__main__':
    main()
