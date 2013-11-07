Timelapse.py
============

Grab images from webcam and make time lapse videos

[![Build Status](https://travis-ci.org/gujo/timelapse.png?branch=master)](https://travis-ci.org/gujo/timelapse)

Usage
-----

	usage: timelapse.py [-h] [-c COUNT] [-d DELAY] [-f FPS] [-o OUTPUT]
                           [-t INPUTTIME] [-T OUTPUTTIME]
	optional arguments:
	  -h, --help            show this help message and exit
	  -c COUNT, --count COUNT
                        Number of images to grab
	  -d DELAY, --delay DELAY
                        Delay between images, defaults to 1 sec
	  -f FPS, --fps FPS     Frames per second in movie, defaults to 25
	  -o OUTPUT, --output OUTPUT
                        Output filename
	  -t INPUTTIME, --inputtime INPUTTIME
                        Duration of image grabbing (seconds)
	  -T OUTPUTTIME, --outputtime OUTPUTTIME
                        Time of the produced video file (seconds)

Requires
--------

* python-pygame
* mencoder