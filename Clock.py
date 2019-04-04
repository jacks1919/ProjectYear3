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

LOCALE_LOCK = threading.Lock()
ui_locale = 'en_GB.utf8' # e.g. 'fr_FR' fro French, '' as default
current_date = time.gmtime()
ui_locale = 'en_GB.utf8' # e.g. 'fr_FR' fro French, '' as default
time_format = 24 # 12 or 24
xlarge_text_size = 90
large_text_size = 60
medium_text_size = 30
small_text_size = 20
extra_small_text_size = 13
sec_text_size = 40

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Abel', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        self.tick()
        
        
    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format
                sec2 = time.strftime(':%S') #hour in 24h format

            #day_of_week2 = time.strftime('%A')
            #date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
                
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)