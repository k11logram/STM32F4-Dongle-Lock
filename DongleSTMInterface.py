# Authors: Buqwana Xolisile and Kagiso Dube
# Version: 23/10/2025
# Project: EEE3095S Project
# Class Description: Displays Interface after successful STM connection.

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel,
    QSizePolicy, QTextEdit, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from BaseInterface import BaseInterface


class DongleSTMInterface(BaseInterface):
    """Interface displayed after successful STM connection, with COM and Target info."""

    def __init__(self, handler_parent):
        super().__init__(handler_parent)
        self.handler_parent = handler_parent
        self.handler = None
        self.build()

    def build(self):
        """Builds STM management interface with COM & Target info."""
        main_layout = QVBoxLayout()
        self.layout.addLayout(main_layout)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(10)

        # GRID LAYOUT (70/30)
        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(8)
        grid.setColumnStretch(0, 7)
        grid.setColumnStretch(1, 3)
        main_layout.addLayout(grid)

        # HEADINGS
        log_label = QLabel("Log")
        mem_label = QLabel("Memory & Code Editing")
        for lbl in (log_label, mem_label):
            lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
            lbl.setStyleSheet("color: white;")
        grid.addWidget(log_label, 0, 0)
        grid.addWidget(mem_label, 0, 1)

        # LEFT PANEL: LOG BOX
        left_box = QFrame()
        left_box.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #f2f2f2, stop:1 #e6e6e6);
                border-radius: 10px;
            }
        """)
        left_layout = QVBoxLayout(left_box)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(8)

        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        self.log_panel.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: none;
                border-radius: 6px;
                font-family: Consolas, monospace;
                font-size: 12px;
                color: #1a1a1a;
                padding: 8px;
            }
        """)
        left_layout.addWidget(self.log_panel)
        grid.addWidget(left_box, 1, 0)

        # RIGHT PANEL: MEMORY & CODE EDITING 
        right_box = QFrame()
        right_box.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #f2f2f2, stop:1 #e6e6e6);
                border-radius: 10px;
            }
        """)
        right_layout = QVBoxLayout(right_box)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)

        # MEMORY PANEL 
        mem_panel = QFrame()
        mem_panel.setStyleSheet("QFrame { background-color: #05244b; border-radius: 8px; }")
        mem_inner = QHBoxLayout(mem_panel)
        mem_inner.setContentsMargins(10, 10, 10, 10)
        mem_inner.setSpacing(12)

        get_col, set_col = QVBoxLayout(), QVBoxLayout()
        self.get1_btn = QPushButton("Get Code 1")
        self.get2_btn = QPushButton("Get Code 2")
        self.get3_btn = QPushButton("Get Code 3")
        self.set1_btn = QPushButton("Set Code 1")
        self.set2_btn = QPushButton("Set Code 2")
        self.set3_btn = QPushButton("Set Code 3")

        for b in (self.get1_btn, self.get2_btn, self.get3_btn):
            self._style_standard_button(b)
            get_col.addWidget(b)

        for b in (self.set1_btn, self.set2_btn, self.set3_btn):
            self._style_standard_button(b)
            set_col.addWidget(b)

        mem_inner.addLayout(set_col)
        mem_inner.addLayout(get_col)
        right_layout.addWidget(mem_panel)

        # EDIT/CLEAR PANEL 
        edit_panel = QFrame()
        edit_panel.setStyleSheet("QFrame { background-color: #05244b; border-radius: 8px; }")
        edit_inner = QHBoxLayout(edit_panel)
        edit_inner.setContentsMargins(10, 10, 10, 10)
        edit_inner.setSpacing(12)

        self.clear_btn = QPushButton("Clear Code")
        self.edit_btn = QPushButton("Edit Code")
        for b in (self.clear_btn, self.edit_btn):
            self._style_standard_button(b)
            edit_inner.addWidget(b)
        right_layout.addWidget(edit_panel)

        # COM PORT STATUS PANEL 
        com_panel = QFrame()
        com_panel.setStyleSheet("""
            QFrame { background-color: #001f3f; border-radius: 8px; }
            QLabel {
                color: #dee6f3;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        com_layout = QVBoxLayout(com_panel)
        com_layout.setContentsMargins(10, 8, 10, 8)
        com_layout.setSpacing(6)

        com_title = QLabel("COM Port Status")
        com_title.setStyleSheet("color: #7ec8ff; font-weight: 600; font-size: 13px;")
        com_layout.addWidget(com_title)

        com_grid = QGridLayout()
        com_grid.setSpacing(4)
        self.com_labels = []
        self.com_keys = [
            "Baud:", "Parity:", "Data Bits:", "Stop Bits:",
            "Timeout:", "XON/XOFF:", "CTS Handshake:", "DSR Handshake:"
        ]
        for i, key in enumerate(self.com_keys):
            row, col = i // 2, (i % 2) * 2
            key_lbl = QLabel(key)
            val_lbl = QLabel("--")
            key_lbl.setStyleSheet("color: #9fc4e3;")
            val_lbl.setStyleSheet("color: #ffffff; font-weight: 500;")
            com_grid.addWidget(key_lbl, row, col)
            com_grid.addWidget(val_lbl, row, col + 1)
            self.com_labels.append(val_lbl)

        com_layout.addLayout(com_grid)
        right_layout.addWidget(com_panel)

        # TARGET INFORMATION PANEL
        target_panel = QFrame()
        target_panel.setStyleSheet("""
            QFrame { background-color: #001f3f; border-radius: 8px; }
            QLabel {
                color: #dee6f3;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        target_layout = QVBoxLayout(target_panel)
        target_layout.setContentsMargins(10, 8, 10, 8)
        target_layout.setSpacing(6)

        target_title = QLabel("Target Information")
        target_title.setStyleSheet("color: #7ec8ff; font-weight: 600; font-size: 13px;")
        target_layout.addWidget(target_title)

        self.target_info_label = QLabel(
            "Board: --\nDevice: STM32F446xx\nType: MCU\n"
            "Device ID: 0x421\nCPU: Cortex-M4"
        )
        self.target_info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        target_layout.addWidget(self.target_info_label)
        right_layout.addWidget(target_panel)
        grid.addWidget(right_box, 1, 1)

        # DISCONNECT BUTTON 
        self.exit_btn = QPushButton("Disconnect")
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #c2c43f;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                padding: 8px 16px;
                min-height: 38px;
            }
            QPushButton:hover { background-color: #d0d246; }
            QPushButton:pressed { background-color: #a8aa36; }
        """)
        hl = QHBoxLayout()
        hl.addStretch()
        hl.addWidget(self.exit_btn)
        main_layout.addLayout(hl)

        # FIXED HANDLER CONNECTION
        self.handler = self.handler_parent  
        if self.handler.log_panel is None:
            self.handler.log_panel = self.log_panel

        # INITIAL LOG MESSAGE
        self.handler.log_event("[Connected] STM Dongle connection established successfully.")

        # BUTTON CONNECTIONS 
        self.get1_btn.clicked.connect(lambda: self.handler.handle_code_request(1))
        self.get2_btn.clicked.connect(lambda: self.handler.handle_code_request(2))
        self.get3_btn.clicked.connect(lambda: self.handler.handle_code_request(3))
        self.set1_btn.clicked.connect(lambda: self.handler.handle_set_code(1))
        self.set2_btn.clicked.connect(lambda: self.handler.handle_set_code(2))
        self.set3_btn.clicked.connect(lambda: self.handler.handle_set_code(3))
        self.clear_btn.clicked.connect(self.handler.handle_clear_code)
        self.edit_btn.clicked.connect(self.handler.handle_edit_code)
        self.exit_btn.clicked.connect(self.handler.handle_exit)

        # COM INFO REFRESH 
        self.update_com_info()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_com_info)
        self.timer.start(2000)

    # BUTTON STYLE HELPER 
    def _style_standard_button(self, btn: QPushButton):
        btn.setMinimumHeight(36)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1184d5;
                color: #dee4e7;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #1a9ee9; }
            QPushButton:pressed { background-color: #0f6bab; }
        """)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    # LIVE COM INFO REFRESH 
    def update_com_info(self):
        """Updates the COM status panel dynamically."""
        status = self.handler.get_com_status().split("\n")
        for i, line in enumerate(status[:len(self.com_labels)]):
            parts = line.split(":", 1)
            if len(parts) == 2:
                self.com_labels[i].setText(parts[1].strip())
