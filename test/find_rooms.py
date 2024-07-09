import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget

# Start the PyQt application
app = QApplication(sys.argv)

# Find the main window with the title "CoinPoker"
main_window = None

print(app.topLevelWidgets())

for widget in app.topLevelWidgets():
    if widget.windowTitle() == "NL ₮25 IV - NL Hold'em - Blinds ₮ 0.10/₮ 0.25 Ante ₮ 0.02":
        main_window = widget
        break

print(main_window)