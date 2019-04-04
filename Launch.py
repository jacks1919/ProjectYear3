from Tkinter import *
#from Tkinter.scrolledtext import ScrolledText as st
#from tkinter import scrolledtext as st
#from tkinter import constants as const
from picamera.array import PiRGBArray
from picamera import PiCamera

from time import sleep

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
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

from PIL import Image, ImageTk
from contextlib import contextmanager



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


class Launch(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
        self.launch = ''
        self.launchDate = ''
        
        self.rocketLbl = Label(self.launch, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.rocketLbl.place(x=0, y=300, anchor = NW)
        
        self.launchLbl =  Label(self.launch, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.launchLbl.place(x=60, y=300)
        
        self.launchDateLbl =  Label(self.launchDate, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.launchDateLbl.place(x=60, y=325)
        self.get_events()
        
        
            
    def get_events(self):
        try:
            
            launch_URL = ('https://launchlibrary.net/1.4/launch?launchid=12')
            r = requests.get(launch_URL)
            launch_obj = json.loads(r.text)
            
            launch2 = launch_obj['launches'][0]['name']
            launchDate2 = launch_obj['launches'][0]['net']
        
            if self.launchLbl != launch2:
                    self.launch = launch2
                    self.launchLbl.config(text=launch2)
                    
            if self.launchDateLbl != launchDate2:
                    self.launchDate = launchDate2
                    self.launchDateLbl.config(text=launchDate2)
            
            image = Image.open("assets/rocket.png")
            image = image.resize((50, 50), Image.ANTIALIAS)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)
            
            self.rocketLbl.config(image=photo)
            self.rocketLbl.image = photo
        
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get launch." , e)

        self.after(600000, self.get_events)