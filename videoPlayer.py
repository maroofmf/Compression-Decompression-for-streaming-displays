'''
Description: Read and index data.
#----------------------------------------------------------------------------------------------------------------#
Class functions:


#----------------------------------------------------------------------------------------------------------------#
Notes:

'''
import Tkinter as tk, threading
from PIL import Image, ImageTk
import math
from videoData import videoData
import time

class videoPlayer(videoData):
	def __init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS):
		videoData.__init__(self, FILENAME, HEIGHT, WIDTH, CHANNELS)
		#self.__fileName = FILENAME

	# def playVid(self,gui):
	# 	#gui = Tkinter.Tk()
	# 	#for i in range(self.totalFrames):
	# 	for frame in self.iterator():
	# 		frameImage = Image.fromarray(frame)
	# 		guiPhoto = ImageTk.PhotoImage(frameImage)
	# 		Tkinter.Label(gui, image=guiPhoto).pack()

	# def play(self,gui):
	# 	gui.after(5,self.playVid,gui)
	# 	gui.mainloop() # Start the GUI


    # for image in video.iter_data():
    #     frame_image = ImageTk.PhotoImage(Image.fromarray(image))
    #     label.config(image=frame_image)
    #     label.image = frame_image

def stream(label, vidPlayer):
	for frame in vidPlayer.iterator():
		frameImage = Image.fromarray(frame)
		guiPhoto = ImageTk.PhotoImage(frameImage)
		label.config(image=guiPhoto)
		label.image = frameImage

def main():

	vidPlayer = videoPlayer('oneperson_960_540.rgb',540, 960, 3)
	#vidPlayer.playVid()
	gui = tk.Tk()
	my_label = tk.Label(gui)
	my_label.pack()
	thread = threading.Thread(target=stream, args=(my_label, vidPlayer),)
	thread.daemon = 1
	thread.start()
	gui.mainloop()


# def main():

# 	vidPlayer = videoPlayer('oneperson_960_540.rgb',540, 960, 3)
# 	#vidPlayer.playVid()
# 	gui = Tkinter.Tk()
# 	# for frame in vidPlayer.iterator():
# 	frame = vidPlayer.getFrame(0)
# 	frameImage = Image.fromarray(frame)
# 	guiPhoto = ImageTk.PhotoImage(frameImage)
# 	label = Tkinter.Label(gui, image = guiPhoto).pack()
	
	# frame = vidPlayer.getFrame(10)
	# frameImage = Image.fromarray(frame)
	# guiPhoto = ImageTk.PhotoImage(frameImage)


	gui.mainloop()

	# for frame in vidPlayer.iterator():
	# 	frameImage = Image.fromarray(frame)
	# 	guiPhoto = ImageTk.PhotoImage(frameImage)
	# 	label.config(image=guiPhoto)


	#vidPlayer.play(gui)


#-----------------------------------------------------------------------------------------------#
# Boilerplate code:

if __name__ == '__main__':
	main()
