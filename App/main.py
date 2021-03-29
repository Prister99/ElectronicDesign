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


Config.set('graphics', 'width',150)
Config.set('graphics', 'height',150)

class MainApp(App):
    lat = "";
    ln = "";
    tmstmp = "";
    minTime = 5000;
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')
    
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

    def build(self):
        title = "Tcontrol"
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            print("sms.py: Android detected. Requesting permissions")
            self.request_android_permissions()

        return MySpace()

    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()
    
    @mainthread    
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()]) 

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_pause(self):
        gps.stop()
        return True

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
   