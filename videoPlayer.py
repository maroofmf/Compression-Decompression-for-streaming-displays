'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
from videoData import videoData
import time
import cv2

class videoPlayer(videoData):
	def __init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS, FRAMERATE):
		videoData.__init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS)
		self.__frameRate = FRAMERATE
		
	def sync(self, systemTime):
		time.sleep((1.0/self.__frameRate) - systemTime)

def main():
	vidPlayer = videoPlayer('oneperson_960_540.rgb',540, 960, 3, 30)
	for systemTime, frame in vidPlayer.iterator():
		cv2.imshow('frame',frame)
		vidPlayer.sync(systemTime);
		if cv2.waitKey(1) & 0xFF == ord('h'):
			break
	cv2.destroyAllWindows()
if __name__ == '__main__':
	main()
