"""
Dongle Lock GUI Application - Integrated Version
EEE3095S Embedded Systems II Project
Authors: Dube Kagiso and Xolisile Buqwana
Date: 14 October 2025
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QInputDialog, QMessageBox, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

# Import our custom modules
from Communication_Ports import CommunicationPorts
from Protocol_Handler import ProtocolHandler


class ModernButton(QPushButton):
    """Custom styled button with hover effects"""
    def __init__(self, text, color="#4F46E5"):
        super().__init__(text)
        self.color = color
        self.setMinimumHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.update_style()
        
    def update_style(self, hover=False):
        """Update button style"""
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
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)


class StatusLabel(QLabel):
    """Animated status label with color coding"""
    def __init__(self, text=""):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(40)
        self.setStyleSheet("""
            QLabel {
                background: #F3F4F6;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                color: #6B7280;
            }
        """)
        
    def set_status(self, text, status_type="info"):
        """Set status with color coding"""
        colors = {
            "success": "#10B981",
            "error": "#EF4444",
            "warning": "#F59E0B",
            "info": "#3B82F6"
        }
        self.setText(text)
        color = colors.get(status_type, colors["info"])
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
        self.comm_port = None  # CommunicationPorts instance
        self.is_connected = False
        self.protocol = ProtocolHandler()  # Protocol handler
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
        
        # Status bar (create BEFORE connection section)
        self.status_label = StatusLabel("Ready to connect")
        main_layout.addWidget(self.status_label)
        
        # Connection section
        self.connection_frame = self.create_connection_section()
        main_layout.addWidget(self.connection_frame)
        
        # Main controls section (initially hidden)
        self.controls_frame = self.create_controls_section()
        self.controls_frame.hide()
        main_layout.addWidget(self.controls_frame)
        
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
        ports = CommunicationPorts.list_available_ports()
        
        for port_device, port_desc in ports:
            self.port_combo.addItem(f"{port_device} - {port_desc}", port_device)
        
        if self.port_combo.count() == 0:
            self.port_combo.addItem("No COM ports found", None)
            # Only update status label if it exists
            if hasattr(self, 'status_label'):
                self.status_label.set_status("⚠ No COM ports detected", "warning")
        else:
            # Only update status label if it exists
            if hasattr(self, 'status_label'):
                self.status_label.set_status(f"Found {len(ports)} COM port(s)", "info")
            
    def connect_dongle(self):
        """Connect to the STM dongle"""
        port = self.port_combo.currentData()
        
        if port is None:
            self.status_label.set_status("⚠ No COM port selected", "error")
            QMessageBox.warning(self, "No Port", "Please select a valid COM port")
            return
        
        self.status_label.set_status("Connecting...", "info")
        QApplication.processEvents()  # Update UI
        
        try:
            # Create communication port instance
            self.comm_port = CommunicationPorts(port=port, baudrate=115200, timeout=2.0)
            
            # Open connection
            if not self.comm_port.open_connection():
                raise Exception("Failed to open serial port")
            
            # Send CONNECT message using protocol handler
            connect_msg = self.protocol.create_connect_message()
            response = self.comm_port.send_command(connect_msg, wait_response=True)
            
            # Check response
            if response and self.protocol.is_ok_response(response):
                self.is_connected = True
                self.status_label.set_status("✓ Connected successfully!", "success")
                
                # Hide connection section, show controls
                self.connection_frame.hide()
                self.controls_frame.show()
                
            else:
                raise Exception(f"Invalid response from dongle: {response}")
                
        except Exception as e:
            self.status_label.set_status(f"✗ Connection failed: {str(e)}", "error")
            QMessageBox.critical(self, "Connection Error", 
                               f"Device Not Found\n\n{str(e)}\n\nPlease check:\n"
                               f"- STM board is powered on\n"
                               f"- Correct COM port is selected\n"
                               f"- STM firmware is running")
            if self.comm_port:
                self.comm_port.close_connection()
                self.comm_port = None
                
    def get_code(self, code_num):
        """Get code from dongle"""
        if not self.is_connected or not self.comm_port:
            self.status_label.set_status("✗ Not connected to dongle", "error")
            return
        
        # Validate code number
        if not self.protocol.validate_code_number(code_num):
            self.status_label.set_status(f"✗ Invalid code number: {code_num}", "error")
            return
        
        try:
            # Send GET_CODE_N message
            get_msg = self.protocol.create_get_code_message(code_num)
            response = self.comm_port.send_command(get_msg, wait_response=True)
            
            if not response:
                self.status_label.set_status("✗ No response from dongle", "error")
                return
            
            # Check if code slot is empty
            if self.protocol.is_empty_response(response):
                # Code doesn't exist, prompt for new code
                code, ok = QInputDialog.getText(
                    self, 
                    f"Set Code {code_num}", 
                    f"Code slot {code_num} is empty.\nEnter new access code:",
                    text=""
                )
                
                if ok and code:
                    # Validate code
                    is_valid, error_msg = self.protocol.validate_code_value(code)
                    if not is_valid:
                        self.status_label.set_status(f"✗ Invalid code: {error_msg}", "error")
                        QMessageBox.warning(self, "Invalid Code", error_msg)
                        return
                    
                    # Send SET_CODE_N message
                    set_msg = self.protocol.create_set_code_message(code_num, code)
                    confirm = self.comm_port.send_command(set_msg, wait_response=True)
                    
                    if confirm and self.protocol.is_saved_response(confirm):
                        # Copy to clipboard
                        clipboard = QApplication.clipboard()
                        clipboard.setText(code)
                        self.status_label.set_status(
                            f"✓ Code {code_num} saved and copied to clipboard", 
                            "success"
                        )
                    else:
                        self.status_label.set_status(
                            f"✗ Failed to save code: {confirm}", 
                            "error"
                        )
                else:
                    self.status_label.set_status("Operation cancelled", "info")
                    
            elif self.protocol.is_code_response(response):
                # Code exists, extract and copy to clipboard
                code = self.protocol.extract_code_from_response(response)
                
                if code:
                    clipboard = QApplication.clipboard()
                    clipboard.setText(code)
                    self.status_label.set_status(
                        f"✓ Code {code_num} copied to clipboard", 
                        "success"
                    )
                    
                    # Show preview of code (first 3 chars + ***)
                    preview = code[:3] + "***" if len(code) > 3 else code
                    QMessageBox.information(
                        self, 
                        f"Code {code_num} Retrieved", 
                        f"Code preview: {preview}\n\n"
                        f"Full code has been copied to clipboard."
                    )
                else:
                    self.status_label.set_status("✗ Failed to extract code", "error")
                    
            else:
                self.status_label.set_status(
                    f"✗ Unexpected response: {response}", 
                    "error"
                )
                
        except Exception as e:
            self.status_label.set_status(f"✗ Error: {str(e)}", "error")
            QMessageBox.critical(self, "Communication Error", str(e))
            
    def disconnect_dongle(self):
        """Disconnect from dongle and exit"""
        if self.is_connected and self.comm_port:
            try:
                # Send DISCONNECT message
                disconnect_msg = self.protocol.create_disconnect_message()
                self.comm_port.send_command(disconnect_msg, wait_response=False)
                
                # Close connection
                self.comm_port.close_connection()
                self.is_connected = False
                
            except Exception as e:
                print(f"Error during disconnect: {e}")
        
        # Clear clipboard for security
        clipboard = QApplication.clipboard()
        clipboard.clear()
        
        # Close application
        self.close()
        
    def closeEvent(self, event):
        """Handle window close event"""
        if self.is_connected:
            # Send disconnect message
            try:
                if self.comm_port:
                    disconnect_msg = self.protocol.create_disconnect_message()
                    self.comm_port.send_command(disconnect_msg, wait_response=False)
                    self.comm_port.close_connection()
            except:
                pass
            
            # Clear clipboard
            clipboard = QApplication.clipboard()
            clipboard.clear()
        
        event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont("Segoe UI", 10))
    
    # Set application metadata
    app.setApplicationName("Dongle Lock Manager")
    app.setOrganizationName("UCT EEE3095S")
    
    # Create and show main window
    window = DongleLockGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()