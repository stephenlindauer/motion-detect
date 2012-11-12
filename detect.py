#!/usr/bin/env python

import Image, ImageDraw
import math
from subprocess import call
import time
import datetime
import os
import cv

REQUIRED_DETECTION=400

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

frames = []
recording = False
inactive_frames = 0
video_number = 0

capture = cv.CaptureFromCAM(0)

last_frame = cv.QueryFrame(capture)


while True:

    key = cv.WaitKey(10)
    if key == 113:
        break
        
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
    
    BAR_WIDTH = 400
    color = (0,255,0)    
    percent = 1.0*diff_count/REQUIRED_DETECTION
    if percent >= .6:
        color = (0,255,255)
    if percent >= 1:
        percent=1
        color = (0,0,255)
        print 'Motion captured'
        
        
        
    cv.Rectangle(display_frame, (frame.width/2-BAR_WIDTH/2, 690), (frame.width/2+BAR_WIDTH/2, 710), (0,0,0), -1)
    cv.Rectangle(display_frame, (frame.width/2-BAR_WIDTH/2, 690), (frame.width/2+BAR_WIDTH/2, 710), color)

    cv.Rectangle(display_frame, (frame.width/2-BAR_WIDTH/2, 690), (int(frame.width/2-BAR_WIDTH/2+BAR_WIDTH*percent), 710), color, -1)
    
    cv.ShowImage("Window", display_frame)

    last_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
    cv.Copy(frame, last_frame)
    
    if percent >= 1:
        
        if not recording:
            recording = True
            video_number += 1
            writer = cv.CreateVideoWriter("out-%s.avi" % (video_number), cv.CV_FOURCC('M', 'J', 'P', 'G'), 5, cv.GetSize(frame), True)

        if recording:
            cv.WriteFrame(writer, display_frame)
            
    
    else:
        if recording:
            inactive_frames += 1
            frames.append(frame)
            if inactive_frames > 20:
                recording = False
                inactive_frames = 0                
                print 'Save video'
                del writer



        
    
#     k=cv.WaitKey(500)
#     print k






