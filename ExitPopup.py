# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 06/10/2025
# Project: EEE3095S Project
# Class Description: Initializes the Exit pop up interface class.

from PyQt5.QtWidgets import QMessageBox, QApplication, QPushButton
from PopupBase import PopupBase

class ExitPopup(PopupBase):
    """Popup that asks user to confirm exit."""
    def __init__(self, parent=None):
        super().__init__("Confirm Exit", "Are you sure you want to exit?", parent)
        self.ok_btn.deleteLater()

        # Create custom message box
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Confirm Exit")
        msg_box.setText("Are you sure you want to exit?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.setIcon(QMessageBox.NoIcon)  

        # Apply custom styles to the message box
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #05244b;
                color: #dee4e7;
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
                font-size: 13px;
            }

            QPushButton {
                border: none;
                border-radius: 8px;
                min-width: 90px;
                min-height: 36px;
                font-weight: 600;
                color: #dee4e7;
            }

            QPushButton:hover {
                opacity: 0.9;
            }
        """)

        # Get the buttons and style them individually
        yes_button = msg_box.button(QMessageBox.Yes)
        no_button = msg_box.button(QMessageBox.No)

        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #c2c43f;
                color: white;
                border: none;
                border-radius: 8px;
                min-width: 90px;
                min-height: 36px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #d0d246; }
            QPushButton:pressed { background-color: #a8aa36; }
        """)

        no_button.setStyleSheet("""
            QPushButton {
                background-color: #1184d5;
                color: #dee4e7;
                border: none;
                border-radius: 8px;
                min-width: 90px;
                min-height: 36px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #1a9ee9; }
            QPushButton:pressed { background-color: #0f6bab; }
        """)

        reply = msg_box.exec_()  

        if reply == QMessageBox.Yes:
            QApplication.instance().quit()
