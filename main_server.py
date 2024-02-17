import os
import subprocess
import socket
import json
import time

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
from ping3 import ping, verbose_ping

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


