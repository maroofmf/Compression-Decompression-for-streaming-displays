'''
Description: The main file for encoder
#----------------------------------------------------------------------------------------------------------------#
Notes:

'''

#----------------------------------------------------------------------------------------------------------------#
from videoData import videoData
from compression import compression
from segmentation import segmentation
import sys
#----------------------------------------------------------------------------------------------------------------#
def main():
    fileName = sys.argv[1]
    height = 540
    width = 960
    channels = 3
    vidData = videoData(fileName, height, width, channels)
    compressor = compression(1,1,vidData);
    compressor.saveCMP()
#----------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
