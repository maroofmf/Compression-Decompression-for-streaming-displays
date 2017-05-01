'''
Description: Read and index video data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''

#----------------------------------------------------------------------------------------------------------------#
# Importing dependancies:

import numpy as np
import math

class videoData:

	def __init__(self, FILE_NAME, HEIGHT, WIDTH, CHANNELS):

		print('\033[1;33m[Status]==> Loading video file\033[0m')
		self.videoFrames = np.fromfile(FILE_NAME, dtype ='uint8')
		self.width = WIDTH
		self.height = HEIGHT
		self.channels = CHANNELS
		self.totalFrames = len(self.videoFrames)/(WIDTH*HEIGHT*CHANNELS)
		self.iteratorIndex = 0
		self.blockLabels = np.zeros((int(self.totalFrames),int(math.ceil(self.height/8.0)),int(math.ceil(self.width/8.0))))
		#--- Reshape videoFrame from 1 x (540_rows x 960_cols x 3_channels x 363_frames) --------------------#
		#---------------------- to (363_frames) x (3_channels) x (540_rows) x (960_cols) --------------------#
		self.videoFrames = self.videoFrames.reshape((int(self.totalFrames), int(self.channels), int(self.height), int(self.width)))

#----------------------------------------------------------------------------------------------------------------#
# Getters:

	def getNumChannels(self):
		return self.channels

	def getHeight(self):
		return self.height

	def getWidth(self):
		return self.width

	def getNumBlocks(self,blockSize):
		noOfBlocks =  math.ceil(1.0*self.width/blockSize) * math.ceil(1.0*self.height/blockSize)
		return int(noOfBlocks)

	def getLabel(self, frameNumber, i, j):
		return self.blockLabels[int(frameNumber), int(i), int(j)]

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

		# Retrive frame
		frame = self.videoFrames[frameNumber, :,:,:]
		return frame

	def getBlock(self, frameNumber, i, j, block_size):
		block3D = self.videoFrames[frameNumber, :, i:i+block_size, j:j+block_size]
		return block3D

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

#----------------------------------------------------------------------------------------------------------------#
# Boiler-plate syntax for testing only:

if __name__ =='__main__':
	print('Started')
	a = videoData('oneperson_960_540.rgb',540,960,3)
	arr = a.nextFrame()
	print(np.shape(arr))
