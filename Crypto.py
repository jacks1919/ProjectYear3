from Tkinter import *
#from Tkinter.scrolledtext import ScrolledText as st
#from tkinter import scrolledtext as st
#from tkinter import constants as const
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep


import time
import datetime
import cv2
import os
import pygame
import locale
import threading
import requests
import json  
import traceback
import feedparser
from sample import FacialRec
from Clock import Clock
from Sec import Sec
from Day import Day
from Date import Date
from Weather import Weather
from News import News, NewsHeadline
#from NewsHeadlines import NewsHeadline
from Calendar import Calendar
from CalendarTime import CalendarTime
from Traffic import Traffic
from Launch import Launch

from PIL import Image, ImageTk
from contextlib import contextmanager
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

### Setup #####################################################################








ui_locale = 'en_GB.utf8' # e.g. 'fr_FR' fro French, '' as default
time_format = 24 # 12 or 24
date_format = "%b %d" # check python doc for strftime() for options
news_country_code = 'uk'
weather_api_token = '52cb312030821b9d32409a1452c4fbec' # create account at https://darksky.net/dev/
weather_lang = 'en' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'si' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
latitude = '53.01' # Set this if IP location lookup does not work for you (must be a string)
longitude = '-9.0' # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 90
large_text_size = 60
medium_text_size = 30
small_text_size = 20
extra_small_text_size = 13
sec_text_size = 40



class Crypto(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
        self.coin1 = ''
        self.coin2 = ''
        self.coin3 = ''
        
        self.coin1Lbl = Label(self.coin1, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.coin1Lbl.place(x=1015, y=300, width=100, anchor=NE)
        
        self.coin2Lbl = Label(self.coin2, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.coin2Lbl.place(x=1015, y=325, width=100, anchor=NE)
        
        self.coin3Lbl = Label(self.coin3, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.coin3Lbl.place(x=1015, y=350, width=100, anchor=NE)
        
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
          'start': '1',
          'limit': '3',
          'convert': 'EUR',
        }
        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': '98320f56-b874-402b-85aa-459fe110d6cb',
        }

        session = Session()
        session.headers.update(headers)
        #self.get_events()
        
        '''try:
          response = session.get(url, params=parameters)
          data = json.loads(response.text)
          print(data)
        
        except (ConnectionError, Timeout, TooManyRedirects) as e:
          print(e)'''
        
        
    #def get_events(self):
        try:
            r = session.get(url, params=parameters)
            data = json.loads(r.text)
            
            coin11 = data['data'][0]['name']
            coin22 = data['data'][1]['name']
            coin33 = data['data'][2]['name']
        
            if self.coin1Lbl != coin11:
                    self.coin1 = coin11
                    self.coin1Lbl.config(text=coin11)
                    
            if self.coin2Lbl != coin22:
                    self.coin2 = coin22
                    self.coin2Lbl.config(text=coin22)
                    
            if self.coin3Lbl != coin33:
                    self.coin3 = coin33
                    self.coin3Lbl.config(text=coin33)
                    
            
            '''image = Image.open("assets/rocket.png")
            image = image.resize((50, 50), Image.ANTIALIAS)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)
            
            self.rocketLbl.config(image=photo)
            self.rocketLbl.image = photo'''
            
        except Exception as e:
                traceback.print_exc()
                print ("Error: %s. Cannot get crypto." , e)

        #self.after(600000, self.get_events)
        
class CryptoPrice(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
        self.coin1Price = ''
        self.coin2Price = ''
        self.coin3Price = ''
        
        self.coin1PriceLbl = Label(self.coin1Price, font=('Abel', extra_small_text_size), fg="white", bg="black", justify=RIGHT)
        self.coin1PriceLbl.place(x=920, y=300, width=250, anchor=NE)
        
        self.coin2PriceLbl = Label(self.coin2Price, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.coin2PriceLbl.place(x=920, y=325, width=250, anchor=NE)
        
        self.coin3PriceLbl = Label(self.coin3Price, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.coin3PriceLbl.place(x=920, y=350, width=250, anchor=NE)
        #self.get_events()
        
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
          'start': '1',
          'limit': '3',
          'convert': 'EUR',
        }
        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': '98320f56-b874-402b-85aa-459fe110d6cb',
        }

        session = Session()
        session.headers.update(headers)
        
    #def get_events(self):
        try:
            r = session.get(url, params=parameters)
            data = json.loads(r.text)
            
            coin11Price = data['data'][0]['quote']['EUR']['price']
            coin22Price = data['data'][1]['quote']['EUR']['price']
            coin33Price = data['data'][2]['quote']['EUR']['price']
            
            coin11Price = 'EUR {:.2f}'.format(coin11Price)
            coin22Price = 'EUR {:.2f}'.format(coin22Price)
            coin33Price = 'EUR {:.2f}'.format(coin33Price)
        
            if self.coin1PriceLbl != coin11Price:
                    self.coin1Price = coin11Price
                    self.coin1PriceLbl.config(text=coin11Price)
                    
            if self.coin2PriceLbl != coin22Price:
                    self.coin2Price = coin22Price
                    self.coin2PriceLbl.config(text=coin22Price)
                    
            if self.coin3PriceLbl != coin33Price:
                self.coin3Price = coin33Price
                self.coin3PriceLbl.config(text=coin33Price)
                    
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get crypto." , e)