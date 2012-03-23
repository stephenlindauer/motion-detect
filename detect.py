#!/usr/bin/env python

import Image, ImageDraw
import math
from subprocess import call
import time
import datetime
import os


def my_range(start, end, step):
    while start<=end:
        yield start
        start += step

def pix_change(p1, p2, x, y, delta):
	r = p2[x,y][0] + delta
	g = p2[x,y][1] + delta
	b = p2[x,y][2] + delta
	return (b, g, b)

file1 = "previous.jpg"
file2 = "current.jpg"

# if not os.path.isfile(file1):
call(["./imagesnap", '-d', 'Logitech Camera', '-q', file1])
time.sleep(3)

while True:
	print 'capturing current picture now'
	call(["./imagesnap", '-d', 'Logitech Camera', '-q', file2])
	
	
	i1 = Image.open(file1)
	i2 = Image.open(file2)
	
	pixels1 = i1.load()
	pixels2 = i2.load()
	
	
	
	thresh = 80
	diff_count = 0
	
	for x in my_range(0,i1.size[0]-1, 4):
		for y in my_range(0, i1.size[1]-1, 4):
	# 		print pixels1[x, y]
			val1 = pixels1[x,y][0] + pixels1[x,y][1] + pixels1[x,y][2]
			val2 = pixels2[x,y][0] + pixels2[x,y][1] + pixels2[x,y][2]
			
			if abs(val1-val2) > thresh:
				diff_count += 1
	# 			print val1, val2, abs(val1-val2)
	# 			print x, y
				pixels2[x,y] = pix_change(pixels1, pixels2, x, y, 100)
				if (x >= 2 and y >= 2):
					pixels2[x-2 ,y-2] = pix_change(pixels1, pixels2, x+2, y+2, -100)
				
	
	print 'pixel difference: ', diff_count
	if diff_count >= 1000:
		print 'Motion captured'
		output_file = "diff%s.jpg" % (datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S'))
		i2.save(output_file)
	else:
		print 'No motion detected'
	# 	call(["open", output_file])
	
	os.remove(file1)
	os.rename(file2, file1)
	
	print 'Next capture in 3...'
	time.sleep(1)
	print '2...'
	time.sleep(1)
	print '1...'
	time.sleep(1)
	

