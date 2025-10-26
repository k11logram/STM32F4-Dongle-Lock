# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 06/10/2025
# Project: EEE3095S Project
# Class Description: Renders the Dongle Interface.

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from Icon import Icon
from ThemeUI import ThemeUI
from HomeInterface import HomeInterface
from HelpInterface import HelpInterface
from ConnectedInterface import ConnectedInterface
from DongleSTMInterface import DongleSTMInterface
from DongleSTMHandler import DongleSTMHandler


class DongleInterfaceInit:
    """Sets up the main GUI container window.
       Delegates each interface (Home, Connected, Help, Exit).
    """

    def __init__(self):
        # use unified handler (DongleSTMHandler)
        self.handler = DongleSTMHandler(self, None)
        print("[DBG] DongleInterfaceInit: created self.handler (DongleSTMHandler)")

        self.window = QWidget()
        self.window.setWindowTitle("STM32DongleLock")
        self.window.setWindowIcon(Icon.get_icon())
        self.window.setMinimumSize(560, 360)
        self._apply_styles()

        self.layout = QVBoxLayout(self.window)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Banner Layout 
        banner_layout = QHBoxLayout()
        banner_layout.setContentsMargins(12, 8, 12, 8)
        banner_layout.setSpacing(8)

        banner_icon = QLabel()
        banner_icon.setPixmap(
            QPixmap(
                "C:/Users/xolisile/OneDrive - University of Cape Town/EEE3095S/EEE3095S PROJECT/assets/STM_DONGLE_LOCKER.png"
            ).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        banner_text = QLabel()
        banner_text.setText(
            "<span style='color:#00AEEF; font-family:Segoe UI; font-size:11pt;'>"
            "<b>STM</b>32 <b>Dongle</b>Locker"
            "</span>"
        )
        banner_text.setAlignment(Qt.AlignVCenter)

        banner_layout.addWidget(banner_icon)
        banner_layout.addWidget(banner_text)
        banner_layout.addStretch()

        banner_container = QWidget()
        banner_container.setLayout(banner_layout)
        banner_container.setStyleSheet("background-color: white;")
        self.layout.addWidget(banner_container)

        # Central Widget 
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addWidget(self.central_widget, stretch=1)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # initial screen
        self.setup_home_interface()

    def _apply_styles(self):
        self.window.setStyleSheet(ThemeUI.get_stylesheet())

    def clear_central(self):
        """Removes all widgets from the central area."""
        while self.central_layout.count():
            item = self.central_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def setup_home_interface(self):
        self.clear_central()
        screen = HomeInterface(self.handler)
        screen.build()
        self.central_layout.addWidget(screen)

    def setup_connected_interface(self):
        self.clear_central()
        screen = ConnectedInterface(self.handler)
        screen.build()
        self.central_layout.addWidget(screen)

    def setup_help_interface(self):
        self.clear_central()
        screen = HelpInterface(self.handler)
        screen.build()
        self.central_layout.addWidget(screen)

    def setup_stm_interface(self):
        self.clear_central()
        screen = DongleSTMInterface(self.handler)
        self.central_layout.addWidget(screen)

    def show(self):
        self.window.show()
