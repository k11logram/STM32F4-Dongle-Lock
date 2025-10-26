# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 22/10/2025
# Project: EEE3095S Project
# Class Description: STM-themed popup for selecting which code to edit or clear.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from Icon import Icon

class CodeSelectPopup(QDialog):
    """STM-styled popup for choosing which code to edit or clear."""
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(Icon.get_icon())
        self.setModal(True)
        self.setFixedSize(340, 180)
        self.code_id = None
        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self._build_ui(message)
        self._apply_style()

    def _apply_style(self):
        """Applies STM navy and button theme."""
        self.setStyleSheet("""
            QDialog {
                background-color: #05244b;  /* deep navy theme */
                border-radius: 10px;
                font-family: Segoe UI, Arial;
                color: white;
            }

            QLabel {
                color: #dee6f3;
                font-weight: 600;
                font-size: 13px;
            }

            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #0077b6;
                border-radius: 6px;
                padding: 6px;
                font-size: 13px;
                color: #05244b;
                qproperty-alignment: AlignCenter;
            }
            QLineEdit:focus {
                border: 1px solid #1a9ee9;
                background-color: #f0faff;
            }

            QPushButton {
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                padding: 6px 14px;
                min-width: 80px;
            }

            QPushButton#ok_btn {
                background-color: #c2c43f;   /* lime green */
                color: white;
            }
            QPushButton#ok_btn:hover {
                background-color: #d0d246;
            }
            QPushButton#ok_btn:pressed {
                background-color: #a8aa36;
            }

            QPushButton#cancel_btn {
                background-color: #1184d5;   /* STM blue */
                color: #dee4e7;
            }
            QPushButton#cancel_btn:hover {
                background-color: #1a9ee9;
            }
            QPushButton#cancel_btn:pressed {
                background-color: #0f6bab;
            }
        """)

    def _build_ui(self, message):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Message
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Input
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter code number (1–3)")
        layout.addWidget(self.input)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        ok_btn = QPushButton("OK")
        ok_btn.setObjectName("ok_btn")

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancel_btn")

        ok_btn.clicked.connect(self._on_ok)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(ok_btn)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _on_ok(self):
        """Validates and stores the selected code ID."""
        try:
            val = int(self.input.text())
            if val in [1, 2, 3]:
                self.code_id = val
                self.accept()
            else:
                self.input.clear()
                self.input.setPlaceholderText("Enter 1, 2, or 3 only")
        except ValueError:
            self.input.clear()
            self.input.setPlaceholderText("Please enter a number")
