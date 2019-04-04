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

class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'Todays Headlines                                                                           '
        self.newsLbl = Label(self, text=self.title, font=('Abel', small_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()
        
        
        
    def get_headlines(self):
        try:
            # remove all children
            for widget in self.headlinesContainer.winfo_children():
                widget.destroy()
            if news_country_code == None:
                headlines_url = "https://news.google.com/news?ned=us&output=rss"
            else:
                headlines_url = "https://news.google.com/news?ned=%s&output=rss" % news_country_code

            feed = feedparser.parse(headlines_url)
            
            for post in feed.entries[0:10]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)
                
                #self.headline.see("end")
                #self.after(10000)
                
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get news." ,e)

        self.after(120000, self.get_headlines)
        
class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=W)

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Abel', extra_small_text_size), fg="white", bg="black", justify=LEFT)
        self.eventNameLbl.pack(side=LEFT, anchor=W, fill=X)