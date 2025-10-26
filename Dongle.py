# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 06/10/2025
# Project: EEE3035S Project
# Class Description: Creates DongleInterfaceInit object which initializes the GUI.

import sys
from PyQt5.QtWidgets import QApplication  # imports QApplication

from DongleInterfaceInit import DongleInterfaceInit  # import your main GUI container
from Icon import Icon

class Dongle:
    @staticmethod
    def init():
        app = QApplication(sys.argv)
        app.setWindowIcon(Icon.get_icon())
        main_GUI = DongleInterfaceInit()  
        print("[DBG] Dongle: initialized main container (DongleInterfaceInit)")
        main_GUI.show()
        sys.exit(app.exec_())
        
def main():
    Dongle.init()
main()

