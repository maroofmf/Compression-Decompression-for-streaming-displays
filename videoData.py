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
import sys

class videoData:

	def __init__(self, FILE_NAME, HEIGHT, WIDTH, CHANNELS):

		print('\033[1;33m[Status]==> Loading video file\033[0m')
		self.fileName = FILE_NAME
		self.iteratorIndex = 0
		self.width = WIDTH
		self.height = HEIGHT
		self.channels = CHANNELS
		self.patch = 0
		self.decompressor = None

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

#----------------------------------------------------------------------------------------------------------------#
# Get values in given Frame:

	def getBlock(self, frameNumber, i, j, block_size):

		# Perform checks:
		if(frameNumber>=self.totalFrames):
			frameNumber =0

		i_low = i
		i_high = i+block_size
		j_low = j
		j_high = j+block_size

		if(i<0):
			i_low=0
			i_high = block_size+i

		if(j<0):
			j_low=0
			j_high = block_size+j

		return self.videoFrames[frameNumber, :, i_low:i_high, j_low:j_high]

#----------------------------------------------------------------------------------------------------------------#
# Set values in given Frame:

	def setBlock(self,frameNumber,i,j,block_size,blockValues = 0):

		# Perform checks:
		if(frameNumber>=self.totalFrames):
			frameNumber =0

		i_low = i
		i_high = i+block_size
		j_low = j
		j_high = j+block_size

		if(i<0):
			i_low=0
			i_high = block_size+i

		if(j<0):
			j_low=0
			j_high = block_size+j

		#print(np.shape(blockValues),np.shape(self.videoFrames[frameNumber, :, i_low:i_high, j_low:j_high]))
		self.videoFrames[frameNumber, :, i_low:i_high, j_low:j_high] = blockValues

#----------------------------------------------------------------------------------------------------------------#
# Requantize Frame:

	def reQuantize(self,frameNumber,i,j,block_size):

		# Perform checks:
		if(frameNumber>=self.totalFrames):
			frameNumber =0
		'''
		# Compute i and j for top right corner;
		topLeft = [i-block_size//2,j-block_size//2]

		if(topLeft[0] <0):
			topLeft[0] = 0
		if(topLeft[0] >=self.height):
			topLeft[0] = 528
		if(topLeft[1] <0):
			topLeft[1] = 0
		if(topLeft[1] >=self.width):
			topLeft[1] = 952

		# Compute i and j for top right corner;
		bottomRight = [i+block_size//2,j+block_size//2]

		if(bottomRight[0] <0):
			bottomRight[0] = 0
		if(bottomRight[0] >=self.height):
			bottomRight[0] = 528
		if(bottomRight[1] <0):
			bottomRight[1] = 0
		if(bottomRight[1] >=self.width):
			bottomRight[1] = 952

		# Get image Patch:
		patch = np.empty((1,3,8,8),np.uint8)

		i=topLeft[0]
		j=topLeft[1]
		totalRows = (bottomRight[0]-topLeft[0])//8+1
		totalCols = (bottomRight[1]-topLeft[1])//8+1

		while(i<bottomRight[0]):
			while(j<bottomRight[1]):
				blocks = ((i//8)*120+(j//8)+frameNumber*8160)
				#patch = self.decompressor.computeIDCT(blocks)
				patch1 = np.zeros((1,3,8,8),dtype=np.uint8)
				patch = np.append(patch,patch1,0)
				j+=8
			i+=8


		# Get block numbers:
		tempPatch = np.empty((3,8,8))
		first= True
		for h_offset in range(i-block_size//2,i+block_size//2,8):
			for w_offset in range(i-block_size//2,i+block_size//2,8):

				if(h_offset<0 or w_offset<0):
					continue

				tempPatch = np.append(tempPatch,np.zeros((3,8,8)),2)

			patch = np.append(patch,tempPatch,1)


		print(np.shape(patch))
		#print(totalRows,totalCols)
		#patch = patch.reshape(3,-(topLeft[0]-bottomRight[0])+8,-(topLeft[1]-bottomRight[1]+8))
		#print(3,(topLeft[0]-bottomRight[0])//8,(topLeft[1]-bottomRight[1])//8)
		'''

		# Get block numbers:
		blockList = []
		temp = []
		for h_offset in range(i-block_size//2,i+block_size//2,8):
			for w_offset in range(j-block_size//2,j+block_size//2,8):

				if(h_offset<0 or w_offset<0 or h_offset>=self.height or w_offset>=self.width):
					continue

				blocks = ((h_offset//8)*120+(w_offset//8)+frameNumber*8160)
				temp.append(blocks)

			if(not len(temp)==0):
				blockList.append(temp)
				temp = []

		# Set patch:
		self.patch = self.getBlock(frameNumber,i-block_size//2,j-block_size//2,block_size).copy()

		patch = np.zeros((3,np.shape(self.patch)[1],np.shape(self.patch)[2]))

		for index1,rows in enumerate(blockList):
			for index2,columns in enumerate(rows):

				if(not np.shape(patch[:,index1*8:8*(index1+1),index2*8:8*(index2+1)])==(3,8,8)):
					#print(index1,index2,np.shape(patch[:,index1*8:8*(index1+1),index2*8:8*(index2+1)]),np.shape(patch))
					patch[:,index1*8-4:8*(index1+1),index2*8:8*(index2+1)] = self.decompressor.computeIDCT(columns)
					continue

				patch[:,index1*8:8*(index1+1),index2*8:8*(index2+1)] = self.decompressor.computeIDCT(columns)
				#patch[:,index1*8:8*(index1+1),index2*8:8*(index2+1)] = np.zeros((3,8,8))

		self.setBlock(frameNumber,i-block_size//2,j-block_size//2,block_size,patch)

#----------------------------------------------------------------------------------------------------------------#
# Repatch:

	def repatch(self,frameNumber,i,j,block_size):

		# Perform checks:
		if(frameNumber>=self.totalFrames):
			frameNumber =0

		self.setBlock(frameNumber,i-block_size//2,j-block_size//2,block_size,self.patch)

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

