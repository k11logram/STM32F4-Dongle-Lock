# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 06/10/2025
# Project: EEE3095S Project
# Class Description: Window Icon.

import os
from PyQt5.QtGui import QIcon

class Icon:
    ICON_PATH = r"C:\Users\xolisile\OneDrive - University of Cape Town\EEE3095S\EEE3095S PROJECT\assets\STM_DONGLE_LOCKER.png"

    @staticmethod
    def get_icon():
        if not os.path.exists(Icon.ICON_PATH):
            print(f"[WARNING] Icon not found: {Icon.ICON_PATH}")
        return QIcon(Icon.ICON_PATH)

