# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 06/10/2025
# Project: EEE3095S Project
# Class Description: Initializes the Connected Interface class.

from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from BaseInterface import BaseInterface

class ConnectedInterface(BaseInterface):
    """Connected screen interface."""
    def __init__(self, handler):
        super().__init__(handler)

    def build(self):
        title_layout = QHBoxLayout()
        usb_icon = QLabel()
        usb_icon.setPixmap(QPixmap("C:/Users/xolisile/OneDrive - University of Cape Town/EEE3095S/EEE3095S PROJECT/assets/USB_logo.png").scaled(
            30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        text_label = QLabel("Dongle — connection options")
        text_label.setAlignment(Qt.AlignCenter)

        title_layout.addStretch()
        title_layout.addWidget(usb_icon)
        title_layout.addSpacing(8)
        title_layout.addWidget(text_label)
        title_layout.addStretch()
        self.layout.addLayout(title_layout)

        # Buttons 
        btns = QHBoxLayout()
        connect_btn = QPushButton("Connect")
        help_btn = QPushButton("Help")
        exit_btn = QPushButton("Exit")

        # Connect button 
        connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #c2c43f;
                color: white;
                border: none;
                border-radius: 8px;
                min-width: 140px;
                min-height: 42px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #d0d246; }
            QPushButton:pressed { background-color: #a8aa36; }
        """)

        # Help button
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #f2e36b;
                color: white;
                border: none;
                border-radius: 8px;
                min-width: 140px;
                min-height: 42px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #f7eb7a; }
            QPushButton:pressed { background-color: #e5d85d; }
        """)

        # Exit button (blue)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #1184d5;
                color: #dee4e7;
                border: none;
                border-radius: 8px;
                min-width: 140px;
                min-height: 42px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #1a9ee9; }
            QPushButton:pressed { background-color: #0f6bab; }
        """)

        # Connect signals
        connect_btn.clicked.connect(self.handler.attempt_connect)
        exit_btn.clicked.connect(self.handler.confirm_and_exit)
        help_btn.clicked.connect(self.handler.show_help)

        # Layout
        btns.addStretch()
        btns.addWidget(connect_btn)
        btns.addSpacing(12)
        btns.addWidget(help_btn)
        btns.addSpacing(12)
        btns.addWidget(exit_btn)
        btns.addStretch()

        self.layout.addSpacing(20)
        self.layout.addLayout(btns)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
