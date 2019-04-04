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


calendar_cuttoff = datetime.datetime.now()

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


class CalendarTime(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
        self.calendarEvent1Time = ''
        self.calendarEvent2Time = ''
        self.calendarEvent3Time = ''
        
        self.calendarEvent1TimeLbl =  Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.calendarEvent1TimeLbl.pack(side=TOP, anchor=NE)
        
        self.calendarEvent2TimeLbl =  Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.calendarEvent2TimeLbl.pack(side=TOP, anchor=NE)
        
        self.calendarEvent3TimeLbl =  Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.calendarEvent3TimeLbl.pack(side=TOP, anchor=NE)
        self.get_events()
        
    def get_events(self):
        try:
            calendar_url = ("https://www.googleapis.com/calendar/v3/calendars/smartmirror157@gmail.com/events/?key=AIzaSyDD16yoES6q7LCUdAF0dlnOLSQnGUOcGJQ")
            r = requests.get(calendar_url)
            calendar_obj = json.loads(r.text)
            
            calendarEvent1Time2 = calendar_obj['items'][0]['start']['date']
            
            calendarEvent2Time2 = calendar_obj['items'][1]['start']['date']
           
            calendarEvent3Time2 = calendar_obj['items'][2]['start']['date']
            
            #print(calendarEvent1Time2)
            #print(calendarEvent2Time2)
            #print(calendarEvent3Time2)
            
            if self.calendarEvent1TimeLbl != calendarEvent1Time2:
                    self.calendarEvent1Time = calendarEvent1Time2
                    self.calendarEvent1TimeLbl.config(text=calendarEvent1Time2)

            
            if self.calendarEvent2TimeLbl != calendarEvent2Time2:
                    self.calendarEvent2Time = calendarEvent2Time2
                    self.calendarEvent2TimeLbl.config(text=calendarEvent2Time2)
                                                             
            
            if self.calendarEvent3TimeLbl != calendarEvent3Time2:
                    self.calendarEvent3Time = calendarEvent3Time2
                    self.calendarEvent3TimeLbl.config(text=calendarEvent3Time2)
            
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get calendar." , e)

        self.after(600000, self.get_events)