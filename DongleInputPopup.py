# Authors: Buqwana Xolisile and Kagiso Dube 
# Version: 22/10/2025
# Project: EEE3095S Project
# Class Description: Popup to prompt user to input or edit a code value (STM-themed).

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt
from Icon import Icon


class DongleInputPopup(QDialog):
    """Prompts user to input or edit a code value with STM-style UI."""
    def __init__(self, code_id, handler, parent=None):
        super().__init__(parent)
        self.code_id = code_id
        self.handler = handler

        self.setWindowTitle(f"Enter Code {code_id}")
        self.setWindowIcon(Icon.get_icon())
        self.setModal(True)
        self.setFixedSize(360, 200)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self._build_ui()
        self._apply_style()

    def _apply_style(self):
        """Applies STM consistent color scheme and button styling."""
        self.setStyleSheet("""
            QDialog {
                background-color: #05244b;  /* deep navy like interface panels */
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
            }

            QPushButton {
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                padding: 6px 14px;
                min-width: 80px;
            }

            QPushButton#save_btn {
                background-color: #c2c43f;   /* lime green */
                color: white;
            }
            QPushButton#save_btn:hover {
                background-color: #d0d246;
            }
            QPushButton#save_btn:pressed {
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

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Header section
        header = QLabel(f"Enter value for Code {self.code_id}:")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter code here...")
        layout.addWidget(self.input_field)

        # Button row
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        save_btn = QPushButton("Save")
        save_btn.setObjectName("save_btn")

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancel_btn")

        save_btn.clicked.connect(self._on_save)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _on_save(self):
        """Triggered when the user presses Save."""
        code_value = self.input_field.text()
        print(f"[DEBUG] User entered value for Code {self.code_id}: {code_value}")
        self.handler.log_event(f"[User Input] Entered new code for Code {self.code_id}.")
        self.handler.save_new_code(self.code_id, code_value)
        self.accept()
