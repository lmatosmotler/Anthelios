#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 19:43:33 2022

@author: lucasmolter
"""

import PySimpleGUI as sg
import os.path
import numpy as np
# from modelTensor import *
import datetime
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.models import save_model
from tensorflow.keras.models import load_model
from datetime import datetime
from pathlib import Path
import pandas as pd

#loading model
model = load_model('/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/model/model.h5')

df = pd.DataFrame(columns=['Name', 'BUY_Date','Target_Date','Signal'])


basepath = Path('/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/backtest/BUY')
files_in_basepath = basepath.iterdir()
for item in files_in_basepath:
    if item.is_file():
        x = item.name.split("_")
        path = '/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/backtest/BUY/'+item.name
        img = tf.keras.preprocessing.image.load_img(
            path,
            grayscale=True,
            color_mode='grayscale',
            target_size=(256,256,1),
            interpolation='nearest',
            keep_aspect_ratio=False
            )

        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        vector = model.predict(img_array)
        vector = tf.keras.layers.Softmax(vector)
        vector = np.array(vector)
        pos = np.argmax(vector)
        if pos == 0:
            signal = "BUY"
        else:
            signal = "SELL"
        df = df.append({'Name': x[0],'BUY_Date': x[1],'Target_Date': x[2],'Signal': signal}, ignore_index=True)
print(df)

df.to_csv('/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/backtestSPY.csv')

        

path = '/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/backtest/BUY/SPY_01-01-03_03-11-03_1d_Nov-03-2022.png'
img = tf.keras.preprocessing.image.load_img(
    path,
    grayscale=True,
    color_mode='grayscale',
    target_size=(256,256,1),
    interpolation='nearest',
    keep_aspect_ratio=False
    )

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])


#loading images
ds_test = tf.keras.preprocessing.image_dataset_from_directory(
        '/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/backtest',
        labels='inferred',
        label_mode = "int",
        class_names=["BUY","SELL"],
        color_mode = "grayscale",
        batch_size = 128,
        shuffle = False,
        seed = 265,
        validation_split = 0.999,
        subset="validation",
        
    )

#making predictions
for i in ds_test:
    vector = model.predict(i)
    vector = np.array(vector)
    pos = np.argmax(vector)
    if pos == 0:
        signal = "BUY"
    else:
        signal = "SELL"
    
    
