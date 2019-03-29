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

from sample import FacialRec

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

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
        '''# initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Abel', small_text_size ), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)'''
        
        '''# initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Abel', small_text_size ), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)'''
        
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
                
            
            '''if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)'''
            '''if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)'''
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)


class Sec(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
        # initialize time label
        self.sec = ''
        self.secLbl = Label(self, font=('Abel', sec_text_size), fg="white", bg="black")
        self.secLbl.pack(side=TOP, anchor=E)
        self.tick()
        
    def tick(self):
        with setlocale(ui_locale):
            sec2 = time.strftime(':%S') #hour in 24h format
            if sec2 != self.sec:
                self.sec = sec2
                self.secLbl.config(text=sec2)
            self.secLbl.after(200, self.tick)
            
class Day(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
       # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Abel', medium_text_size ), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E) 
        self.tick()
        
    def tick(self):
        day_of_week2 = time.strftime('%A,')
        date2 = time.strftime(date_format)
        if day_of_week2 != self.day_of_week1:
            self.day_of_week1 = day_of_week2
            self.dayOWLbl.config(text=day_of_week2)
        #self.timeLbl.after(200, self.tick)
         
         
class Date(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Abel', medium_text_size ), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()
        
    def tick(self):
        day_of_week2 = time.strftime('%A')
        date2 = time.strftime(date_format)
        if date2 != self.date1:
            self.date1 = date2
            self.dateLbl.config(text=date2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        #self.timeLbl.after(200, self.tick)
        
        
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


class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = '---------------------------------------Todays Headlines---------------------------------------'
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
            print ("Error: %s. Cannot get news." + e)

        self.after(120000, self.get_headlines)
        
'''def scroll_textbox(elem):
    # get the current index
    current = float(elem.index(const.CURRENT))
    new = current
    # keep incrementing the index until it's not visible
    while elem.bbox(new):
        new += 1
    # make sure the new index is visible
    elem.see(new)
    # move the index again in 250ms
    elem.after(250, lambda: scroll_textbox(elem))'''
 
class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("assets/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Abel', extra_small_text_size), fg="white", bg="black", justify=LEFT)
        self.eventNameLbl.pack(side=LEFT, anchor=W, fill=X)
        
        #self.self.see("end")
        #self.after(10000)
        
        
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
        
        #self.title = Label(self, text=self.title, font=('Abel', extra_small_text_size), fg="white", bg="black")
        #self.title.pack(side=TOP, anchor=NW)
        
        self.subTitleLbl = Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.subTitleLbl.pack(side=TOP, anchor=NE)
   
        self.calendarEvent1Lbl = Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.calendarEvent1Lbl.pack(side=TOP, anchor=NE)
        
        #self.calendarEvent1TimeLbl =  Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        #self.calendarEvent1TimeLbl.place(x=1015, y=180,width=200, anchor=NE)
        
        self.calendarEvent2Lbl = Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.calendarEvent2Lbl.pack(side=TOP, anchor=NE)
        
        #self.calendarEvent2TimeLbl =  Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        #self.calendarEvent2TimeLbl.place(x=950, y=180,width=200, anchor=NW)
        
        self.calendarEvent3Lbl = Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.calendarEvent3Lbl.pack(side=TOP, anchor=NE)
        
        #self.calendarEvent3TimeLbl =  Label(self, font=('Abel', extra_small_text_size), fg="white", bg="black")
        #self.calendarEvent3TimeLbl.place(x=950, y=195,width=200, anchor=NW)
        #.place(x=1000, y=140,width=350, anchor=NE)
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
            
            '''if self.title != title2:
                    self.title = title2
                    self.title.config(text=subTitle2)'''
            
            if self.subTitle != subTitle2:
                    self.subTitle = subTitle2
                    self.subTitleLbl.config(text=subTitle2)
                    
            if self.calendarEvent1 != calendarEvent11:
                    self.calendarEvent1 = calendarEvent11
                    self.calendarEvent1Lbl.config(text=calendarEvent11)
                    
            '''if self.calendarEvent1TimeLbl != calendarEvent1Time2:
                    self.calendarEvent1Time = calendarEvent1Time2
                    self.calendarEvent1TimeLbl.config(text=calendarEvent1Time2)'''
                    
            if self.calendarEvent2 != calendarEvent22:
                    self.calendarEvent2 = calendarEvent22
                    self.calendarEvent2Lbl.config(text=calendarEvent22)
            
            '''if self.calendarEvent2TimeLbl != calendarEvent2Time2:
                    self.calendarEvent2Time = calendarEvent2Time2
                    self.calendarEvent2TimeLbl.config(text=calendarEvent2Time2)'''
                                                             
            if self.calendarEvent3 != calendarEvent33:
                    self.calendarEvent3 = calendarEvent33
                    self.calendarEvent3Lbl.config(text=calendarEvent33)
            
            '''if self.calendarEvent3TimeLbl != calendarEvent3Time2:
                    self.calendarEvent3Time = calendarEvent3Time2
                    self.calendarEvent3TimeLbl.config(text=calendarEvent3Time2)'''
                                                             
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get calendar." , e)

        self.after(600000, self.get_events)


'''class CalendarEvent(Frame):
    def __init__(self, parent, event_name="Event 1"):
        Frame.__init__(self, parent, bg='black')
        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Abel', extra_small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=TOP, anchor=E)'''
 
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
            
'''class FacialRec():
    
    def get_FacialRecognition(self):
        try:
    # Capture frames from the camera
            for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):

                image = frame.array

                # Look for faces and phones in the image using the loaded cascade file
                gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                faces  = face_cascade.detectMultiScale(gray)
                phones = phone_cascade.detectMultiScale(gray)

                # Draw a rectangle around every face
                
                
                for (x,y,w,h) in faces:
                    cv2.rectangle( image, ( x, y ), ( x + w, y + h ), ( 255, 255, 0 ), 2 )
                    cv2.putText( image, "face detected" + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )
                    print('Face Detected')
                    #camera.resolution = ( 320, 240 )
                    #rawCapture = PiRGBArray( camera, size=( 320, 240 ) )
                    #camera.start_preview()
                    sleep(5)
                    camera.capture('/tmp/cameraTest.jpg')
                    #camera.stop_preview()
                    #sleep(15)
                    
                    

                # Draw a rectangle around every phone
                for (x,y,w,h) in phones:
                    cv2.rectangle( image, ( x, y ), ( x + w, y + h ), ( 255, 0, 0 ), 2 )
                    cv2.putText( image, "iPhone", ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 255, 255 ), 2 )

                # Calculate and show the FPS
                fps = fps + 1
                sfps = fps / ( time.time() - t_start )
                cv2.putText( image, "FPS : " + str( int( sfps ) ), ( 10, 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )
                cv2.imshow( "Frame", image )
                cv2.waitKey( 1 )

                # Clear the stream in preparation for the next frame
                rawCapture.truncate( 0 )
                break
                #continue
            
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get face." + e)

            self.after(600000, self.get_FacialRecognition)'''
            
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
        #Crypto
        self.crypto = Crypto(self.topFrame)
        self.crypto.pack(side=TOP, anchor=NE)
        #Crypto Time
        self.cryptoPrice = CryptoPrice(self.topFrame)
        self.cryptoPrice.pack(side=TOP, anchor=NE)
        #camera
        s = FacialRec()
        #s.get_FacialRecognition()
        #s.run()
        
        
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