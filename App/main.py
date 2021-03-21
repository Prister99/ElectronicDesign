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

lat = "";
lon = "";
time = "";
acc = "";

        
class MySpace(Widget):
    recipient = ObjectProperty(None)

    def onLocationChanged(self, location):
        self.root.on_location(
                lat=location.getLatitude(),
                lon=location.getLongitude(),
                acc=location.getAccuracy(),
                time=Location.getTimeStamp())
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')

    def btn(self,sms_message,sms_recipient):
        sms_recipient = StringProperty()
        sms_message = StringProperty()
        def send_sms(self, *args):
            sms.send(recipient=self.sms_recipient, message=self.sms_message)
   

class MainApp(App):
    
    def build(self):
        title = "Tcontrol"
        return MySpace()

    def on_pause(self):
        return True
    
    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start(3000, 0)
        pass

    def _send(self, **kwargs):
        raise NotImplementedError()

    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.
        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION], callback)
        # # To request permissions without a callback, do:
        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION])
     
def build(self):
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()
        return MyWidgets(Widget)



if __name__ == '__main__':
    MainApp().run()