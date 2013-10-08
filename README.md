Timelapse.py
============

Grab images from webcam and make time lapse videos

Usage
-----

	Usage: timelapse.py [-h] -c COUNT [-d DELAY] [-f FPS] -o OUTPUT

	optional arguments:
	  -h, --help            show this help message and exit
	  -c COUNT, --count COUNT
	                        Number of images to grab
          -d DELAY, --delay DELAY
				Delay between images, defaults to 1 sec
	  -f FPS, --fps FPS     Frames per second in movie, defaults to 25
	  -o OUTPUT, --output OUTPUT 
	     	     	      	 Output filename

Requires
--------

* python-pygame
* mencoder