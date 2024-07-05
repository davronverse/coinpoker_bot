import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget

# Start the PyQt application
app = QApplication(sys.argv)

# Find the main window with the title "CoinPoker"
main_window = None
for widget in app.topLevelWidgets():
    if widget.windowTitle() == "CoinPoker":
        main_window = widget
        break

print(main_window)