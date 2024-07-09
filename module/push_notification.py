import sys
import os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def show_push_notification(title, message, icon_path=resource_path("icon.png"), duration=5000):
    # Create the system tray icon
    tray_icon = QSystemTrayIcon()

    if icon_path:
        icon = QIcon(icon_path)
        tray_icon.setIcon(QIcon(icon_path))
    else:
        tray_icon.setIcon(QIcon(resource_path("icon.png")))  # Replace with a path to a default icon if needed

    tray_icon.setVisible(True)

    # Show the notification
    tray_icon.showMessage(title, message, icon, duration)

# Example usage
# show_push_notification("CoinPoker Bot", "Fish added: poker123", "icon.png")