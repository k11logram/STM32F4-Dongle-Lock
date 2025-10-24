"""
Communication Ports Module
Handles serial communication with the STM Dongle
Authors: Dube Kagiso and Xolisile Buqwana
Date: 14 October 2025
"""

import serial
import serial.tools.list_ports
import time
from typing import Optional, List, Tuple

class CommunicationPorts:
    """Handles serial communication with STM dongle using UART protocol"""
    
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 2.0):
        """
        Initialize communication port parameters
        
        Args:
            port: COM port name (e.g., 'COM3', '/dev/ttyUSB0')
            baudrate: Communication speed in bits per second (default: 115200)
            timeout: Read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection: Optional[serial.Serial] = None
        
    def open_connection(self) -> bool:
        """
        Open a serial connection with the specified port and baudrate
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            time.sleep(0.5)  # Wait for connection to stabilize
            print(f"✓ Connection opened on {self.port} at {self.baudrate} baudrate")
            return True
            
        except serial.SerialException as e:
            print(f"✗ Error opening connection on {self.port}: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False
    
    def close_connection(self) -> None:
        """Close the serial connection"""
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
                print(f"✓ Connection on {self.port} closed")
            except Exception as e:
                print(f"✗ Error closing connection: {e}")
            finally:
                self.connection = None
    
    def send_data(self, data: str) -> bool:
        """
        Send data through the serial connection
        
        Args:
            data: String data to send
            
        Returns:
            bool: True if send successful, False otherwise
        """
        if not self.is_connected():
            print("✗ Connection is not open. Cannot send data")
            return False
            
        try:
            # Ensure data ends with newline for proper message framing
            if not data.endswith('\n'):
                data += '\n'
                
            self.connection.write(data.encode('utf-8'))
            self.connection.flush()  # Ensure data is sent immediately
            print(f"→ Sent: {data.strip()}")
            return True
            
        except serial.SerialException as e:
            print(f"✗ Error sending data: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error while sending: {e}")
            return False
    
    def receive_data(self, timeout_override: Optional[float] = None) -> Optional[str]:
        """
        Receive data from the serial connection
        
        Args:
            timeout_override: Optional custom timeout for this read operation
            
        Returns:
            str: Received data or None if error/timeout
        """
        if not self.is_connected():
            print("✗ Connection is not open. Cannot receive data")
            return None
            
        try:
            # Temporarily override timeout if specified
            original_timeout = self.connection.timeout
            if timeout_override is not None:
                self.connection.timeout = timeout_override
            
            # Read until newline or timeout
            data = self.connection.readline().decode('utf-8').strip()
            
            # Restore original timeout
            if timeout_override is not None:
                self.connection.timeout = original_timeout
            
            if data:
                print(f"← Received: {data}")
                return data
            else:
                print("⚠ No data received (timeout)")
                return None
                
        except serial.SerialException as e:
            print(f"✗ Error receiving data: {e}")
            return None
        except UnicodeDecodeError as e:
            print(f"✗ Error decoding received data: {e}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error while receiving: {e}")
            return None
    
    def send_command(self, command: str, wait_response: bool = True) -> Optional[str]:
        """
        Send a command and optionally wait for response
        
        Args:
            command: Command string to send
            wait_response: Whether to wait for a response
            
        Returns:
            str: Response data if wait_response=True, None otherwise
        """
        if self.send_data(command):
            if wait_response:
                return self.receive_data()
            return ""
        return None
    
    def is_connected(self) -> bool:
        """
        Check if the serial connection is open and valid
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self.connection is not None and self.connection.is_open
    
    def flush_buffers(self) -> None:
        """Flush input and output buffers"""
        if self.is_connected():
            try:
                self.connection.reset_input_buffer()
                self.connection.reset_output_buffer()
                print("✓ Buffers flushed")
            except Exception as e:
                print(f"✗ Error flushing buffers: {e}")
    
    @staticmethod
    def list_available_ports() -> List[Tuple[str, str]]:
        """
        List all available COM ports on the system
        
        Returns:
            List of tuples: (port_name, port_description)
        """
        ports = serial.tools.list_ports.comports()
        available_ports = []
        
        for port in ports:
            available_ports.append((port.device, port.description))
            print(f"Found port: {port.device} - {port.description}")
        
        if not available_ports:
            print("⚠ No COM ports found")
        
        return available_ports
    
    def __enter__(self):
        """Context manager entry"""
        self.open_connection()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_connection()
        return False


# Example usage and testing
if __name__ == "__main__":
    print("=== Communication Ports Test ===\n")
    
    # List available ports
    print("Available COM Ports:")
    ports = CommunicationPorts.list_available_ports()
    print()
    
    # Example: Connect to first available port
    if ports:
        test_port = ports[0][0]
        print(f"Testing connection to {test_port}...\n")
        
        # Using context manager (automatically closes connection)
        with CommunicationPorts(test_port, baudrate=115200) as comm:
            if comm.is_connected():
                # Test sending CONNECT message
                response = comm.send_command("CONNECT")
                print(f"Response to CONNECT: {response}\n")
                
                # Test sending GET_CODE_1 message
                response = comm.send_command("GET_CODE_1")
                print(f"Response to GET_CODE_1: {response}\n")
    else:
        print("No ports available for testing")