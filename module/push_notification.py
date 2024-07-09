import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

def show_push_notification(title, message, icon_path=None, duration=5000):
    app = QApplication(sys.argv)
    
    # Create the system tray icon
    tray_icon = QSystemTrayIcon()

    if icon_path:
        icon = QIcon(icon_path)
        tray_icon.setIcon(QIcon(icon_path))
    else:
        tray_icon.setIcon(QIcon("icon.png"))  # Replace with a path to a default icon if needed

    tray_icon.setVisible(True)

    # Show the notification
    tray_icon.showMessage(title, message, icon, duration)

    # Create a menu for the tray icon (optional)
    menu = QMenu()
    exit_action = QAction("Exit", app)
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)
    tray_icon.setContextMenu(menu)
    
    # Run the application event loop
    sys.exit(app.exec_())

# Example usage
show_push_notification("CoinPoker Bot", "Fish added: poker123", "icon.png")