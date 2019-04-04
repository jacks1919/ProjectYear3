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


class Calendar(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
        #image = Image.open("assets/Rain.gif")
        
        #frames = [PhotoImage(file=assets/news.gif, format="gif -index %i" %(i)) for i in range(100)]
        '''photo = ImageTk.PhotoImage(file = "/home/pi/Downloads/assets/Storm1.gif", format = "gif -index 2")
        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=RIGHT, anchor=N)'''
        
        #self.windLbl.config(image=photo)
        #self.windLbl.image = photo
        
        #self.title = 'Events for: ',
        self.subTitle = ''
        self.calendarEvent1 = ''
        self.calendarEvent2 = ''
        self.calendarEvent3 = ''
        self.calendarEvent1Time = ''
        self.calendarEvent2Time = ''
        self.calendarEvent3Time = ''
        
        self.subTitleLbl = Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.subTitleLbl.pack(side=TOP, anchor=NE)
   
        self.calendarEvent1Lbl = Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.calendarEvent1Lbl.pack(side=TOP, anchor=NE)
        
        self.calendarEvent2Lbl = Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.calendarEvent2Lbl.pack(side=TOP, anchor=NE)
        
        self.calendarEvent3Lbl = Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.calendarEvent3Lbl.pack(side=TOP, anchor=NE)
       
        self.get_events()
        
    
    def get_events(self):
        try:
            calendar_url = ("https://www.googleapis.com/calendar/v3/calendars/smartmirror157@gmail.com/events/?key=AIzaSyDD16yoES6q7LCUdAF0dlnOLSQnGUOcGJQ")
            r = requests.get(calendar_url)
            calendar_obj = json.loads(r.text)
            
            
            subTitle2 = calendar_obj['summary']
            #title = ('Events for: ', subTitle2)
            #print(title)
            calendarEvent11 = calendar_obj['items'][0]['summary']
            #calendarEvent1Time2 = calendar_obj['items'][0]['start']['dateTime']
            calendarEvent22 = calendar_obj['items'][1]['summary']
            #calendarEvent2Time2 = calendar_obj['items'][1]['start']['dateTime']
            calendarEvent33 = calendar_obj['items'][2]['summary']
            #calendarEvent3Time2 = calendar_obj['items'][2]['start']['dateTime']
            #print (subTitle2)
            #print (calendarEvent11)
            #print (calendarEvent22)
            #print (calendarEvent33)
            #print(calendarEvent1Time2)
            #print(calendarEvent2Time2)
            #print(calendarEvent3Time2)
            
            
            
            if self.subTitle != subTitle2:
                    self.subTitle = subTitle2
                    self.subTitleLbl.config(text=subTitle2)
                    
            if self.calendarEvent1 != calendarEvent11:
                    self.calendarEvent1 = calendarEvent11
                    self.calendarEvent1Lbl.config(text=calendarEvent11)
                    
            
                    
            if self.calendarEvent2 != calendarEvent22:
                    self.calendarEvent2 = calendarEvent22
                    self.calendarEvent2Lbl.config(text=calendarEvent22)
            
            
                                                             
            if self.calendarEvent3 != calendarEvent33:
                    self.calendarEvent3 = calendarEvent33
                    self.calendarEvent3Lbl.config(text=calendarEvent33)
            
            
                                                             
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get calendar." , e)

        self.after(600000, self.get_events)