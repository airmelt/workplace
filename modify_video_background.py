#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: modify or replace video background
@file_name: modify_video_background.py
@project: workplace
@version: 1.0
@date: 2023/4/12 21:47
@author: air
"""

import os
import cv2
import numpy as np
import mediapipe as mp
import subprocess

# use your own input & output
images = 'images'
videos = 'videos'
image = 'bg_image.png'
input_video = 'input.MP4'
output_video = 'output0.mp4'

# background image
bg_image = cv2.imread(os.path.join(images, image))

# create media pipe
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# input & output video
cap = cv2.VideoCapture(os.path.join(videos, input_video))
out = cv2.VideoWriter(os.path.join(videos, output_video), cv2.VideoWriter_fourcc(*'mp4v'), 30.0, (720, 1280))

# process
while cap.isOpened():
    result, frame = cap.read()
    # break when cap is finish
    if not result:
        break
        
    height, width, channel = frame.shape
    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # get the result
    results = selfie_segmentation.process(RGB)

    # extract segmented mask
    mask = results.segmentation_mask

    # it returns true or false where the condition applies in the mask
    condition = np.stack(
        (results.segmentation_mask,) * 3, axis=-1) > 0.5

    # resize the background image to the same size of the original frame
    bg_image = cv2.resize(bg_image, (width, height))

    # combine frame and background image using the condition
    output_image = np.where(condition, frame, bg_image)
    
    # show picture
    # cv2.imshow("mask", mask)
    # cv2.imshow("Frame", frame)
    # cv2.imshow("Output", output_image)
    out.write(output_image)

# release resources
cap.release()
out.release()
cv2.destroyAllWindows()

# concat audio
subprocess.run('ffmpeg -i ./videos/7.mp4 -f mp3 -ab 192000 -vn ./videos/sound.mp3', shell=True)
subprocess.run('ffmpeg -i ./videos/output0.mp4 -i ./videos/sound.mp3 -c copy -map 0:v:0 -map 1:a:0 ./videos/output.mp4',
               shell=True)
