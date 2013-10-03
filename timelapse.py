#!/usr/bin/env python

import sys
import os
import glob
import pygame
import time
import subprocess
import pygame.camera


def grab_images(imgcount, delay):
    """Initialize camera and grab still images"""

    try:
        pygame.camera.init()
        cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        cam.start()
    except:
        print "Could not initialize camera"
        sys.exit(1)

    for i in range(0, imgcount):
        print '\r', i, '/', imgcount,
        sys.stdout.flush()
        epoch = str(time.time())
        img = cam.get_image()
        pygame.image.save(img, "tmpdir/photo-" + epoch + ".jpg")
        time.sleep(delay)

    pygame.camera.quit()


def launch_mencoder(fps):
    """Launch mencoder with proper args"""
    mencoder_proc = subprocess.Popen(
        [
            'mencoder',
            'mf://tmpdir/*.jpg',
            '-mf', 'w=800:h=600:fps='+str(fps)+':type=jpg',
            '-ovc', 'lavc',
            '-lavcopts', 'vcodec=mpeg4:mbd=2:trell',
            '-oac', 'copy',
            '-o', 'output.avi',
            '-really-quiet'
            ],
        stdout=sys.stdout,
        stderr=sys.stderr
        )

    retval = mencoder_proc.wait()

    print "Return value %s" % retval

    os.chdir("tmpdir")
    files = glob.glob("*.jpg")
    for filename in files:
        os.unlink(filename)


def main():
    """Parse argv and launch functions"""
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: ./grab.py [count] [delay] [fps]")
        sys.exit(1)

    grab_images(int(sys.argv[1]), int(sys.argv[2]))
    launch_mencoder(int(sys.argv[3]))


if __name__ == "__main__":
    main()
