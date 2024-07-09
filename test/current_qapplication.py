from pywinauto import Application
from PyQt5.QtGui import QWindow
from PyQt5 import QtWidgets
from _locale import *
import os
import locale

app = QtWidgets.qApp

print(app.arguments())