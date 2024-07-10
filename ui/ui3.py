import sys
import os
import getpass
import subprocess
import psutil
import winreg as reg
import os

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QComboBox, QListWidget, QListWidgetItem, QCheckBox, QGroupBox, QFormLayout, QSpinBox, QPushButton, QGridLayout, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QPixmap, QIcon
from openpyxl import Workbook, load_workbook

from module.push_notification import show_push_notification
from module.bot import run_bot

NOTIFICATION_TITLE = "CoinPoker BOT"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PlusSpinBox(QSpinBox):
    def textFromValue(self, value):
        return f"{value}+"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CoinPoker Bot")

        # System tray icon
        self.tray_icon = QSystemTrayIcon(QIcon(resource_path("icon.png")), self)
        self.tray_icon.setToolTip("CoinPoker Bot")
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # Menu for tray icon
        self.tray_menu = QMenu()
        restore_action = self.tray_menu.addAction("Restore")
        restore_action.triggered.connect(self.showNormal)

        self.play_stop_action = self.tray_menu.addAction("Play")
        self.play_stop_action.triggered.connect(self.toggle_play)

        quit_action = self.tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.save_settings)
        quit_action.triggered.connect(QApplication.instance().quit)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        # Main layout
        main_layout = QVBoxLayout()

        # Header with image
        header = QLabel()
        pixmap = QPixmap(resource_path("CoinPokerBot.png"))
        header.setPixmap(pixmap)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Status label
        self.status_label = QLabel("CoinPoker is not running")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; color: red; font-weight: bold;")
        main_layout.addWidget(self.status_label)

        # Timer to check if CoinPoker is running
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_coinpoker_running)
        self.timer.start(2000)

        # Grouping the first four inputs
        input_groupbox = QGroupBox("Settings")
        input_groupbox.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")
        form_layout = QFormLayout()

        self.min_blinds_input = QLineEdit()
        self.min_blinds_input.setPlaceholderText("Minimum (e.g., 5/10)")
        self.min_blinds_input.setStyleSheet("padding: 5px; font-size: 16px;")
        form_layout.addRow("Minimum Buy-in Blinds:", self.min_blinds_input)

        self.max_blinds_input = QLineEdit()
        self.max_blinds_input.setPlaceholderText("Maximum (e.g., 50/100)")
        self.max_blinds_input.setStyleSheet("padding: 5px; font-size: 16px;")
        form_layout.addRow("Maximum Buy-in Blinds:", self.max_blinds_input)

        self.seat_checkboxes = []
        seats_layout = QHBoxLayout()
        for seat in ["2", "4", "7"]:
            checkbox = QCheckBox(seat)
            checkbox.setStyleSheet("font-size: 16px; color: black; background-color: white; padding: 5px;")
            self.seat_checkboxes.append(checkbox)
            seats_layout.addWidget(checkbox)
        form_layout.addRow("Seats:", seats_layout)

        self.filled_seats_spinbox = PlusSpinBox()
        self.filled_seats_spinbox.setRange(0, 7)
        self.filled_seats_spinbox.setStyleSheet("padding: 5px; font-size: 16px;")
        form_layout.addRow("Filled Seats:", self.filled_seats_spinbox)

        input_groupbox.setLayout(form_layout)
        main_layout.addWidget(input_groupbox)

        # Color checkboxes
        color_groupbox = QGroupBox("Fish Colors")
        color_groupbox.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")
        color_layout = QGridLayout()

        colors = ["Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Pink"]
        self.color_checkboxes = []
        for i, color in enumerate(colors):
            checkbox = QCheckBox(color)
            checkbox.setStyleSheet(f"font-size: 16px; color: {color.lower()}; padding: 5px;")
            self.color_checkboxes.append(checkbox)
            color_layout.addWidget(checkbox, i // 2, i % 2)

        color_groupbox.setLayout(color_layout)

        # Buttons for Fish section
        self.view_fishes_button = QPushButton("View Fishes")
        self.view_fishes_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.view_fishes_button.clicked.connect(self.view_fishes)

        self.open_file_location_button = QPushButton("Open File Location")
        self.open_file_location_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.open_file_location_button.clicked.connect(self.open_file_location)

        color_layout.addWidget(self.view_fishes_button, 4, 0)
        color_layout.addWidget(self.open_file_location_button, 4, 1)

        main_layout.addWidget(color_groupbox)

        # Play/Stop button
        self.play_button = QPushButton("Play!")
        self.play_button.setStyleSheet("""
            padding: 10px;
            font-size: 16px;
            background-color: #ffcc00;
            color: black;
            font-weight: bold;
            border-radius: 10px;
            border: 2px solid #000;
        """)

        self.play_button.clicked.connect(self.toggle_play)
        main_layout.addWidget(self.play_button)

        # Container widget
        container = QWidget()
        container.setLayout(main_layout)

        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1C1C22;
            }
            QLabel {
                color: white;
            }
            QLineEdit, QComboBox, QSpinBox, QPushButton {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 4px;
            }
            QCheckBox {
                color: white;
            }
            QListWidget {
                height: 50px;
            }
        """)

        self.setCentralWidget(container)

        # Ensure the Fish.xlsx file exists
        self.ensure_fish_file()

        # Load settings from the registry
        self.load_settings()

    def check_coinpoker_running(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == "Lobby.exe":
                self.status_label.setText("CoinPoker is running")
                self.status_label.setStyleSheet("font-size: 18px; color: green; font-weight: bold;")
                return
        self.status_label.setText("CoinPoker is not running")
        self.status_label.setStyleSheet("font-size: 18px; color: red; font-weight: bold;")

    def ensure_fish_file(self):
        username = getpass.getuser()
        file_path = f"C:\\Users\\{username}\\Documents\\CoinPokerBot\\Fish.xlsx"
        dir_path = os.path.dirname(file_path)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if not os.path.exists(file_path):
            wb = Workbook()
            ws = wb.active
            ws.title = "Fishes"
            ws.append(["Name"])
            wb.save(file_path)

    def view_fishes(self):
        username = getpass.getuser()
        file_path = f"C:\\Users\\{username}\\Documents\\CoinPokerBot\\Fish.xlsx"
        os.startfile(file_path)

    def open_file_location(self):
        username = getpass.getuser()
        file_path = f"C:\\Users\\{username}\\Documents\\CoinPokerBot\\Fish.xlsx"
        dir_path = os.path.dirname(file_path)
        subprocess.Popen(f'explorer "{dir_path}"')

    def toggle_play(self):
        if self.play_button.text() == "Play!":
            self.play_button.setText("Stop")
            self.play_button.setStyleSheet("""
                padding: 10px;
                font-size: 16px;
                background-color: #ff3300;
                color: black;
                font-weight: bold;
                border-radius: 10px;
                border: 2px solid #000;
            """)
            self.play_stop_action.setText("Stop")

            show_push_notification(NOTIFICATION_TITLE, "CoinPoker bot is running")

            min_blind = self.min_blinds_input.text()
            max_blind = self.max_blinds_input.text()
            selected_seats = [int(checkbox.text()) for checkbox in self.seat_checkboxes if checkbox.isChecked()]
            filled_min_seats = self.filled_seats_spinbox.value()
            
            run_bot(
                min_blind=min_blind,
                max_blind=max_blind,
                selected_seats=selected_seats,
                filled_min_seats=filled_min_seats
            )
        else:
            self.play_button.setText("Play!")
            self.play_button.setStyleSheet("""
                padding: 10px;
                font-size: 16px;
                background-color: #ffcc00;
                color: black;
                font-weight: bold;
                border-radius: 10px;
                border: 2px solid #000;
            """)
            self.play_stop_action.setText("Play")
            show_push_notification(NOTIFICATION_TITLE, "CoinPoker bot stopped")

    def save_settings(self):
        key = reg.HKEY_CURRENT_USER
        subkey = r"Software\CoinPokerBot"

        try:
            registry_key = reg.OpenKey(key, subkey, 0, reg.KEY_WRITE)
        except FileNotFoundError:
            registry_key = reg.CreateKey(key, subkey)

        reg.SetValueEx(registry_key, "MinBlinds", 0, reg.REG_SZ, self.min_blinds_input.text())
        reg.SetValueEx(registry_key, "MaxBlinds", 0, reg.REG_SZ, self.max_blinds_input.text())
        selected_seats = [checkbox.text() for checkbox in self.seat_checkboxes if checkbox.isChecked()]
        reg.SetValueEx(registry_key, "Seats", 0, reg.REG_SZ, ','.join(selected_seats))
        reg.SetValueEx(registry_key, "FilledSeats", 0, reg.REG_DWORD, self.filled_seats_spinbox.value())

        for i, checkbox in enumerate(self.color_checkboxes):
            reg.SetValueEx(registry_key, f"Color_{i}", 0, reg.REG_DWORD, int(checkbox.isChecked()))

        reg.CloseKey(registry_key)

    def load_settings(self):
        key = reg.HKEY_CURRENT_USER
        subkey = r"Software\CoinPokerBot"

        try:
            registry_key = reg.OpenKey(key, subkey, 0, reg.KEY_READ)
            self.min_blinds_input.setText(reg.QueryValueEx(registry_key, "MinBlinds")[0])
            self.max_blinds_input.setText(reg.QueryValueEx(registry_key, "MaxBlinds")[0])

            seats = reg.QueryValueEx(registry_key, "Seats")[0].split(',')
            for checkbox in self.seat_checkboxes:
                if checkbox.text() in seats:
                    checkbox.setChecked(True)

            self.filled_seats_spinbox.setValue(reg.QueryValueEx(registry_key, "FilledSeats")[0])

            for i, checkbox in enumerate(self.color_checkboxes):
                checkbox.setChecked(bool(reg.QueryValueEx(registry_key, f"Color_{i}")[0]))

            reg.CloseKey(registry_key)
        except FileNotFoundError:
            pass

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal()

    def closeEvent(self, event):
        self.hide()
        event.ignore()
