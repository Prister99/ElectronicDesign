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
from kivy.uix.label import  Label
from kivy.uix.button import  Button
from kivy.uix.widget import  Widget
from kivy.config import Config
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from plyer import sms

Config.set('graphics', 'width',150)
Config.set('graphics', 'height',150)

class MainApp(App):
    lat = "";
    ln = "";
    time = "";
    acc = "";

    def build(self):
        title = "Tcontrol"
        return MySpace()

    def on_pause(self):
        return True
        
class MySpace(Widget):
    recipient = ObjectProperty(None)
    def on_start(self):
        gps.configure(on_location=self.on_gps_location)
        gps.start()
        def on_gps_location(self, **kwargs):
            lat = str(kwargs['lat'])
            ln = str(kwargs['lon'])
    def btn(self,sms_message,sms_recipient):
        sms_recipient = StringProperty()
        sms_message = StringProperty()
        def send_sms(self, *args):
            sms.send(recipient=self.sms_recipient, message=self.sms_message)

if __name__ == '__main__':
    MainApp().run()