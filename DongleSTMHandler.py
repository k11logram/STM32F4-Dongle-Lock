# Authors: Buqwana Xolisile and Kagiso Dube 
# Version: 23/10/2025
# Project: EEE3095S Project
# Class Description: Unified handler for GUI, STM communication, and UI logging (Real Version).

import time
import serial
import pyperclip
import serial.tools.list_ports
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QTimer, QDateTime

from DongleInputPopup import DongleInputPopup
from CodeSelectPopup import CodeSelectPopup
from PopupBase import PopupBase
from ExitPopup import ExitPopup


class DongleSTMHandler:
    """Handles STM communication, GUI switching, clipboard operations, and logging."""

    def __init__(self, gui, log_panel):
        self.gui = gui
        self.log_panel = log_panel
        self.codes = {}
        self.ser = None
        self.is_connected = False
        self.port = "COM7"
        self.baud = 115200

        print(f"[DBG] DongleSTMHandler.__init__ called: log_panel is {'set' if log_panel else 'None'}")

    # GUI NAVIGATION 
    def show_first_interface(self):
        self.gui.setup_home_interface()

    def show_second_interface(self):
        self.gui.setup_connected_interface()

    def show_help(self):
        self.gui.setup_help_interface()

    def confirm_and_exit(self):
        ExitPopup(self.gui.window)

    # STM CONNECTION LOGIC 
    def attempt_connect(self):
        """Auto-scan and connect to STM32 dongle safely."""
        ports = serial.tools.list_ports.comports()
        available = [p.device for p in ports]
        print(f"[DEBUG] Available ports: {available}")

        if not available:
            print("\033[91m[Error] No COM ports found.\033[0m")  # Red text
            self._show_popup(
                "Connection Failed",
                '<span style="color:red;">Device Not Found.</span>'
            )
            return False

        self.port = available[0]
        print(f"[DEBUG] Trying port: {self.port}")

        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(1.5)
            print(f"[DEBUG] Serial port {self.port} opened.")

            self.ser.write(b'CONNECT\n')
            response = self.ser.readline().decode().strip()
            print(f"[DEBUG] Handshake response: {response}")

            if response == "OK":
                self.is_connected = True
                print("\033[92m[Connected] STM Dongle connection established successfully.\033[0m")
                self._show_popup(
                    "Connected",
                    '<span style="color:green;">STM Dongle connected successfully.</span>'
                )
                QTimer.singleShot(500, self.gui.setup_stm_interface)
                return True
            else:
                print(f"\033[91m[Error] Unexpected STM response: {response}\033[0m")
                self._show_popup(
                    "Connection Failed",
                    '<span style="color:red;">Unexpected STM response.<br>'
                    'Please try again.</span>'
                )
                self.ser.close()
                return False

        except Exception as e:
            print(f"\033[91m[Error] Could not connect to STM: {e}\033[0m")
            self._show_popup(
                "Connection Failed",
                f'<span style="color:red;">Could not connect to STM.<br><br>Details: {e}</span>'
            )
            return False


    def disconnect_stm(self):
        """Disconnect from STM32 and return to home interface."""
        if self.ser and self.ser.is_open:
            try:
                print("\033[94m[Disconnecting] Disconnecting from STM...\033[0m")
                self.ser.write(b"DISCONNECT\n")

                time.sleep(0.3)
                response = self.ser.readline().decode().strip()
                if response:
                    print(response)  

                self.ser.close()
                print("\033[92m[Disconnected] STM Dongle disconnected successfully.\033[0m")

            except Exception as e:
                print(f"\033[91m[Error] Disconnect failed: {e}\033[0m")

        else:
            print("\033[91m[Error] No active STM connection to disconnect.\033[0m")

        self.is_connected = False
        self.log_event("[Disconnected] STM Dongle disconnected successfully.")
        QTimer.singleShot(700, self.gui.setup_home_interface)


    # CODE MANAGEMENT 
    def handle_code_request(self, code_id: int):
        """Retrieve a stored code from STM."""
        self.log_event(f"[Get Code {code_id}] Checking STM storage...")

        if self.is_connected and self.ser:
            cmd = f"GET_CODE_{code_id}"
            try:
                self.ser.write((cmd + "\r\n").encode())
                time.sleep(0.2)
                resp = self.ser.readline().decode().strip()
                print(f"[DEBUG] STM replied to {cmd}: {resp}")
                self.log_event(f"[DEBUG] STM replied to {cmd}: {resp}")

                if resp and "CODE_" in resp:
                    parts = resp.split(":")
                    if len(parts) == 2:
                        self.codes[code_id] = parts[1]
                        pyperclip.copy(parts[1])
                        self._show_popup("Code Retrieved", f"Code {code_id}: {parts[1]}")
                        self.log_event(f"[Retrieved] Code {code_id}: {parts[1]}")
            except Exception as e:
                self.log_event(f"[Error] Could not read STM: {e}")
        else:
            self.log_event("[Error] STM not connected.")
    
    def handle_set_code(self, code_id: int):
        """Prompt user to enter and send a real code value to the STM."""
        self.log_event(f"[Set Code {code_id}] Prompting user for input...")

        popup = DongleInputPopup(code_id, self, parent=self.gui.window)
        if popup.exec_() == QDialog.Accepted:
            code_value = popup.input_field.text().strip()
            if not code_value:
                self._show_popup("Invalid Input", "Code value cannot be empty.")
                self.log_event(f"[Error] Empty code entered for Code {code_id}.")
                return

            # Save locally and log
            self.codes[code_id] = code_value
            pyperclip.copy(code_value)

            # Send to STM
            if self.is_connected and self.ser:
                try:
                    cmd = f"SET_CODE_{code_id}:{code_value}"
                    self.ser.write((cmd + "\r\n").encode())
                    time.sleep(0.2)
                    resp = self.ser.readline().decode().strip()
                    self.log_event(f"[DEBUG] STM replied to SET_CODE_{code_id}: {resp}")

                except Exception as e:
                    self.log_event(f"[Error] Could not send to STM: {e}")
            else:
                self.log_event("[Error] STM not connected.")
        else:
            self.log_event(f"[Set Code {code_id}] User cancelled input.")

    def save_new_code(self, code_id: int, code_value: str):
        """Save new code and send it to STM."""
        self.codes[code_id] = code_value
        pyperclip.copy(code_value)
        self._show_popup("Code Saved", f"Code {code_id} stored and copied to clipboard.")
        self.log_event(f"[Code Saved] Stored new value for Code {code_id}.")
  
        if self.is_connected and self.ser:
            try:
                cmd = f"SET_CODE_{code_id}:{code_value}"
                self.ser.write((cmd + "\r\n").encode())
                time.sleep(0.2)
                resp = self.ser.readline().decode().strip()
            except Exception as e:
                self.log_event(f"[Error] Could not verify STM: {e}")

    def handle_exit(self):
        pyperclip.copy("")
        self.log_event("[Exit] Sent DISCONNECT to STM, clearing clipboard and returning home.")
        self._show_popup("Disconnected", "STM Dongle disconnected.")
        self.disconnect_stm()
    
    def handle_edit_code(self):
        """Edit existing code."""
        if not self.codes:
            self._show_popup("Something went wrong", "No codes available to edit.")
            self.log_event("[Edit Code] Attempted to edit but no codes stored.")
            return

        popup = CodeSelectPopup("Edit Code", "Enter code number (1–3):", self.gui.window)
        if popup.exec_() == QDialog.Accepted:
            code_id = popup.code_id
            if code_id not in self.codes:
                self._show_popup("Not Found", f"Code {code_id} not yet stored.")
                self.log_event(f"[Edit Code] Code {code_id} not found for editing.")
                return

            self.log_event(f"[Edit Code] Editing Code {code_id}.")
            edit_popup = DongleInputPopup(code_id, self)
            edit_popup.exec_()
        else:
            self.log_event("[Edit Code] User cancelled selection.")

    def handle_clear_code(self):
        """Clear existing stored code."""
        if not self.codes:
            self._show_popup("Something went wrong", "No codes to clear.")
            self.log_event("[Clear Code] No codes found to clear.")
            return

        popup = CodeSelectPopup("Clear Code", "Enter code number to clear (1–3):", self.gui.window)
        if popup.exec_() == QDialog.Accepted:
            code_id = popup.code_id
            if code_id not in self.codes:
                self._show_popup("Not Found", f"Code {code_id} not stored.")
                self.log_event(f"[Clear Code] Tried to clear Code {code_id}, but it doesn't exist.")
                return

            del self.codes[code_id]
            self._show_popup("Code Cleared", f"Code {code_id} has been cleared.")
            self.log_event(f"[Clear Code] Code {code_id} cleared successfully.")
        else:
            self.log_event("[Clear Code] User cancelled clear operation.")


    # LOGGING 
    def log_event(self, message: str):
        """Appends log message with timestamp to the log panel."""
        if not self.log_panel:
            print(message)
            return

        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        color = "#003344"
        if "[Error]" in message:
            color = "#E63946"
        elif any(w in message for w in ["Saved", "Retrieved", "Connected", "Cleared"]):
            color = "#007F00"
        elif any(w in message for w in ["Edit", "Get", "User"]):
            color = "#0077B6"

        html_line = (
            f'<span style="color:gray;">[{timestamp}]</span> '
            f'<span style="color:{color};">{message}</span><br>'
        )
        self.log_panel.moveCursor(QTextCursor.End)
        self.log_panel.insertHtml(html_line)
        self.log_panel.moveCursor(QTextCursor.End)

    # UTILITIES 
    def get_com_status(self) -> str:
        """Return current COM port settings (live)."""
        try:
            if self.ser and self.ser.is_open:
                return (
                    f"Baud: {self.ser.baudrate}\n"
                    f"Parity: {self.ser.parity}\n"
                    f"Data Bits: {self.ser.bytesize}\n"
                    f"Stop Bits: {self.ser.stopbits}\n"
                    f"Timeout: {self.ser.timeout}\n"
                    f"XON/XOFF: {self.ser.xonxoff}\n"
                    f"CTS Handshake: {self.ser.rtscts}\n"
                    f"DSR Handshake: {self.ser.dsrdtr}"
                )
            else:
                return (
                    f"Baud: {self.baud}\n"
                    f"Parity: None\n"
                    f"Data Bits: 8\n"
                    f"Stop Bits: 1\n"
                    f"Timeout: OFF\n"
                    f"XON/XOFF: --\n"
                    f"CTS Handshake: --\n"
                    f"DSR Handshake: --"
                )
        except Exception as e:
            return f"[Error] Could not read COM port info: {e}"


    def _show_popup(self, title, message):
        popup = PopupBase(title, message, parent=self.gui.window)
        popup.exec_()
