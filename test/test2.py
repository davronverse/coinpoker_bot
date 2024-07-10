from time import sleep
from pywinauto import Application
from _locale import *
import pyautogui
import pywinauto
import win32gui 

from pywinauto import timings

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget

# Connect to the application
app = Application(backend="uia").connect(path="C:\CoinPoker\Lobby.exe")

# Access the main window
app_window = app["GameWindow"]

app_handle = app_window.wrapper_object().handle

print(app_window.window_text())
print(app_window.class_name())
print(app_window.handle)

# Send the BM_CLICK message to the button
import ctypes
ctypes.windll.user32.SendMessageW(app_handle, 0x00F5, 100, 700)