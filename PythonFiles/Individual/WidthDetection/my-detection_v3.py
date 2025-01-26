#!/usr/bin/python3
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import jetson.inference
import jetson.utils
import argparse
import sys
from collections import Counter
import time
import struct
import numpy as np

def load_model():


    net = jetson.inference.detectNet('ssd-mobilenet-v2',argv=['--model=models/flowers/ssd-mobilenet.onnx','--labels=models/flowers/labels.txt','--input-blob=input_0','--output-cvg=scores','--output-bbox=boxes'],threshold=0.5)
    return net


def run_model(net):
    camera = jetson.utils.videoSource("/dev/video0")      # '/dev/video0' for V4L2
    display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
    class_name = []
    width_object =[]
    print("with out appens",class_name)
    count = 0
    while display.IsStreaming() and count <= 200:
        img = camera.Capture()
        detections = net.Detect(img)
        
        for detection in detections:
            width=(detection.Width)
            width_object.append(width)
            class_names = net.GetClassDesc(detection.ClassID)
            print("inside for loop",class_names)
            class_name.append(class_names)
        print("appens",class_name)
        print("width_object:",width_object)
        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
        count = count+1
        print("count",count)
    return class_name,width_object

def calibrate_width(net, width_pot_1, width_pot_2, distance_pot):
    print(f"Keep the flower pot_1 at distance of {distance_pot} cemtimeters (100mm) and wait for 15 sec...")
    time.sleep(5)
    detected_class,width = run_model(net)
    sum_width_1 = np.sum(width)
    avg_width_1 = sum_width_1/len(width)
    print(f"average pixels occupaied by pot_1 at {distance_pot} cemtimeters:",avg_width_1)
    print(f"Keep the flower pot_2 at distance of {distance_pot} cemtimeters (200mm) and wait for 15 sec...")
    time.sleep(5)
    detected_class,width = run_model(net)
    sum_width_2 = np.sum(width)
    avg_width_2 = sum_width_2/len(width)
    print(f"average pixels occupaied by pot_2 at {distance_pot} cemtimeters:",avg_width_2)
    ideal_pot1_width = width_pot_1
    noof_pixels_1 = avg_width_1/ideal_pot1_width
    print(f"no.of pixels occupaied per 1mm for pot_1 at {distance_pot}cm distance is:",noof_pixels_1)
    ideal_pot2_width = width_pot_2
    noof_pixels_2 = avg_width_2/ideal_pot2_width
    print(f"no.of pixels occupaied per 1mm for pot_2 {distance_pot}cm distance is:",noof_pixels_2)
    diff_pixels = noof_pixels_1 - noof_pixels_2
    print("error between two tests",diff_pixels )
    avg_pixels_mm = (noof_pixels_1 + noof_pixels_2)/2
    print("average pixels occupaied per 1mm is:",avg_pixels_mm)
    return avg_pixels_mm
    

net = load_model()
avg_pixels = calibrate_width(net, 80, 80, 10)
time.sleep(1)

detected_class,width = run_model(net)
width_real = ((np.sum(width))/len(width))
print("width_real",width_real)
width_flower_pot = width_real/avg_pixels
print(f"width of the flower pot: {width_flower_pot}mm")
#while True:
 #   
  #  detected_class,width = run_model(net)
  #  print("main function", detected_class)
  #  print("no.of Distint classes detected:",Counter(detected_class).keys())
  #  print("Count of Distint Classes detected:",Counter(detected_class).values())
  #  
  #  print(np.sum(width))
  #  print("reg width of object")
  #  print(np.sum(width)/len(width))
   # for x in len(width):
    #    sum_width += width[x]
    #print(sum_width)
   # time.sleep(20)

    
     

