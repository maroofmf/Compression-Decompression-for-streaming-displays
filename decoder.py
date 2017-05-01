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
    n1 = 50#int(sys.argv[1])
    n2 = 200#int(sys.argv[2])
    gazeControl = 1#int(sys.argv[3])

    height = 540
    width = 960
    channels = 3
    frameRate = 30
    totalFrames = 363
    #------------------------------ Construct objects ----------------------------------#
    #vidPlayer = videoData(fileName, height, width, channels, frameRate)
    decompressor = decompression(n1, n2, totalFrames);
    
    #------------------------------- Read all the frames -------------------------------#
    
    DCTVid = decompressor.loadFromCMP()
    quantizedDCTVid = decompressor.quantize(DCTVid)
    rgbVid = decompressor.computeIDCT(quantizedDCTVid)
    img = np.zeros((height, width, channels), dtype = np.uint8)
    for i in range(channels):
        img[:,:,2-i] = np.uint8(rgbVid[100, i,:,:])
    cv2.imshow('img', img)
    cv2.waitKey(0)
##----------------------------------------------------------------------------------------------------------------##
if __name__ == '__main__':
    main()
