# -*- coding: utf-8 -*-
'''
Created on Sat Apr 29 17:26:34 2017

@author: aggar
'''

import numpy as np
import cv2, math, time
from videoData import videoData

class decompression():
    def __init__(self,n1,n2,totalFrames):
        self.quantStepFG = n1
        self.quantStepBG = n2
        self.totalFrames = totalFrames
        self.framesPerCMP = 50

    def loadFromCMP(self):
        no_of_frames = self.framesPerCMP
        cmpCounter=0
        Dct_array = np.zeros((8160*self.totalFrames,193))
        startTime = time.time()
        for file_sel in range(int(math.ceil(1.0*self.totalFrames/no_of_frames))):
            startTime = time.time()
            if file_sel == int(math.ceil(1.0*self.totalFrames/no_of_frames))-1:
                tillFrame = 1.0*self.totalFrames/(file_sel+1)
                till_frame_number = self.totalFrames - file_sel*no_of_frames
            else:
                tillFrame = no_of_frames
                till_frame_number = no_of_frames

            f = open('DCT' + str(int((file_sel+1) * tillFrame))+'.cmp')
            cntr1 = 0
            for line in f.read().split('\n'):
                dctNumsStr = line.split(' ')
                Dct_array[cmpCounter,:] = list(map(float,dctNumsStr))
                frameCount = int(cmpCounter/8160)
                cmpCounter = cmpCounter +  1
                cntr1 = cntr1 + 1
                if cntr1 == 8160 * till_frame_number:
                    break
            if frameCount==self.totalFrames:
                break
            print('Loaded', str(int((file_sel+1) * tillFrame))+'.cmp in ', time.time() - startTime, 'sec')
        return Dct_array

    def quantize(self, Dct_array):
        self.totalFrames = self.totalFrames
        no_of_frames = self.framesPerCMP
        for interval in range(int(math.ceil(1.0*self.totalFrames/no_of_frames))):
            if interval == int(math.ceil(1.0*self.totalFrames/no_of_frames))-1:
                till_frame_number = self.totalFrames - interval*no_of_frames
            else:
                till_frame_number = no_of_frames
            bGIndices = np.where(Dct_array[interval*8160*no_of_frames:interval*8160*no_of_frames + 8160*till_frame_number,0] < 0.1)[0]
            Dct_array[bGIndices,1:] = Dct_array[bGIndices,1:]/self.quantStepBG
            Dct_array[bGIndices,1:] = np.round(Dct_array[bGIndices,1:])
            Dct_array[bGIndices,1:] = Dct_array[bGIndices,1:]*self.quantStepBG

            fGIndices = np.where(Dct_array[interval*8160*no_of_frames:interval*8160*no_of_frames + 8160*till_frame_number,0] > 0.9)[0]
            Dct_array[fGIndices,1:] = Dct_array[fGIndices,1:]/self.quantStepFG
            Dct_array[fGIndices,1:] = np.round(Dct_array[fGIndices,1:])
            Dct_array[fGIndices,1:] = Dct_array[fGIndices,1:]*self.quantStepFG

        return Dct_array

    def computeIDCT(self,dequantised_coef):
        rgb_frames = np.zeros((self.totalFrames,3,540,960))
        iIndices = list(range(0, 540, 8))
        jIndices = list(range(0, 960, 8))
        iIndices[-1] = 540 - 8
        jIndices[-1] = 960 - 8

        for frame in range(self.totalFrames):
            block_cntr = 0
            for i in iIndices:
                for j in jIndices:
                    for channel in range (3):
                        rgb_frames[frame,channel,i:i+8,j:j+8] = cv2.idct(dequantised_coef[8160*frame+block_cntr,(channel*64)+1:((channel+1)*64)+1].reshape(8,8))
                    block_cntr = block_cntr + 1

        return rgb_frames
