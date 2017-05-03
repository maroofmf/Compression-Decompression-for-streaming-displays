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
		self.fileName = FILE_NAME
		self.iteratorIndex = 0
		self.width = WIDTH
		self.height = HEIGHT
		self.channels = CHANNELS
		self.patch = 0

		# Load from file if FILE_NAME is mentioned
		if(self.fileName):
			self.videoFrames = np.fromfile(FILE_NAME, dtype ='uint8')
			self.totalFrames = int(len(self.videoFrames)/(WIDTH*HEIGHT*CHANNELS))
			self.blockLabels = np.zeros((int(self.totalFrames),int(math.ceil(self.height/8.0)),int(math.ceil(self.width/8.0))))
			self.videoFrames = self.videoFrames.reshape((self.totalFrames, self.channels, self.height, self.width))
			#self.videoFrames = np.transpose(self.videoFrames,(0,2,3,1))

		else:
			self.videoFrames = None
			self.totalFrames = None
			self.blockLabels = None
			self.videoFrames_orig = None

#----------------------------------------------------------------------------------------------------------------#
# create instance from array:

	@classmethod
	def fromArray(cls,videoArray,HEIGHT,WIDTH,CHANNELS):
		instance = cls(None,HEIGHT,WIDTH,CHANNELS)
		instance.videoFrames = videoArray
		instance.videoFrames_orig = videoArray.copy()
		instance.totalFrames = np.size(videoArray)/(WIDTH*HEIGHT*CHANNELS)
		instance.blockLabels = np.zeros((int(instance.totalFrames),int(math.ceil(HEIGHT/8.0)),int(math.ceil(WIDTH/8.0))))
		return instance

#----------------------------------------------------------------------------------------------------------------#
# Metadata:

	def writeMetaData(self):
		metaData = str(int(self.__width))+'\n'
		metaData += str(int(self.__height))+'\n'
		metaData += str(int(self.__channels))+'\n'
		metaData += str(int(self.totalFrames))+'\n'
		metaData += str(int(self.__frameRate))

		metaFile = open('MetaData.txt','w')
		metaFile.write(metaData)
		metaFile.close()

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

		'''
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
		'''

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

		return self.videoFrames[frameNumber, :,:,:]

	def getBlock(self, frameNumber, i, j, block_size):
		return self.videoFrames[frameNumber, :, i:i+block_size, j:j+block_size]

#----------------------------------------------------------------------------------------------------------------#
# Set values in current Frame:

	def setBlock(self,frameNumber,i,j,block_size):

		# Perform checks:
		if(frameNumber>=self.totalFrames):
			frameNumber =0

		self.patch = self.getBlock(frameNumber,i,j,block_size).copy()
		self.videoFrames[frameNumber,:,i:i+block_size,j:j+block_size] = 0

#----------------------------------------------------------------------------------------------------------------#
# Repatch:

	def repatch(self,frameNumber,i,j,block_size):

		# Perform checks:
		if(frameNumber>=self.totalFrames):
			frameNumber =0

		self.videoFrames[frameNumber,:,i:i+block_size,j:j+block_size] = self.patch

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
	b = videoData.fromArray(a.videoFrames,540,960,3)
	print(np.shape(np.transpose(a.currentFrame(),(1,2,0))))

