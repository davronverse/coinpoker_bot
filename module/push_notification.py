import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

def show_push_notification(title, message, icon_path="./img/icon.png", duration=5000):
    # Create the system tray icon
    tray_icon = QSystemTrayIcon()

    if icon_path:
        icon = QIcon(icon_path)
        tray_icon.setIcon(QIcon(icon_path))
    else:
        tray_icon.setIcon(QIcon("./img/icon.png"))  # Replace with a path to a default icon if needed

    tray_icon.setVisible(True)

    # Show the notification
    tray_icon.showMessage(title, message, icon, duration)

# Example usage
# show_push_notification("CoinPoker Bot", "Fish added: poker123", "icon.png")