from time import sleep
from pywinauto import Application
from _locale import *
import os
import locale

# auto_id="Lobby.captionWrapper.wrapper.content.TabForm.scrollbarContainer.ListBox", control_type="Table"
# Connect to the application
app = Application(backend="uia").connect(path="C:\CoinPoker\Lobby.exe")

# Access the main window
app_window = app["GameWindow"]
app_win_wrapper = app_window.set_focus() # not needed if this is already in focus (needed during debug)

# tableView = app_window.child_window(auto_id="CustomTableView", visible_only=True)
# tableView = app_window.child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.scrollbarContainer.ListBox", control_type="Table")

parent = app_window.child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.filterContainer.FilterBox", control_type="ComboBox", top_level_only=True, found_index=1)
buy_combo1 = app_window.child_window(parent=parent, title="Low (Up to ₮25)", control_type="ListItem", top_level_only=True)

print("Starting...")

parent.wrapper_object().invoke()
buy_combo1.wrapper_object().click_input()
# parent.print_control_identifiers()
# app_window.print_control_identifiers()