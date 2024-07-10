import pyautogui
import pywinauto
import win32gui 
import random
import os
import locale
import re

from time import sleep
from pywinauto import Application
from _locale import *
from pywinauto.controls.uia_controls import ListItemWrapper, ListViewWrapper

# Connect to the application
app = Application(backend="uia").connect(path="C:\CoinPoker\Lobby.exe")

# Access the main window
app_window = app["GameWindow"]
app_win_wrapper = app_window.set_focus() # not needed if this is already in focus (needed during debug)

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

# Access to the Buy-in Filter Dropdown
# buyin_element = app_window.child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.filterContainer.FilterBox", control_type="ComboBox", top_level_only=True, found_index=1)
# mouse_click(buyin_element)

# buyin_check1 = buyin_element.child_window(title="Low (Up to ₮25)", control_type="ListItem", top_level_only=True)
# mouse_click(buyin_check1)
# buyin_check2 = buyin_element.child_window(title="Medium (₮50 - ₮200)", control_type="ListItem", top_level_only=True)
# mouse_click(buyin_check2)
# buyin_check3 = buyin_element.child_window(title="High (₮500+)", control_type="ListItem", top_level_only=True)
# mouse_click(buyin_check3)

# # Access to the Seats Filter Dropdown
# seats_element = app_window.child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.filterContainer.FilterBox", control_type="ComboBox", top_level_only=True, found_index=2)
# mouse_click(seats_element)

# seats_check1 = seats_element.child_window(title="2", control_type="ListItem", top_level_only=True)
# mouse_click(seats_check1)
# seats_check2 = seats_element.child_window(title="4", control_type="ListItem", top_level_only=True)
# mouse_click(seats_check2)
# seats_check3 = seats_element.child_window(title="7", control_type="ListItem", top_level_only=True)
# mouse_click(seats_check3)

# Access to the Rooms Table
# table = app_window.child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.scrollbarContainer.ListBox", control_type="Table")

# def refresh_table():
#     updated_table = app_window.child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.scrollbarContainer.ListBox", control_type="Table")
#     return updated_table

def get_value_from_blind(s):
    pattern = r'^\D*([\d.]+)'
    match = re.search(pattern, s)
    if match:
        first_value = match.group(1)
        return float(first_value)
    return 0

def get_first_value_from_seats(s):
    first_value_str = s.split('/')[0].strip()
    try:
        first_value = float(first_value_str)  # Convert to float (or int if whole number)
        return first_value
    except ValueError:
        return 0

def get_second_value_from_seats(s):
    second_value_str = s.split('/')[1].strip()
    try:
        second_value = float(second_value_str)  # Convert to float (or int if whole number)
        return second_value
    except ValueError:
        return 0
    
def one_page_process(MIN_BLIND = 10, MAX_BLIND = 100, SEATS = [2, 4, 7], FILLED_MIN_SEATS = 1, first_page=False):
    table = app_window.child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.scrollbarContainer.ListBox", control_type="Table", found_index=0, visible_only=True)

    rows = []
    stack = []
    for child in table.children():
        control_type = child.element_info.control_type

        if control_type == 'DataItem':
            stack.append(child)

            if len(stack) == 7:
                rows.append(stack.copy())
                stack.clear()

    # duplicated
    if not first_page:
        rows.pop(0)

    mouse_click(rows[0][0])

    for i in range(len(rows)):
        # check if row meets filter criteria
        blind = rows[i][3].element_info.name
        room = rows[i][4].element_info.name

        print(blind, room)

        blind = get_value_from_blind(blind)
        filled = get_first_value_from_seats(room)

        seats = get_second_value_from_seats(room)
        left = seats - filled

        if blind >= MIN_BLIND and blind <= MAX_BLIND and seats in SEATS and filled >= FILLED_MIN_SEATS and left > 0:
            key_press("enter")
            win32gui.SetForegroundWindow(app_window.wrapper_object().handle)
            key_press("down")
        
        else:
            key_press("down")

    key_press('pagedown')

def run_bot(min_blind, max_blind, selected_seats, filled_min_seats):
    MIN_BLIND = get_value_from_blind(min_blind)
    MAX_BLIND = get_value_from_blind(max_blind)
    SEATS = selected_seats
    FILLED_MIN_SEATS = int(filled_min_seats)

    for i in range(5):
        if i == 0:
            one_page_process(
                MIN_BLIND=MIN_BLIND,
                MAX_BLIND=MAX_BLIND,
                SEATS=SEATS,
                FILLED_MIN_SEATS=FILLED_MIN_SEATS,
                first_page = True)
        else:
            one_page_process(
                MIN_BLIND=MIN_BLIND,
                MAX_BLIND=MAX_BLIND,
                SEATS=SEATS,
                FILLED_MIN_SEATS=FILLED_MIN_SEATS,
                first_page = False)