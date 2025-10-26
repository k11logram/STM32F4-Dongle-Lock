# Authors: Buqwana Xolisile and Kagiso Dube 
# Version: 06/10/2025
# Project: EEE3095S Project
# Class Description: Initializes the Help Interface class.

from PyQt5.QtWidgets import QLabel, QTextEdit, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from BaseInterface import BaseInterface


class HelpInterface(BaseInterface):
    def __init__(self, handler):
        super().__init__(handler)

    def build(self):
        header = QLabel("Support Help")
        header.setFont(QFont("Helvetica", 14, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header)
 
        text = QTextEdit()
        text.setReadOnly(True)

        text.setHtml("""
            <div style="
                background-color: #ffffff;
                color: #000000;
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
                font-size: 13px;
                line-height: 1.6;
                padding: 10px;
            ">
                <p style="font-size: 14px; font-weight: 500; margin-bottom: 10px;">
                    <b>Welcome to STM32 Dongle Locker Support</b>
                </p>

                <p>Follow these simple steps to operate the application:</p>

                <ol style="margin-left: 20px; margin-top: 8px;">
                    <li><b>Connect Dongle</b> — Click this to reveal connection options.</li>
                    <li><b>Connect</b> — On the next screen, click <b>Connect</b> to attempt communication with your STM device.</li>
                    <li><b>Connection Status</b> — A popup will show whether the connection was successful:
                        <ul style="margin-top: 5px;">
                            <li><span style="color:green;"><b>Device Successfully Connected</b></span></li>
                            <li><span style="color:red;"><b>Device Not Found</b></span></li>
                        </ul>
                    </li>
                    <li><b>Exit</b> — Use this option to safely close the application.</li>
                </ol>
            </div>
        """)
 
        text.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: #ffffff;
                color: #000000;
                border-radius: 6px;
            }
        """)

        text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(text)
 
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.handler.show_first_interface)
        b_layout = QHBoxLayout()
        b_layout.addStretch()
        b_layout.addWidget(back_btn)
        b_layout.addStretch()
        self.layout.addLayout(b_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
