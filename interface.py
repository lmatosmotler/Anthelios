#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 00:23:58 2022

@author: lucasmolter
"""

import PySimpleGUI as sg
import sys
import os.path
from ticker_data import *
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
import pandas as pd
import scipy


class InputUser:
    def __inti__(self,stock = None,signal = None,ImageName = None,strike=None, model = None,image = None):
        self.stk = stock
        self.signal = signal
        self.ImageName = ImageName
        self.strike = strike
        self.model = model
        self.fig = image
        
    def clear_objet(self):
        self.stk = None
        self.signal = None
        self.ImageName = None
        self.strike = None
        self.model = None
        self.fig = None
        
    def validate(self,date_text):
        print(date_text)
        try:
            datetime.datetime.strptime(date_text, '%m-%d-%y')
        except ValueError:
            layout2 = [
                [sg.Text('Wrong date, please try again')]
                [sg.Ok()]
            ]
            window = sg.Window('Anthelios', layout2)
            _ = window.read()
            window.close()
            raise ValueError("Incorrect date")
    
    def creat_input(self):
        sg.theme('DarkTanBlue')
        
        layout = [
            [sg.Text('Enter security ticker, date, lemght of period (in days) and frequency (d, w or m)')],
            [sg.Text('Ticker', size =(15, 1)), sg.InputText()],
            [sg.Text('Day', size =(15, 1)), sg.InputText()],
            [sg.Text('Month', size =(15, 1)), sg.InputText()],
            [sg.Text('Year', size =(15, 1)), sg.InputText()],
            #[sg.Text('Period (in days)', size =(15, 1)), sg.InputText()],
            [sg.Text('Frequency (d/w/m)', size =(15, 1)), sg.InputText()],
            [sg.Submit(), sg.Cancel()]
        ]
        
        window = sg.Window('Anthelios', layout)
        event, values = window.read()
        window.close()
        data = ""
        if (int(values[2])<1 or int(values[2])>12):
            layout2 = [
                [sg.Text('Wrong month, it must be something between 1 and 12')],
                [sg.Ok()],
                [sg.Button("Abort")]
            ]
            window = sg.Window('Anthelios', layout2)
            event, x = window.read()
            window.close()
            if event in (None,"Abort"):
                sys.exit()
            self.clear_objet()
            return self.creat_input()
        if (int(values[1])<1 or int(values[1])>31):
            layout2 = [
                [sg.Text('Wrong day, it must be something between 1 and 31')],
                [sg.Ok()],
                [sg.Button("Abort")]
            ]
            window = sg.Window('Anthelios', layout2)
            event, x = window.read()
            window.close()
            if event in (None,"Abort"):
                sys.exit()
            self.clear_objet()
            return self.creat_input()
        if (int(values[3])<2000 or int(values[2])>2022):
            layout2 = [
                [sg.Text('Wrong year, it must be something between 2000 and 2022 and it cannot be a day in the future')],
                [sg.Ok()],
                [sg.Button("Abort")]
            ]
            window = sg.Window('Anthelios', layout2)
            event, x = window.read()
            window.close()
            if event in (None,"Abort"):
                sys.exit()
            self.clear_objet()
            return self.creat_input()
        data+=values[2]+"-"+values[1]+"-"+values[3]
        
        
        nome_ticker = values[0]
        frequencia = values[4]
        
        if frequencia == "d":
            frequencia = "1d"
        elif frequencia == "m":
            frequencia = "1mo"
        elif frequencia == "w":
            frequencia = "1wk"
        else:
            layout2 = [
                [sg.Text('Wrong frequency, it must be d, m or w')],
                [sg.Ok()],
                [sg.Button("Abort")]
            ]
            window = sg.Window('Anthelios', layout2)
            event, x = window.read()
            window.close()
            if event in (None,"Abort"):
                sys.exit()
            self.clear_objet()
            return self.creat_input()
        
        self.stk = stock(nome_ticker,data,date.today().strftime("%m-%d-%Y"),frequencia)
        self.ImageName = self.stk.sec_name
        got_data= self.stk.security_data_yahoo()
        
        if not got_data:
            layout2 = [
                [sg.Text('Problem with the inputs, probably ticker name, please try again.')],
                [sg.Ok()],
                [sg.Button("Abort")]
            ]
            window = sg.Window('Anthelios', layout2)
            event, x = window.read()
            window.close()
            if event in (None,"Abort"):
                sys.exit()
            self.clear_objet()
            return self.creat_input()
        self.stk.show_stock()
        return
    
    def show_graph(self,flag = False):
        if self.stk is None:
            return
        self.stk.chart_creator(True)
        if flag:
            layout = [
    
                [sg.Image(self.stk.fig_name)],
                [sg.Button("Abort")],
                [sg.Button("Continue")]
    
             ]
            
            window = sg.Window('Anthelios', layout)
            event,x = window.read()
            window.close()
            if event in (None,"Abort"):
                sys.exit()
        return
        
    def carrega_modelo(self):
        self.model = load_model('/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/model/modelNew.h5')
        
    def load_image_ds_format(self):
        # ds_test = tf.keras.preprocessing.image_dataset_from_directory(
        #         '/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/user_image',
        #         labels='inferred',
        #         label_mode = "int",
        #         class_names=["BUY","SELL"],
        #         color_mode = "grayscale",
        #         batch_size = 128,
        #         shuffle = False,
        #         seed = 265,
        #         validation_split = 0.99,
        #         subset="validation",
                
        #     )
        # self.fig = ds_test
        
        img = tf.keras.preprocessing.image.load_img(
            '/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/user_image/BUY/user.png',
            grayscale=True,
            color_mode='grayscale',
            target_size=(256,256,1),
            interpolation='nearest',
            keep_aspect_ratio=False
            )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        self.fig = img_array
        
        return
        
    def create_signal(self):
        # tem que fazer aqui a estimativa do modelo, baseado nos dados
        # vector = self.model.predict(self.fig)
        # print("pred: ",vector)
        # vector = np.array(vector)
        # pos = np.argmax(vector)
        # print("pos de max: ", pos)
        # if pos == 0:
        #     self.signal = "BUY"
        # else:
        #     self.signal = "SELL"
        
        vector = self.model.predict(self.fig)
        vector = np.array(vector)
        vector = np.array(scipy.special.softmax(vector))
        pos = np.argmax(vector)
        if pos == 0:
            self.signal = "BUY"
        else:
            self.signal = "SELL"        
        return
    
    
    
    def calc_strike(self):
      
        delta = datetime.strptime(self.stk.data_venda,"%m-%d-%Y")-datetime.strptime(self.stk.data_compra,"%m-%d-%Y")
        strike = datetime.strptime(self.stk.data_venda,"%m-%d-%Y") + timedelta(hours=delta.days*24)/2
        while strike.weekday()>4:
            strike = strike + timedelta(hours=24)
        self.strike=strike
        return
    
    def cria_imagem(self):
        self.show_graph()
        return
        
    def write_file_atharv(self):
        df = pd.DataFrame(columns=['Name', 'BUY_Date','Target_Date','Signal'])
        df = df.append({'Name': self.stk.sec_name,'BUY_Date': date.today(),'Target_Date': self.strike,'Signal': self.signal}, ignore_index=True)
        path = "/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/API"
        df.to_csv("/Users/lucasmolter/Documents/Cornell/Courses/Projectz/ProjectZ/API/"+self.stk.sec_name+"_"+self.strike.strftime("%m-%d-%Y")+".csv")
        return
    
    def show_result(self):
        if self.signal == "BUY":
            sg.theme('DarkGreen7')
            layout_buy = [
                [sg.Text('Security Name:', size =(20, 1)),sg.Text(self.stk.sec_name)],
                [sg.Text('The signal is:', size =(20, 1)),sg.Text('BUY')],
                [sg.Text('Strike Date:', size =(20, 1)),sg.Text(self.strike.strftime("%m/%d/%Y"))],
                [sg.Image(self.stk.fig_name)],
                [sg.Button("Exit")],
                [sg.Button("Save")],
                [sg.Button("New Analysis")]
    
             ]
            window = sg.Window('Anthelios', layout_buy)
        elif self.signal =="SELL":
            sg.theme('DarkRed2')
            layout_sell = [
                [sg.Text('Security Name:', size =(20, 1)),sg.Text(self.stk.sec_name)],
                [sg.Text('The signal is:', size =(20, 1)),sg.Text('SELL')],
                [sg.Text('Strike Date:', size =(20, 1)),sg.Text(self.strike.strftime("%m/%d/%Y"))],
                [sg.Image(self.stk.fig_name)],
                [sg.Button("Exit")],
                [sg.Button("Save")],
                [sg.Button("New Analysis")]
    
             ]
            window = sg.Window('Anthelios', layout_sell)
        else:
            return False
        event, x = window.read()
        window.close()
        if event in ("Save"):
            self.write_file_atharv()
            layout = [
    
                [sg.Text("Data Saved in the standard file!")],
                [sg.Button("Exit")],
                [sg.Button("New Analysis")]
    
             ]
            window = sg.Window('Anthelios', layout)
            event, x = window.read()
            window.close()
        if event in (None,"Exit"):
            sys.exit()
        if event in ("New Analysis"):
            self.clear_objet()
            return True
        return False
    

def main():
    #Cria interface
    test = InputUser()
    batch_size = 128
    catcher = True
    while catcher:
        #Chamar o usuario para ele colocar as informacoes que ele quer e puxar os dados da API
        test.creat_input()
        #Criar o grafico
        test.stk.chart_creator(True)
        #Carregar imagem no formato correto
        test.load_image_ds_format()
        #carregar modelo da memoria para mandar como parametro na proxima linha
        test.carrega_modelo()
        test.model.summary()
        #Enviar o modelo para criar o sinal
        test.create_signal()
        #Tem que transformar os dados em grafico para colocar na memoria
        test.cria_imagem()
        #Tem que criar a data de strike
        test.calc_strike()
        #Mostrar resultado para o usuario
        catcher = test.show_result()
    
    # reconstruir o modelo com o bathsize fixado
    
    
    
    
    





