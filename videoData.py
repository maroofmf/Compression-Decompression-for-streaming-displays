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
		self.videoFrames = np.fromfile(FILE_NAME, dtype ='uint8')
		self.width = WIDTH
		self.height = HEIGHT
		self.channels = CHANNELS
		self.totalFrames = len(self.videoFrames)/(WIDTH*HEIGHT*CHANNELS)
		self.iteratorIndex = 0

#----------------------------------------------------------------------------------------------------------------#
# Retrieve frame data in RGB format:

	def getFrame(self,frameNumber):

		# Check frameNumbers:
		if(self.iteratorIndex <0):
				self.iteratorIndex = self.totalFrames -1
				frameNumber = self.iteratorIndex

		if(self.iteratorIndex >= self.totalFrames):
				self.iteratorIndex = 0
				frameNumber = 0

		if(frameNumber >= self.totalFrames):
				frameNumber = self.totalFrames - 1

		if(frameNumber < 0):
				frameNumber = 0

		# Pre allocate frame memory
		frame = np.empty((self.height,self.width, self.channels),'uint8')
		frameOffset = frameNumber*self.height*self.width*self.channels

		# Loop through all channels
		for c in range(self.channels):
			channelOffset = self.height*self.width*c
			startIndex = frameOffset + channelOffset
			endIndex =	startIndex + self.height*self.width
			frame[:,:,c] = np.copy((self.videoFrames[startIndex:endIndex]).reshape((self.height,self.width)))

		return frame

#----------------------------------------------------------------------------------------------------------------#
# Get current Frame:

	def currentFrame(self):
		return(self.getFrame(self.iteratorIndex))


#----------------------------------------------------------------------------------------------------------------#
# Get next Frame:

	def nextFrame(self):
		self.iteratorIndex +=1
		return(self.getFrame(self.iteratorIndex))


#----------------------------------------------------------------------------------------------------------------#
# Get previous Frame:

	def prevFrame(self):
		self.iteratorIndex -=1
		return(self.getFrame(self.iteratorIndex))

#----------------------------------------------------------------------------------------------------------------#
# Iterate over frames:

	def iterator(self):
		while(True):
			yield(self.getFrame(self.iteratorIndex))
			self.iteratorIndex+=1


