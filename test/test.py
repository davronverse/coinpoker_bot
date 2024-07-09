from pywinauto import Application
from PyQt5.QtGui import QWindow
from _locale import *
import os
import locale

# Connect to the application
app = Application(backend="uia").connect(path="C:\CoinPoker\Lobby.exe", visible_only=False)

# Access the main window
app_window = app.window(title="GameWindow", auto_id="Lobby", control_type="Window", visible_only=False)

# app_window.print_control_identifiers(filename="out.txt")

# tableView = app_window.child_window(auto_id="CustomTableView", visible_only=True)
tableView = app_window.child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.scrollbarContainer.ListBox", control_type="Table", visible_only=False)
# print(tableView.dump_tree())

element = tableView.child_window(control_type="DataItem", visible_only=False, ctrl_index=0)

print(app_window.dump_tree())

# main_window = app_window.wrapper_object()

# qt_window = QWindow.fromWinId(app_window.handle)

# print(qt_window)

# # child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.filterContainer", control_type="Group")

# # app_window.print_control_identifiers()
# tableView.print_control_identifiers()


# child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.filterContainer.FilterBox", control_type="ComboBox")
# child_window(auto_id="Lobby.captionWrapper.wrapper.content.TabForm.filterContainer.FilterBox", control_type="ComboBox")