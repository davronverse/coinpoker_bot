from pywinauto import Application
from _locale import *
import os
import locale

# auto_id="Lobby.captionWrapper.wrapper.content.TabForm.scrollbarContainer.ListBox", control_type="Table"
# Connect to the application
app = Application(backend="uia").connect(path="C:\CoinPoker\Lobby.exe")
# Access the main window
app_window = app["GameWindow"]

# tableView = app_window.child_window(auto_id="CustomTableView", visible_only=True)
tableView = app_window.child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.filterContainer", control_type="Group")

# child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.filterContainer", control_type="Group")

# app_window.print_control_identifiers()
tableView.print_control_identifiers()






# child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.filterContainer.FilterBox", control_type="ComboBox")
# child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.filterContainer.FilterBox", control_type="ComboBox")