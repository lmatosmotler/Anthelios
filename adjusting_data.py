#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 11:33:44 2022

@author: lucasmolter
"""

from pathlib import Path
import shutil
import os
import pandas as pd
import numpy as np

#getting paths
src = '/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/dataset'
buy = '/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/datasetBUY'
sell = '/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/datasetSELL'
#getting and organizing the dataframe
df = pd.read_csv('/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/labels.csv')
df = df.drop(columns = 'Unnamed: 0',axis = 1)
df = df.drop([0,1])
#first part of the paths
first_part = '/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/dataset/'
#rewriting the dataframe
for i in df.index:
    df['Label'][i]=np.sign(int(float(df['Label'][i])))
print(df.head)
df.to_csv("/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/binLabels.csv")

#Moving images
images=os.listdir(src)

for fname in images:
    curr = first_part+fname
    label = df.loc[df['Fig_Name']==curr]['Label']
    label = label.to_string(index = False)
    if label == "1.0":
        shutil.copy2(os.path.join(src,curr), buy)
    elif label == "-1.0":
        shutil.copy2(os.path.join(src,curr), sell)

        

