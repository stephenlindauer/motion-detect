#!/usr/bin/env python

import Image, ImageDraw
import math
from subprocess import call
import time
import datetime
import os
import cv


def my_range(start, end, step):
    while start<=end:
        yield start
        start += step

def pix_change1(p1, p2, x, y):
    r = 0 #p2[x,y][0]
    g = 120 #255
    b = 0
    return (r, g, b)

def pix_change2(p1, p2, x, y):
    r = 0
    g = 0
    b = 0
    return (r, g, b)


capture = cv.CaptureFromCAM(0)

last_frame = cv.QueryFrame(capture)


while True:

    cv.WaitKey(1)
    frame = cv.QueryFrame(capture)    
    
    display_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
    cv.Copy(frame, display_frame)

    
    pixels1 = last_frame
    pixels2 = display_frame
    
    
    thresh = 50
    diff_count = 0
    
    for y in my_range(0,frame.width-1, 4):
        for x in my_range(0, frame.height-1, 4):

            val1 = pixels1[x,y][0] + pixels1[x,y][1] + pixels1[x,y][2]
            val2 = pixels2[x,y][0] + pixels2[x,y][1] + pixels2[x,y][2]

            if abs(val1-val2) > thresh:
                diff_count += 1

                pixels2[x,y] = pix_change1(pixels1, pixels2, x, y)
                if (x >= 2 and y >= 2):
                    pixels2[x-2 ,y-2] = pix_change1(pixels1, pixels2, x+2, y+2)
                    pixels2[x ,y-2] = pix_change2(pixels1, pixels2, x, y+2)
                    pixels2[x-2 ,y] = pix_change2(pixels1, pixels2, x+2, y)
                
    
    print 'pixel difference: ', diff_count
    if diff_count >= 1000:
        print 'Motion captured'
#         output_file = "%s/Desktop/motion-detect-captures/diff%s.jpg" % (os.environ['HOME'], datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S'))
#         i2.save(output_file)
    else:
        print 'No motion detected'

    cv.ShowImage("Window", display_frame)

    last_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
    cv.Copy(frame, last_frame)
    
#     k=cv.WaitKey(500)
#     print k