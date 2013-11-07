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

    # We can either use -d and -c and to determine how many images to grab and
    # how often. Or we can use -t and -T and just give durations.

    parser = argparse.ArgumentParser()
    group1 = parser.add_mutually_exclusive_group()
    group2 = parser.add_mutually_exclusive_group()

    group1.add_argument('-c', '--count', type=int, required=False,
                        help='Number of images to grab')

    group2.add_argument('-d', '--delay', type=int, default=1,
                        help='Delay between images, defaults to 1 sec')

    parser.add_argument('-f', '--fps', type=int, default=25,
                        help='Frames per second in movie, defaults to 25')

    parser.add_argument('-o', '--output', type=str, required=False,
                        help='Output filename')

    group2.add_argument('-t', '--inputtime', type=str, required=False,
                        help='Duration of image grabbing (seconds)')

    group1.add_argument('-T', '--outputtime', type=str, required=False,
                        help='Time of the produced video file (seconds)')

    args = parser.parse_args()

    if args.count:
        count = args.count
        delay = args.delay
    elif args.outputtime:
        count = int(args.outputtime) * int(args.fps)
        delay = int(args.inputtime) / int(count)

    print "Will grab " + str(count) + " images with " + str(delay) + "s delay"
    print "Grabbing images... "
    grab_images(args.count, args.delay)

    print "Compiling Video..."
    launch_mencoder(args.fps, args.output)


if __name__ == "__main__":
    main()
