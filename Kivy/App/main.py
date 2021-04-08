import kivy
import kivymd
from plyer import gps
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
kivy.require('1.9.0')
from kivy.app import App
from kivy.uix.boxlayout import  BoxLayout
from kivy.uix.gridlayout import  GridLayout
from kivy.uix.floatlayout import  FloatLayout
from kivy.uix.textinput import  TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import  Label
from kivy.uix.button import  Button
from kivy.uix.widget import  Widget
from kivy.config import Config
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from plyer import sms
import json
from ligotimegps import LIGOTimeGPS
import android-tool
import time
import sys, select, os #for loop exit

Config.set('graphics', 'width',150)
Config.set('graphics', 'height',150)

#Initiate android-module
droid = android.Android()

#notify me
droid.makeToast("fetching GPS data")

print("start gps-sensor...")
droid.startLocating()

class MainApp(App):
    
    def request_android_permissions(self):
     
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):

            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION, Permission.SEND_SMS], callback)
        # # To request permissions without a callback, do:
        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION])
    while True:
            #exit loop hook
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = input()
            print("exit endless loop...")
            break

        #wait for location-event
        event = droid.eventWaitFor('location',10000).result
        if event['name'] == "location":
            try:
                #try to get gps location data
                timestamp = repr(event['data']['gps']['time'])
                longitude = repr(event['data']['gps']['longitude'])
                latitude = repr(event['data']['gps']['latitude'])
                altitude = repr(event['data']['gps']['altitude'])
                speed = repr(event['data']['gps']['speed'])
                accuracy = repr(event['data']['gps']['accuracy'])
                loctype = "gps"
            except KeyError:
                #if no gps data, get the network location instead (inaccurate)
                timestamp = repr(event['data']['network']['time'])
                longitude = repr(event['data']['network']['longitude'])
                latitude = repr(event['data']['network']['latitude'])
                altitude = repr(event['data']['network']['altitude'])
                speed = repr(event['data']['network']['speed'])
                accuracy = repr(event['data']['network']['accuracy'])
                loctype = "net"

            data = longitude + ";" + latitude + ";" + timestamp + ";" + accuracy

        print(data) #logging
        time.sleep(5) #wait for 5 seconds

    print("stop gps-sensor...")
    droid.stopLocating()
    def build(self):
        title = "Tcontrol"
        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            print("sms.py: Android detected. Requesting permissions")
            self.request_android_permissions()

        return MySpace()

    def on_pause(self):
        return True
class MySpace(Widget):
    recipient = ObjectProperty(None)
class IntentButton(Button):
    sms_recipient = StringProperty()
    sms_message = StringProperty()

    def send_sms(self, *args):
        sms.send(recipient=self.sms_recipient, message=self.sms_message)
    #def on_gps_location(self, **kwargs):
   #     lat = str(kwargs['lat'])
  #      ln = str(kwargs['lon'])

if __name__ == '__main__':
    MainApp().run()
   