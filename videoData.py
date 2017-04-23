'''
Description: Read and index video data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
# Importing dependancies:

import numpy as np

#----------------------------------------------------------------------------------------------------------------#

class videoData:

	def __init__(self, FILE_NAME, HEIGHT, WIDTH, CHANNELS):

		print('\033[1;33m[Status]==> Loading video file\033[0m')
		self.__videoFrames = np.fromfile(FILE_NAME, dtype ='uint8')
		self.width = WIDTH
		self.height = HEIGHT
		self.channels = CHANNELS
		self.totalFrames = len(self.__videoFrames)/(WIDTH*HEIGHT*CHANNELS)

#----------------------------------------------------------------------------------------------------------------#
# Retrieve frame data in RGB format:

	def getFrame(self,frameNumber):

		frame = np.empty((self.height,self.width, self.channels),'uint8')
		frameOffset = frameNumber*self.height*self.width*self.channels

		# Loop through all channels
		for c in range(self.channels):
			channelOffset = self.height*self.width*c
			startIndex = frameOffset + channelOffset
			endIndex =	startIndex + self.height*self.width
			frame[:,:,c] = np.copy((self.__videoFrames[startIndex:endIndex]).reshape((self.height,self.width)))

		return frame

#----------------------------------------------------------------------------------------------------------------#
# Iterate through frames:

	def iterator(self,startFrame=0):
		for i in range(self.totalFrames):
			yield(self.getFrame(startFrame+i))

