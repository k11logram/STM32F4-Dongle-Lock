# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 06/10/2025
# Project: EEE3095S Project
# Class Description: Parent class in which all interfaces inherit from.

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ThemeUI import ThemeUI
from Icon import Icon

class BaseInterface(QWidget):
    """Base class for all GUI."""
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(ThemeUI.get_stylesheet())
        self.setWindowIcon(Icon.get_icon())
        self.setStyleSheet(ThemeUI.get_stylesheet())

    def build(self):
        """Each child interface implements this."""
        raise NotImplementedError("Each interface must implement build().")
