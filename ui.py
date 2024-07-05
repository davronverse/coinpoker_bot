import sys
import psutil
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QComboBox, QCheckBox, QGroupBox, QFormLayout, QSpinBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CoinPoker Bot")
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel("CoinPoker Bot")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; color: white;")
        main_layout.addWidget(header)
        
        # Status label
        self.status_label = QLabel("CoinPoker is not running")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; color: red;")
        main_layout.addWidget(self.status_label)
        
        # Timer to check if CoinPoker is running
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_coinpoker_running)
        self.timer.start(2000)
        
        # Buy-in Blinds selection
        form_layout = QFormLayout()
        
        self.min_blinds_input = QLineEdit()
        self.min_blinds_input.setPlaceholderText("Minimum (e.g., 5/10)")
        form_layout.addRow("Minimum Buy-in Blinds:", self.min_blinds_input)
        
        self.max_blinds_input = QLineEdit()
        self.max_blinds_input.setPlaceholderText("Maximum (e.g., 50/100)")
        form_layout.addRow("Maximum Buy-in Blinds:", self.max_blinds_input)
        
        # Seats selection
        self.seats_combobox = QComboBox()
        self.seats_combobox.addItems(["2", "4", "7"])
        form_layout.addRow("Seats:", self.seats_combobox)
        
        # Filled Seats
        self.filled_seats_spinbox = QSpinBox()
        self.filled_seats_spinbox.setRange(0, 7)
        form_layout.addRow("Filled Seats:", self.filled_seats_spinbox)
        
        # Color checkboxes
        color_groupbox = QGroupBox("Fish Colors")
        color_layout = QVBoxLayout()
        
        colors = ["Red", "Green", "Blue", "Yellow", "Orange", "Purple", "Pink"]
        self.color_checkboxes = []
        for color in colors:
            checkbox = QCheckBox(color)
            checkbox.setStyleSheet(f"color: {color.lower()};")
            self.color_checkboxes.append(checkbox)
            color_layout.addWidget(checkbox)
        
        color_groupbox.setLayout(color_layout)
        form_layout.addRow(color_groupbox)
        
        main_layout.addLayout(form_layout)
        
        # Container widget
        container = QWidget()
        container.setLayout(main_layout)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
            }
            QLabel {
                color: white;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
            }
            QCheckBox {
                color: white;
            }
        """)
        
        self.setCentralWidget(container)
    
    def check_coinpoker_running(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == "CoinPoker":
                self.status_label.setText("CoinPoker is running")
                self.status_label.setStyleSheet("font-size: 18px; color: green;")
                return
        self.status_label.setText("CoinPoker is not running")
        self.status_label.setStyleSheet("font-size: 18px; color: red;")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
