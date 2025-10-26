# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 06/10/2025
# Project: EEE3095S Project
# Class Description: Parent class for all pop ups.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

from Icon import Icon
from ThemeUI import ThemeUI

class PopupBase(QDialog):
    """Base popup dialog class — used for all small message windows."""
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(Icon.get_icon())
        self.setModal(True)
        self.setFixedSize(320, 140)
        self._build_ui(message)
        self.setStyleSheet(ThemeUI.get_stylesheet())
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)


    def _build_ui(self, message: str):
        """Shared layout for popup content."""
        layout = QVBoxLayout()

        # Message text
        self.msg_label = QLabel(message)
        self.msg_label.setAlignment(Qt.AlignCenter)
        self.msg_label.setWordWrap(True)
        layout.addWidget(self.msg_label)

        # OK button
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)
