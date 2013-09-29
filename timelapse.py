#!/usr/bin/env python

import sys
import pygame
import time
import subprocess
import os
import pygame.camera
import datetime



def grab_images(imgcount):
    """Initialize camera and grab still images"""

    print imgcount

    try:
        pygame.camera.init()
        cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        cam.start()
    except:
        print "Could not initialize camera"


    for i in range(0, int(imgcount)):
        print '\r', i, '/', imgcount,
        sys.stdout.flush()
        epoch = str(time.time())
        img = cam.get_image()
        pygame.image.save(img, "tmpdir/photo-" + epoch + ".jpg")
        time.sleep(1)

    pygame.camera.quit()


def launch_mencoder():
    """Launch mencoder with proper args"""
    mencoder_proc = subprocess.Popen(
        [
            'mencoder',
            'mf://tmpdir/*.jpg',
            '-mf', 'w=800:h=600:fps=25:type=jpg',
            '-ovc', 'lavc',
            '-lavcopts', 'vcodec=mpeg4:mbd=2:trell',
            '-oac', 'copy',
            '-o', 'output.avi'
            ],
        stdout=sys.stdout,
        stderr=sys.stderr
        )

    retval = mencoder_proc.wait()

    print "Return value %s" % retval


def main():
    """Parse argv and launch functions"""
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: ./grab.py [number of images in time lapse]")
        sys.exit(1)

    grab_images(sys.argv[1])
    launch_mencoder()


if __name__ == "__main__":
    main()

