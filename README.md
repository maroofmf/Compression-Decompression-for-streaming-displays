# Segmented and Gaze Controlled Decompression for Streaming displays such as VR

## I. Introduction:
While traditional multimedia applications such as games and video are still very popular, an emerging area generating significant interest in immersion around today's entertainment landscape requires the capture, streaming and rendering of high bandwidth audio/visual content. For example applications such as Virtual Reality, Augmented Reality, Telepresence etc – aim to work with high resolution omnidirectional video. Furthermore these videos may take the form of monoscopic (one) or stereoscopic(two) streams that need to be streamed to a VR headset. Immersion is possible only when the video is of high resolution with realtime and interactive feedback while browsing. This puts stringent requirements on computational platforms as well as the available streaming bandwidth in devices such as VR headsets. While processing/computing power of  such devices is on the rise, and the bandwidths of communication are also on the rise, successful systems that seamless interact with high resolution are still  challenge. One smart way to delivering such content is by adaptively encoding/decoding the content based on semantics in the video and using view dependent gaze to control the decoding
This project is an interesting application of block based motion detection and compression in video based communication industries. Here we will take a given video (in .rgb) as input that we will preprocess into semantic layers, encode each layer separately and store into a file for reading/streaming later. We have also design a player that will read this compressed file, selectively decode layers to display depending on which parts of the video you are gazing at (controlled by mouse pointer) and create the final displayed frames.

## II. Development:

**Language:** Python v3.6.0

**Dependencies:**
[1] OpenCV v3.2.0
[2] Numpy
[3] Pillow
[4] Scipy

**Tested on:**
OS: macOS Sierra
RAM: 8GB
Processor: 2.7 GHz dual-core i5 

## III. How to run:

**Input data** => Should be of .rgb format!  
**Intermediate output** => .npy file  

[1] To encode your .rgb file:

> python3 encoder.py <VIDEO_FILE_NAME.rgb>

[2] To decode and display the stored file:

> python3 decoder.py <n1> <n2> <0>

where:  
n1 - Foreground quantization factor (higher the value, worse the quality)  
n2 - Background quantization factor  

**P.S. -> May consume a lot of RAM and CPU.** 

## IV. File Structure:

[1] **videoData**: Class to handle and index video data.  
[2] **videoPlayer**: Class to set up instances of GUI  
[3] **segmentation**: Class to perform background-foreground segmentation  
[4] **encoder**: Main encoding script file  
[5] **decoder**: Main decoding script file  
[6] **compression**: Class with compression algorithms (DCT)
[7] **decompression**: Class with decompression algorithms (IDCT)
[8] **Metadata.txt**: Contains all the encoded video information  
[9] **metadata/\***: Contains GUI elements  

## V. Authors:  
[1] Aman Vora (amanvora@usc.edu)  
[2] Pranav Aggarwal (pvaggarw@usc.edu)  
[3] Maroof Mohammed Farooq (maroofmf@usc.edu)  

