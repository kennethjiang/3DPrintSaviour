#!/usr/bin/env python3

# import the necessary packages
from skimage.metrics import normalized_root_mse as compare_nrmse
from sys import argv, exit, stderr
from os.path import dirname
import cv2

# get filenames
fst_file = argv[1]
if fst_file[-4:] != '.jpg':
    exit()

# Set current image and previous image
curr = int(fst_file[-10:-4])
prev = curr - 1

# For the 1st and 2nd images, output 0
# 1st image is used as background image
# 2nd image has no previous image (gives errors as prev is BG)
if curr == 0:
    print("0 nan")
    stderr.write("Background Image\n")
    exit()
if curr == 1:
    print("1 nan")
    stderr.write("First Image, no previous images\n")
    exit()

snd_file = fst_file[:-10] + str(prev).rjust(6, '0') + '.jpg'

bg_file = fst_file[:-10] + '000000.jpg'

# convert the images to grayscale
grayA = cv2.imread(fst_file, 0)
grayB = cv2.imread(snd_file, 0)
grayBG = cv2.imread(bg_file, 0)

# Remove background and threshold to remove shadow effects
threshold = 20

diffA = cv2.absdiff(grayA, grayBG)
thresA = cv2.threshold(diffA, threshold, 255, cv2.THRESH_BINARY)[1]

diffB = cv2.absdiff(grayB, grayBG)
thresB = cv2.threshold(diffB, threshold, 255, cv2.THRESH_BINARY)[1]

import ipdb; ipdb.set_trace()
# compute the Normalised Root Mean-Squared Error (NRMSE) between the two
# images
score = compare_nrmse(thresA, thresB)

# Compare the current image with the image from 5 layers ago
# This is used to check for filament runout or huge deviance
deviance = 1.0
scr_diff = 0.0
dev_diff = 0.0
if curr > 5:
    trd_file = fst_file[:-10] + str(curr - 5).rjust(6, '0') + '.jpg'
    grayC = cv2.imread(trd_file, 0)
    diffC = cv2.absdiff(grayC, grayBG)
    thresC = cv2.threshold(diffC, threshold, 255, cv2.THRESH_BINARY)[1]
    deviance = compare_nrmse(thresA, thresC)
    logfile = dirname(fst_file) + '/output.log'

    # Calculate difference compared with previous layer score and deviance
    with open(logfile, 'r') as log:
        data = log.readlines()
    prev_layer = data[-1]
    layer, scr, dev, s_diff, d_diff = prev_layer.split(" ")
    scr_diff = abs(score-float(scr))
    dev_diff = abs(deviance-float(dev))

print("{} {} {} {} {}".format(curr, score, deviance, scr_diff, dev_diff))
stderr.write("Image: {:d}\t Score: {}\t Deviance: {}\tDiffs: {}/{}\n".format(
    curr, score, deviance, scr_diff, dev_diff
))
