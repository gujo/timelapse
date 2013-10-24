#!/usr/bin/env python
"""Grab images from webcam and make time lapse videos"""


import sys
import os
import glob
import pygame
import time
import subprocess
import pygame.camera
import argparse


def grab_images(imgcount, delay):
    """Initialize camera and grab still images"""

    try:
        pygame.camera.init()
        cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        cam.start()
    except:
        print "Could not initialize camera"
        sys.exit(1)

    if not os.path.exists("tmpdir"):
        os.makedirs("tmpdir")

    for i in range(0, imgcount):
        print '\r', i + 1, '/', imgcount,
        sys.stdout.flush()
        epoch = str(time.time())
        img = cam.get_image()
        pygame.image.save(img, "tmpdir/photo-" + epoch + ".jpg")
        time.sleep(delay)

    print ""

    pygame.camera.quit()


def launch_mencoder(fps, output):
    """Launch mencoder with proper args"""
    mencoder_proc = subprocess.Popen(
        [
            'mencoder',
            'mf://tmpdir/*.jpg',
            '-mf', 'w=800:h=600:fps=' + str(fps) + ':type=jpg',
            '-ovc', 'lavc',
            '-lavcopts', 'vcodec=mpeg4:mbd=2:trell',
            '-oac', 'copy',
            '-o', str(output),
            '-really-quiet'
            ],
        stdout=sys.stdout,
        stderr=sys.stderr
        )

    retval = mencoder_proc.wait()

    os.chdir("tmpdir")
    files = glob.glob("*.jpg")
    for filename in files:
        os.unlink(filename)

    return retval


def main():
    """Parse argv and launch functions"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', type=int, required=True,
                        help='Number of images to grab')

    parser.add_argument('-d', '--delay', type=int, default=1,
                        help='Delay between images, defaults to 1 sec')

    parser.add_argument('-f', '--fps', type=int, default=25,
                        help='Frames per second in movie, defaults to 25')

    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output filename')

    args = parser.parse_args()

    print "Grabbing images... "
    grab_images(args.count, args.delay)

    print "Compiling Video..."
    launch_mencoder(args.fps, args.output)


if __name__ == "__main__":
    main()
