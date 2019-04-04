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


# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}

class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.wind = ''
        self.icon = ''
        self.moonPhase = ''
        
        self.windLbl = Label(self, bg="black")
        self.windLbl.place(x=0, y=250, anchor=W)
        
        self.windSpeedLbl = Label(self, font=('Abel', small_text_size), fg="white", bg="black")
        self.windSpeedLbl.place(x=55, y=250, anchor=W)
        
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W, padx=250)
        
        self.temperatureLbl = Label(self.degreeFrm, font=('Abel', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=RIGHT, anchor=NE, ipady=0)
        
        self.iconLbl = Label(self, bg="black")
        self.iconLbl.place(x=130, y=5)
        
        self.moonPhaseLbl = Label(self, bg="black")
        self.moonPhaseLbl.place(x=0, y=5)
        
        self.currentlyLbl = Label(self, font=('Abel', small_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        
        self.locationLbl = Label(self, font=('Abel', small_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        
        self.forecastLbl = Label(self, font=('Abel', small_text_size), fg="white", bg="black")
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.get_weather()
        
    def get_ip(self):
        try:
            ip_url = "http://jsonip.com"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            print (req.text)
            print (ip_json)
            return ip_json['ip']
        
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get ip: "  + e)
            
        
    def get_weather(self):
        try:
                
            # get weather  ------------------------------------------------
            weather_req_url = "https://api.darksky.net/forecast/52cb312030821b9d32409a1452c4fbec/53.2521,-8.9978?lang=en&units=si"
            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)
            
            location2 = weather_obj['timezone']
            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]
            wind2 = weather_obj["currently"]["windSpeed"]
            
            #Weather icon -------------------------------------------------
            icon_id = weather_obj['currently']['icon']
            icon2 = None
        
            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')
            
            #Wind icon ----------------------------------------------------
            image = Image.open("assets/Wind.png")
            image = image.resize((50, 50), Image.ANTIALIAS)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)
            
            self.windLbl.config(image=photo)
            self.windLbl.image = photo
                    
                    
            #MoonPhase icon -----------------------------------------------
            icon_id2 = weather_obj['daily']['data'][0]
            
            icon3 = None
        
            if icon_id2['moonPhase'] >= 0 and icon_id2['moonPhase'] <0.1:
                icon3 = "assets/NewMoon.png"
                
            elif icon_id2['moonPhase'] >= 0.1 and icon_id2['moonPhase'] <0.2:
                icon3 = "assets/WaxingCrescent.png"
                
            elif icon_id2['moonPhase'] >= 0.2 and icon_id2['moonPhase'] <0.3:
                icon3 = "assets/FirstQuarter.png"
                
            elif icon_id2['moonPhase'] >= 0.3 and icon_id2['moonPhase'] <0.4:
                icon3 = "assets/WaxingGibbous.png"
                
            elif icon_id2['moonPhase'] >= 0.4 and icon_id2['moonPhase'] <0.6:
                icon3 = "assets/FullMoon.png"
                
            elif icon_id2['moonPhase'] >= 0.6 and icon_id2['moonPhase']<0.7:
                icon3 = "assets/WaningGibbous.png"
                
            elif icon_id2['moonPhase'] >= 0.7 and icon_id2['moonPhase'] <0.8:
                icon3 = "assets/LastQuarter.png"
                
            elif icon_id2['moonPhase'] >= 0.8 and icon_id2['moonPhase'] <1:
                icon3 = "assets/WaningCrescent.png"
                

            if icon3 is not None:
                if self.moonPhase != icon3:
                    self.moonPhase = icon3
                    image = Image.open(icon3)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.moonPhaseLbl.config(image=photo)
                    self.moonPhaseLbl.image = photo
            else:
                # remove image
                self.moonPhaseLbl.config(image='')
            
            #Update weather ----------------------------------------------
            if self.wind != wind2:
                self.wind = wind2
                self.windSpeedLbl.config(text=wind2)
                
            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
                
            '''if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)'''
            
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
                
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
                    
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get weather. " % e

        self.after(600000, self.get_weather)

        @staticmethod
        def convert_kelvin_to_fahrenheit(kelvin_temp):
            return 1.8 * (kelvin_temp - 273) + 32
