# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 21/10/2025
# Project: EEE3095S Project
# Class Description: Initializes the Home Interface.

from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from BaseInterface import BaseInterface

class HomeInterface(BaseInterface):
    """Home screen interface."""
    def __init__(self, handler):
        super().__init__(handler)

    def build(self):
        # Title row with icon and label
        self.title_layout = QHBoxLayout()
        self.title_icon = QLabel()
        self.title_icon.setPixmap(QPixmap(r"C:\Users\xolisile\OneDrive - University of Cape Town\EEE3095S\EEE3095S PROJECT\assets\Home_Logo.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.title_label = QLabel("Welcome — please choose an action")

        self.title_layout.addStretch()
        self.title_layout.addWidget(self.title_icon)
        self.title_layout.addSpacing(8)
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()
        self.layout.addLayout(self.title_layout)

        # Buttons row
        btns = QHBoxLayout()
        connect_btn = QPushButton("Connect Dongle")
        help_btn = QPushButton("Help")
        exit_btn = QPushButton("Exit")

        connect_btn.clicked.connect(self.handler.show_second_interface)
        help_btn.clicked.connect(self.handler.show_help)
        exit_btn.clicked.connect(self.handler.confirm_and_exit)

        btns.addStretch()
        btns.addWidget(connect_btn)
        btns.addSpacing(12)
        btns.addWidget(help_btn)
        btns.addSpacing(12)
        btns.addWidget(exit_btn)
        btns.addStretch()

        self.layout.addLayout(btns)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
