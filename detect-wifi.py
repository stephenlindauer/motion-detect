#!/usr/bin/env python

import Image, ImageDraw
import math
from subprocess import call
import time
import datetime
import os
import cv
import sys

REQUIRED_DETECTION=80
THRESHOLD = 130
ALWAYS_SHOW_FRAME = False
RECORD = True
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
    g = 120
    b = 0
    return p2[x,y]

def show_frame(frame):
#     size = cv.GetSize(frame)
#     small = cv.CreateImage((size[0] / 4, size[1] / 4), frame.depth, frame.nChannels)
#     cv.Resize(frame, small)
    cv.ShowImage(WINDOW_NAME, frame)


frames = []
recording = False
inactive_frames = 0
video_number = 0

CAM_INDEX = 0
if len(sys.argv) > 1:
    CAM_INDEX = int(sys.argv[1])
#capture = cv.CaptureFromCAM(CAM_INDEX)
capture = cv.CaptureFromFile("http://192.168.10.195:81/videostream.asf?user=admin&pwd=sdlyr8")

WINDOW_NAME = "Window-%s" % CAM_INDEX

last_frame = cv.QueryFrame(capture)


while True:

    if recording:
        key = cv.WaitKey(10)
    else:
        key = cv.WaitKey(500)
    if key == 113:
        break
        
    frame = cv.QueryFrame(capture)    
    
    display_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
    cv.Copy(frame, display_frame)

    
    pixels1 = last_frame
    pixels2 = display_frame
    
    diff_count = 0
    
    for y in my_range(0,frame.width-1, 5):
        for x in my_range(0, frame.height-1, 5):
            red_diff = abs(pixels1[x,y][0] - pixels2[x,y][0])
            green_diff = abs(pixels1[x,y][0] - pixels2[x,y][0])
            blue_diff = abs(pixels1[x,y][0] - pixels2[x,y][0])
            
            if red_diff + blue_diff + green_diff > THRESHOLD:
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
        
        
        
    cv.Rectangle(display_frame, (frame.width/2-BAR_WIDTH/2, frame.height-30), (frame.width/2+BAR_WIDTH/2, frame.height-10), (0,0,0), -1)
    cv.Rectangle(display_frame, (frame.width/2-BAR_WIDTH/2, frame.height-30), (frame.width/2+BAR_WIDTH/2, frame.height-10), color)

    cv.Rectangle(display_frame, (frame.width/2-BAR_WIDTH/2, frame.height-30), (int(frame.width/2-BAR_WIDTH/2+BAR_WIDTH*percent), frame.height-10), color, -1)
    
    last_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
    cv.Copy(frame, last_frame)

    if percent >= 1:
        
        if not recording:
            recording = True
            video_number += 1
            if RECORD:
                writer = cv.CreateVideoWriter("wifi-out-%s.avi" % (video_number), cv.CV_FOURCC('M', 'J', 'P', 'G'), 5, cv.GetSize(frame), True)
            
            print cv.NamedWindow(WINDOW_NAME, flags=cv.CV_WINDOW_NORMAL)
            cv.MoveWindow(WINDOW_NAME, 2500, 20)

        show_frame(display_frame) 
  
        if RECORD and recording:
            cv.WriteFrame(writer, display_frame)
        
        inactive_frames = 0
    
    else:

        if recording:
            show_frame(display_frame)
            
            inactive_frames += 1
            if RECORD:
                cv.WriteFrame(writer, display_frame)
            
            if inactive_frames > 20:
                recording = False
                inactive_frames = 0
                if RECORD:                
                    print 'Save video'
                    del writer
                
                cv.DestroyWindow(WINDOW_NAME)
#                 cv.ResizeWindow(WINDOW_NAME, 200, 120)

    
#     k=cv.WaitKey(500)
#     print k






