# Filename: NewMirror.py
# requirements
# requests, feedparser, traceback, Pillow

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
from Crypto import Crypto, CryptoPrice
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from PIL import Image, ImageTk
from contextlib import contextmanager

### Setup #####################################################################

os.putenv('SDL_FBDEV', '/dev/fb1')

# Setup the camera
'''camera = PiCamera()
camera.resolution = ( 320, 240 )
camera.framerate = 40
rawCapture = PiRGBArray( camera, size=( 320, 240) )

# Load the cascade files for detecting faces and phones
face_cascade = cv2.CascadeClassifier( '/home/pi/Downloads/opencv-3.3.0/data/lbpcascades/lbpcascade_frontalface.xml' )
phone_cascade = cv2.CascadeClassifier( 'cascade.xml' )

t_start = time.time()
fps = 0'''



LOCALE_LOCK = threading.Lock()
calendar_cuttoff = datetime.datetime.now()
current_date = time.gmtime()
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

print(str(calendar_cuttoff))
#2019-04-01T10:05:00+01:00

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
         # weather
        self.weather = Weather(self.topFrame)
        self.weather.place(x=0, y=5, anchor=NW, width=700, height=400)
        # Date
        self.date = Date(self.topFrame)
        self.date.place(x=1015, y=10, anchor=NE, width=350, height=90)
        # Day
        self.day = Day(self.topFrame)
        self.day.place(x=860, y=10, anchor=NE, width=300, height=90)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.place(x=940, y=60, anchor=NE, width=250, height=90)
        #Seconds
        self.sec = Sec(self.topFrame)
        self.sec.place(x=1015, y=60, anchor=NE, width=80, height=85)
        # news
        self.news = News(self.bottomFrame)
        self.news.pack(side=LEFT, anchor=S, padx=0, pady=10)
        # Facial rec
        #self.FacialRecognition = News(self.bottomFrame)
        #self.FacialRecognition.pack(side=LEFT, anchor=N, padx=100, pady=60)
        # calender
        self.calender = Calendar(self.topFrame)
        self.calender.place(x=1015, y=150, width=250, anchor=NE)
        # calender Time
        self.calenderTime = CalendarTime(self.topFrame)
        self.calenderTime.place(x=850, y=172, width=250, anchor=NE)
        #Traffic
        self.traffic = Traffic(self.topFrame)
        #Launch
        self.launch = Launch(self.topFrame)
        #crypto name
        self.crypto = Crypto(self.topFrame)
        self.crypto.pack(side=TOP, anchor=NE)
        #Crypto Time
        self.cryptoPrice = CryptoPrice(self.topFrame)
        self.cryptoPrice.pack(side=TOP, anchor=NE)
        #camera
        s = FacialRec()
        
        
        
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    #root =tk.Tk()
    #frame = NewsHeadline(Frame)
    #frame.pack(fill="both", expand=True)
    w = FullscreenWindow()
    w.tk.mainloop()
   
    '''# a little setup to demonstrate...
    stext = st.ScrolledText(bg='white', height=10)
    # kick off our callback
    stext.after(1000, lambda: scroll_textbox(stext))
    # shove a large amount of text in there
    stext.insert(const.END, get_headlines(self))
    stext.pack(fill=const.BOTH, side=const.LEFT, expand=True)
    stext.focus_set()
    stext.mainloop()'''