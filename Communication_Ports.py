"""This is the file that will work on the ports communication for the project
We will use this file to handle all the communication ports related tasks
We want to utilize UART, SPI, and I2C protocols for communication
So our main focus will be on implementing these protocols efficiently
The frontend will call the functions from this file to perform communication tasks and list available ports"""
import serial # this is for serial communication
import time # this is for making delays


class CommunicationPorts:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        # a baudrate is a measure of how fast data is sent over a communication channel
        self.baudrate = baudrate # default baudrate and the baudrate can be changed later
        self.timeout = timeout # timeout for the communication
        self.connection = None # this will hold the serial connection object

    def open_connection(self):
        """Open a serial connection with the specified port and baudrate"""
        try:
            # establish a serial connection and set the timeout
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # wait for the connection to establish
            print(f"Connection opened on {self.port} at {self.baudrate} baudrate.") # confirm the connection is opened
        except serial.SerialException as e:
            print(f"Error opening connection: {e}") # handle exceptions if the port cannot be opened

    def close_connection(self):
        # Close the serial connection
        if self.connection and self.connection.is_open:
            self.connection.close()
            print(f"Connection on {self.port} closed.")

    def send_data(self, data):
        if self.connection and self.connection.is_open:
            self.connection.write(data.encode())
            print(f"Sent data: {data}")
        else:
            print("Connection is not open. Cannot send data.")

    def receive_data(self):
        if self.connection and self.connection.is_open:
            data = self.connection.readline().decode().strip()
            print(f"Received data: {data}")
            return data
        else:
            print("Connection is not open. Cannot receive data.")
            return None