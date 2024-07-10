from time import sleep
from pywinauto import Application
from _locale import *
import pyautogui
import pywinauto
import win32gui 

import random
import os
import locale

from pywinauto.controls.uia_controls import ListItemWrapper, ListViewWrapper


def mouse_click(element):
    rect = element.rectangle()
    # rect = element.rectangle()
    # Extract the coordinates of the center of the element
    x = rect.left + (rect.right - rect.left) // 2
    y = rect.top + (rect.bottom - rect.top) // 2
    pyautogui.moveTo(x, y, duration=0)  # Optional: Move the mouse cursor visibly (can be omitted if not needed)

    # Simulate a left mouse button click at the specified coordinates
    pyautogui.mouseDown()
    pyautogui.mouseUp()

def key_press(key):
    pyautogui.keyDown(key)
    pyautogui.keyUp(key)

# Connect to the application
app = Application(backend="win32").connect(path="C:\CoinPoker\Lobby.exe")

# Access the main window
app_window = app["CoinPoker - Lobby"]
app_win_wrapper = app_window.set_focus() # not needed if this is already in focus (needed during debug)

print(app_window.dump_tree())