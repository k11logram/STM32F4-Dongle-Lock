#Dube Kagiso and Xolisile Buqwana
# 14 October 2025

"""
Dongle Lock GUI Application
EEE3095S Embedded Systems II Project
"""

import sys  # this is needed for PyQt5 because it handles system args
import serial # i added this for serial communication
import serial.tools # this is needed to list available COM ports
import serial.tools.list_ports # to list the available COM ports
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QInputDialog, QMessageBox, QFrame, QGraphicsDropShadowEffect) # for my gui components
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect # for core Qt functionality
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QLinearGradient, QPainter, QPen # for styling and graphics

class ModernButton(QPushButton):
    """Custom styled button with hover effects"""
    def __init__(self, text, color="#4F46E5"):
        super().__init__(text) # Initialize parent class
        self.color = color # Button color
        self.setMinimumHeight(50)
        self.setCursor(Qt.PointingHandCursor) # Change cursor on hover
        self.update_style()
        
    def update_style(self, hover=False):
        """Update button style"""
        if hover:
            style = f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 {self.color}, stop:1 #6366F1);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: bold;
                    transform: scale(1.05);
                }}
            """
        else:
            style = f"""
                QPushButton {{
                    background: {self.color};
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 {self.color}, stop:1 #6366F1);
                }}
                QPushButton:pressed {{
                    background: #3730A3;
                }}
                QPushButton:disabled {{
                    background: #9CA3AF;
                }}
            """
        self.setStyleSheet(style) 
        
        # Add shadow effect
        # we adding this to give the button a slight 3D effect for fun and aesthetics
        shadow = QGraphicsDropShadowEffect() 
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60)) # subtle shadow
        shadow.setOffset(0, 4) # shadow position
        self.setGraphicsEffect(shadow) # apply shadow effect

class StatusLabel(QLabel):
    """Animated status label"""
    def __init__(self, text=""):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter) # center text
        self.setMinimumHeight(40) # minimum height of the label
        self.setStyleSheet("""
            QLabel {
                background: #F3F4F6;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                color: #6B7280;
            }
        """) # default style
        
    def set_status(self, text, status_type="info"):
        """Set status with color coding"""
        colors = {
            "success":"#10B981",
            "error": "#EF4444",
            "warning": "#F59E0B",
            "info": "#3B82F6"
        } # this was meant for color coding the status messages
        self.setText(text) # update text
        color = colors.get(status_type, colors["info"]) # get color based on status type
        self.setStyleSheet(f"""
            QLabel {{
                background: {color}22;
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 13px;
                color: {color};
                font-weight: 600;
            }}
        """)

class DongleLockGUI(QMainWindow):
    """Main GUI Application for Dongle Lock System"""
    
    def __init__(self):
        super().__init__()
        self.serial_connection = None
        self.is_connected = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🔐 Dongle Lock Manager")
        self.setMinimumSize(600, 700)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #F9FAFB, stop:1 #E5E7EB);
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Connection section
        self.connection_frame = self.create_connection_section()
        main_layout.addWidget(self.connection_frame)
        
        # Main controls section (initially hidden)
        self.controls_frame = self.create_controls_section()
        self.controls_frame.hide()
        main_layout.addWidget(self.controls_frame)
        
        # Status bar
        self.status_label = StatusLabel("Ready to connect")
        main_layout.addWidget(self.status_label)
        
        main_layout.addStretch()
        
    def create_header(self):
        """Create the header section"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        header_frame.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(header_frame)
        
        # Title
        title = QLabel("🔐 Dongle Lock Manager")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #1F2937; margin: 0;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Secure Access Code Storage System")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #6B7280; margin-top: 5px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        return header_frame
        
    def create_connection_section(self):
        """Create the connection section"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                padding: 30px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        frame.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        
        # Section title
        title = QLabel("Connection Settings")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1F2937;")
        layout.addWidget(title)
        
        # COM Port selection
        port_layout = QHBoxLayout()
        port_label = QLabel("Select COM Port:")
        port_label.setStyleSheet("color: #4B5563; font-size: 13px; font-weight: 600;")
        port_layout.addWidget(port_label)
        
        self.port_combo = QComboBox()
        self.port_combo.setMinimumHeight(40)
        self.port_combo.setStyleSheet("""
            QComboBox {
                background: #F9FAFB;
                border: 2px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: #1F2937;
            }
            QComboBox:hover {
                border-color: #4F46E5;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6B7280;
                margin-right: 10px;
            }
        """)
        self.refresh_ports()
        port_layout.addWidget(self.port_combo, 1)
        
        refresh_btn = QPushButton("↻")
        refresh_btn.setMaximumWidth(45)
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: #4F46E5;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4338CA;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_ports)
        port_layout.addWidget(refresh_btn)
        
        layout.addLayout(port_layout)
        
        # Connect button
        self.connect_btn = ModernButton("Connect to Dongle", "#4F46E5")
        self.connect_btn.clicked.connect(self.connect_dongle)
        layout.addWidget(self.connect_btn)
        
        return frame
        
    def create_controls_section(self):
        """Create the main controls section"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 16px;
                padding: 30px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        frame.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        
        # Section title
        title = QLabel("Access Code Management")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1F2937;")
        layout.addWidget(title)
        
        # Code buttons
        self.code_buttons = []
        colors = ["#4F46E5", "#7C3AED", "#DB2777"]
        
        for i in range(3):
            btn = ModernButton(f"🔑 Get Code {i+1}", colors[i])
            btn.clicked.connect(lambda checked, idx=i+1: self.get_code(idx))
            layout.addWidget(btn)
            self.code_buttons.append(btn)
        
        # Disconnect button
        layout.addSpacing(20)
        self.disconnect_btn = ModernButton("Disconnect & Exit", "#DC2626")
        self.disconnect_btn.clicked.connect(self.disconnect_dongle)
        layout.addWidget(self.disconnect_btn)
        
        return frame
        
    def refresh_ports(self):
        """Refresh available COM ports"""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}", port.device)
        
        if self.port_combo.count() == 0:
            self.port_combo.addItem("No COM ports found", None)
            
    def connect_dongle(self):
        """Connect to the STM dongle"""
        port = self.port_combo.currentData()
        
        if port is None:
            self.status_label.set_status("⚠ No COM port selected", "error")
            return
            
        try:
            # Open serial connection
            self.serial_connection = serial.Serial(
                port=port,
                baudrate=9600,
                timeout=2
            )
            
            # Send CONNECT message
            self.serial_connection.write(b"CONNECT\n")
            
            # Wait for OK response
            response = self.serial_connection.readline().decode().strip()
            
            if response == "OK":
                self.is_connected = True
                self.status_label.set_status("✓ Connected successfully!", "success")
                
                # Hide connection section, show controls
                self.connection_frame.hide()
                self.controls_frame.show()
                
            else:
                raise Exception("Invalid response from dongle")
                
        except Exception as e:
            self.status_label.set_status(f"✗ Connection failed: {str(e)}", "error")
            QMessageBox.critical(self, "Connection Error", 
                               f"Device Not Found\n\n{str(e)}")
            if self.serial_connection:
                self.serial_connection.close()
                self.serial_connection = None
                
    def get_code(self, code_num):
        """Get code from dongle"""
        if not self.is_connected:
            return
            
        try:
            # Send GET_CODE_N message
            self.serial_connection.write(f"GET_CODE_{code_num}\n".encode())
            
            # Wait for response
            response = self.serial_connection.readline().decode().strip()
            
            if response == "EMPTY":
                # Code doesn't exist, prompt for new code
                code, ok = QInputDialog.getText(
                    self, 
                    f"Set Code {code_num}", 
                    f"Enter new access code for slot {code_num}:",
                    text="password123"
                )
                
                if ok and code:
                    # Send SET_CODE_N message
                    self.serial_connection.write(f"SET_CODE_{code_num}:{code}\n".encode())
                    
                    # Wait for confirmation
                    confirm = self.serial_connection.readline().decode().strip()
                    
                    if confirm == "SAVED":
                        # Copy to clipboard
                        clipboard = QApplication.clipboard()
                        clipboard.setText(code)
                        self.status_label.set_status(f"✓ Code {code_num} saved and copied to clipboard", "success")
                    else:
                        self.status_label.set_status("✗ Failed to save code", "error")
                        
            elif response.startswith("CODE:"):
                # Code exists, extract and copy to clipboard
                code = response.split(":", 1)[1]
                clipboard = QApplication.clipboard()
                clipboard.setText(code)
                self.status_label.set_status(f"✓ Code {code_num} copied to clipboard", "success")
                
            else:
                self.status_label.set_status("✗ Unexpected response from dongle", "error")
                
        except Exception as e:
            self.status_label.set_status(f"✗ Error: {str(e)}", "error")
            
    def disconnect_dongle(self):
        """Disconnect from dongle and exit"""
        if self.is_connected and self.serial_connection:
            try:
                # Send DISCONNECT message
                self.serial_connection.write(b"DISCONNECT\n")
                self.serial_connection.close()
            except:
                pass
                
        # Clear clipboard
        clipboard = QApplication.clipboard()
        clipboard.clear()
        
        # Close application
        self.close()
        
    def closeEvent(self, event):
        """Handle window close event"""
        if self.is_connected:
            self.disconnect_dongle()
        event.accept()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont("Segoe UI", 10))
    
    # Create and show main window
    window = DongleLockGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()