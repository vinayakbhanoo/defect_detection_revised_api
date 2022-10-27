"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import math
import os
from PIL import Image
from flask_cors import CORS
import numpy as np
 
from base64 import b64encode

import base64
import torch
import logging
#import azure.functions as func
import tempfile
from os import listdir
import cv2
import pandas as pd

import openpyxl
from flask import Flask, render_template, request, redirect,jsonify,send_file
from subprocess import STDOUT, check_call , call
#from w3lib.url import parse_data_uri

import os

# check_call(['apt-get', 'update'], stdout=open(os.devnull,'wb'), stderr=STDOUT)
# check_call(['apt-get', 'install', '-y', 'libgl1'], stdout=open(os.devnull,'wb'), stderr=STDOUT)
# check_call(['apt-get', 'install', '-y', 'libglib2.0-0'], stdout=open(os.devnull,'wb'), stderr=STDOUT)

# check_call([ 'apt-get', 'update'], stdout=open(os.devnull,'wb'), stderr=STDOUT)
# check_call([ 'apt-get', 'install','-y','software-properties-common'], stdout=open(os.devnull,'wb'), stderr=STDOUT)
# check_call( ['add-apt-repository' ,'-y', 'ppa:libreoffice/ppa'], stdout=open(os.devnull,'wb'), stderr=STDOUT)

# check_call([ 'apt-get', 'update'], stdout=open(os.devnull,'wb'), stderr=STDOUT)

# check_call([ 'apt-get' ,'install' ,'-y','libreoffice' ,'libreoffice-style-breeze'], stdout=open(os.devnull,'wb'), stderr=STDOUT)
# check_call([ 'apt-get', 'update','-y'], stdout=open(os.devnull,'wb'), stderr=STDOUT)
# check_call([ 'apt-get', 'install' ,'-y','abiword'], stdout=open(os.devnull,'wb'), stderr=STDOUT)


github='ultralytics/yolov5'
torch.hub.list(github, trust_repo=True)
model = torch.hub.load("ultralytics/yolov5", "yolov5s")
  
model.classes=[0]
model.conf=.5
model.line_thickness=1
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
cap = cv2.VideoCapture("region.mp4")


while(cap.isOpened()):
    ret, frame = cap.read()
    height,width = frame.shape[:2] 
    # img = Image.open(io.BytesIO(frame))
    
    
    results = model(frame)
    img = np.squeeze(results.render())



    #print("RESULT=======",results)
    # file_object = io.BytesIO()

    # data = Image.fromarray(img)
    # data.save(file_object, 'JPEG')



    res_tensor=results.xyxy[0]  # im1 predictions (tensor)
    

    #print(results.pandas().xyxy[0] ) # im1 predictions (pandas)
    #print("y ",res_tensor[0][1])
    #print("c ",int(res_tensor[0][5]))
    #print("tensor len",len(res_tensor))

    rings=[]
    for i in range(0,len(res_tensor)):
        
        print("percent=====",res_tensor[i][1]/height)
  

        if res_tensor[i][1]/height >.35:
            print("Alert")
            cv2.putText(img,'Alert:',(700,470), font, 1,(0,255,0),2,cv2.LINE_4)
    


    # Start coordinate, here (100, 50)
    # represents the top left corner of rectangle
    start_point = (500, 500)
    
    # Ending coordinate, here (125, 80)
    # represents the bottom right corner of rectangle
    end_point = (1000, 500) 
    
    # Black color in BGR
    color = (0,0,255)
    
    # Line thickness of -1 px
    # Thickness of -1 will fill the entire shape
    thickness =2
    
    # Using cv2.rectangle() method
    # Draw a rectangle of black color of thickness -1 px
    image = cv2.line(img, (500, 500), (1000, 500), color, thickness) #horiz
    image = cv2.line(img, (500,500), (500,1000), color, thickness)#vert
    image = cv2.line(img, (1000,500), (1000,1000), color, thickness) #vert

    image = cv2.line(img, (500, 550), (1000, 550), color, thickness)
    image = cv2.line(img, (500, 600), (1000, 600), color, thickness)
    image = cv2.line(img, (500, 700), (1000, 700), color, thickness)
    image = cv2.line(img, (500, 800), (1000, 800), color, thickness)
    image = cv2.line(img, (500, 900), (1000, 900), color, thickness)
    image = cv2.line(img, (500, 650), (1000, 650), color, thickness)
    image = cv2.line(img, (500, 750), (1000, 750), color, thickness)
    image = cv2.line(img, (500, 850), (1000, 850), color, thickness)
    image = cv2.line(img, (500, 950), (1000, 950), color, thickness)
    # Displaying the image 

    cv2.imshow('frame',image)       
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
              