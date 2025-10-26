# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 23/10/2025
# Project: EEE3095S Project
# Class Description: Popup for selecting a COM port and connecting to STM.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
import serial.tools.list_ports


class ConnectPopup(QDialog):
    """Popup window for selecting COM port and connecting to STM device."""

    def __init__(self, handler=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connect to STM Dongle")
        self.setFixedSize(350, 180)
        self.setModal(True)

        self.handler = handler
        self.selected_port = None  

        # Layout setup 
        layout = QVBoxLayout()

        label = QLabel("Select COM Port:")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        # Port selector dropdown
        self.port_box = QComboBox()
        layout.addWidget(self.port_box, alignment=Qt.AlignCenter)

        # Buttons 
        btn_layout = QHBoxLayout()
        self.connect_btn = QPushButton("Connect")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.connect_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Connections 
        self.connect_btn.clicked.connect(self.connect_action)
        self.cancel_btn.clicked.connect(self.reject)

        # Check for available COM ports 
        self.refresh_ports()

    # Populate available COM ports
    def refresh_ports(self):
        """Refresh and list available COM ports dynamically."""
        ports = serial.tools.list_ports.comports()
        self.port_box.clear()

        if not ports:
            self.port_box.addItem("No COM ports found")
            self.port_box.setEnabled(False)
            self.connect_btn.setEnabled(False)
        else:
            for p in ports:
                self.port_box.addItem(p.device)
            self.port_box.setEnabled(True)
            self.connect_btn.setEnabled(True)

    # When user clicks Connect
    def connect_action(self):
        """Store selected port and close popup with success code."""
        if not self.port_box.isEnabled():
            self.reject()
            return

        self.selected_port = self.port_box.currentText()
        if not self.selected_port or "No COM ports" in self.selected_port:
            self.reject()
        else:
            print(f"[DEBUG] User selected port: {self.selected_port}")
            self.accept()

