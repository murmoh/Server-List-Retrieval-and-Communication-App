from kivy.animation import Animation
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from ping3 import ping, verbose_ping
from kivy.config import Config
import socket
import threading
import sys
from blur import *

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

Window.size = (1920 / 2, 1080 / 2)


class MyApp(MDApp):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')

        self.theme_cls.theme_style = "Dark"  # or "Dark"
        self.theme_cls.primary_palette = "Orange"  # choose a color that fits your design

        action_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height='80dp')

        # Add widgets to the action layout
        message = MDTextField(hint_text='Message Here')
        action_layout.add_widget(message)

        # Create a card for the message box
        message_display = MDCard(orientation="vertical", padding="8dp")
        bg_color = {
            "Red": (255, 0, 0, 1),
            "Blue": (0, 0, 255, 1),
            "Black": (0, 0, 0, 1),
            "Gray": (1, 1, 1, 0.1),
            "White": (255, 255, 255, 1),
            "Green": (0, 255, 0, 1)
        }
        message_display.on_md_bg_color(instance_md_widget="", color=bg_color.get('Gray'))
        scroll_view = ScrollView(do_scroll_x=False)
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding="8dp", spacing="4dp")
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        scroll_view.add_widget(scroll_layout)
        message_display.add_widget(scroll_view)
        main_layout.add_widget(action_layout)
        main_layout.add_widget(message_display)

        # Handle button press
        def send_message(instance):
            if message.text:
                label = Label(text=message.text, size_hint_y=None, height="24dp", color=(1, 1, 1, 1))
                scroll_layout.add_widget(label)
                message.text = ""

        # Create a button to send the message
        send_button = MDRectangleFlatButton(text="Send", on_release=send_message)
        action_layout.add_widget(send_button)

        # Users = MDLabel(text='Online Users')
        # action_layout.add_widget(Users)
        return main_layout


if __name__ == '__main__':
    MyApp().run()
