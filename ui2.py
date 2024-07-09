import sys
import os
import getpass
import subprocess
import psutil
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QComboBox, QCheckBox, QGroupBox, QFormLayout, QSpinBox, QPushButton
from PyQt5.QtGui import QPixmap
from openpyxl import Workbook, load_workbook

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CoinPoker Bot")

        # Main layout
        main_layout = QVBoxLayout()

        # Header with image
        header = QLabel()
        pixmap = QPixmap("CoinPokerBot.png")
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

        self.seats_combobox = QComboBox()
        self.seats_combobox.addItems(["2", "4", "7"])
        self.seats_combobox.setStyleSheet("padding: 5px; font-size: 16px;")
        form_layout.addRow("Seats:", self.seats_combobox)

        self.filled_seats_spinbox = QSpinBox()
        self.filled_seats_spinbox.setRange(0, 7)
        self.filled_seats_spinbox.setStyleSheet("padding: 5px; font-size: 16px;")
        form_layout.addRow("Filled Seats:", self.filled_seats_spinbox)

        input_groupbox.setLayout(form_layout)
        main_layout.addWidget(input_groupbox)

        # Color checkboxes
        color_groupbox = QGroupBox("Fish Colors")
        color_groupbox.setStyleSheet("font-size: 16px; color: white; font-weight: bold;")
        color_layout = QVBoxLayout()

        colors = ["Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Pink"]
        self.color_checkboxes = []
        for color in colors:
            checkbox = QCheckBox(color)
            checkbox.setStyleSheet(f"font-size: 16px; color: {color.lower()}; padding: 5px;")
            self.color_checkboxes.append(checkbox)
            color_layout.addWidget(checkbox)

        color_groupbox.setLayout(color_layout)

        # Buttons for Fish section
        self.view_fishes_button = QPushButton("View Fishes")
        self.view_fishes_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.view_fishes_button.clicked.connect(self.view_fishes)

        self.open_file_location_button = QPushButton("Open File Location")
        self.open_file_location_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.open_file_location_button.clicked.connect(self.open_file_location)

        color_layout.addWidget(self.view_fishes_button)
        color_layout.addWidget(self.open_file_location_button)

        main_layout.addWidget(color_groupbox)

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
        """)

        self.setCentralWidget(container)

        # Ensure the Fish.xlsx file exists
        self.ensure_fish_file()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
