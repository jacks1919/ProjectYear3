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


class Traffic(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
                
        self.duration = ''
        self.durationTotal = ''
        
        self.durationLbl =  Label(self.durationTotal, font=('Abel', small_text_size), fg="white", bg="black")
        self.durationLbl.place(x=250, y=1000)
        self.get_events()
        
    def get_events(self):
        try:
            traffic_URL = ("http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=rahoon%2Cwa&wp.1=moycullen%2Cwa&avoid=minimizeTolls&key=ApOFJsj0FMkU0AdBf9YVE1GXVWt2BR5p1MBMTT7jJqhPTigcVzCGDXMZzmzl26on")
            r = requests.get(traffic_URL)
            traffic_obj = json.loads(r.text)
            
            duration = traffic_obj['resourceSets'][0]['resources'][0]['travelDuration']
            durationtraffic = traffic_obj['resourceSets'][0]['resources'][0]['travelDurationTraffic']
            #durationdistance = traffic_obj['resourceSets'][0]['resources'][0]['travelDistance']
            dTotal = ((duration + durationtraffic) / 60)
            durationTotal = 'Your commute will take {} minutes today'.format(dTotal)
            #print(duration)
            #print(durationtraffic)
            #print(durationTotal)
            #print(durationdistance)
            
            if self.durationLbl != durationTotal:
                    self.duration = durationTotal
                    self.durationLbl.config(text=durationTotal)

        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get traffic." , e)

        self.after(600000, self.get_events)