# -*- coding: utf-8 -*-

# !/usr/bin/env python

"""Face recognition module using Tensorflow and Keras.

In this module we train a convolutional neural network
to be able to predict or recognize faces.
"""

import sys
import os

__author__ = "Beck"

import numpy as np

import numpy as np
from PIL import Image
from pillow_heif import register_heif_opener

# Config
# from mtcnn_detector import MTCnnDetector
# from vggModelFinal import VggModel

from facial_recognition_based__attendance_system_app.FacialRecognition.mtcnn_detector import MTCnnDetector
from facial_recognition_based__attendance_system_app.FacialRecognition.vggModelFinal import VggModel

# import constant


class MainClass:
    @staticmethod
    def make_predication(img_path): #, model_weight_url):

       # answer = MTCnnDetector.control_all(img_path, False, False)
       #  return MTCnnDetector.control_all(img_path, model_weight_url, False, False)
        return MTCnnDetector.control_all(img_path, False, False)

    @staticmethod
    def train_model(epoch=1, batch=4):
        vgg = VggModel()
        vgg.train(epoch, batch)

    @staticmethod
    def get_number_of_class_samples():
        vgg = VggModel(flag=False)
        vgg.train(flag=False)
        classes, samples = vgg.get_number_class_samples()
        return classes, samples



# MainClass.train_model(50, 8)

 

# # --- 2. IMAGE PATH (JPG) ---
# image_path = "C:/Users/becka/Desktop/FRAS/media/testing_data/Bekan_Shiferaw_UGR_61569_14/IMG_5043.jpg"

# print(f"Testing Image: {image_path}")

# try:
#     # 3. Load JPG and convert to RGB array
#     img = Image.open(image_path).convert('RGB')
#     image_array = np.array(img)

#     # 4. Run Prediction
#     result = MainClass.make_predication(image_array) 
    
#     print("--------------------------------")
#     print("Predicted Result: " + result)
#     print("--------------------------------")

# except FileNotFoundError:
#     print(f"Error: The image file was not found at {image_path}")
# except Exception as e:
#     print(f"An error occurred: {e}")