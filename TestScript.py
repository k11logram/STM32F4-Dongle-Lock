import serial
import time

ser = serial.Serial('COM7', 115200, timeout=1)
time.sleep(2)


ser.write(b'CONNECT\n')
print("Sent: CONNECT")
response = ser.readline().decode().strip()
print("Received:", response)

if response == "OK":
    cmd = "SET_CODE_1:TEST123\n"
    ser.write(cmd.encode())
    print(f"Sent: {cmd.strip()}")
    resp = ser.readline().decode().strip()
    print("Received:", resp)
    time.sleep(0.5)

    ser.write(b'GET_CODE_1\n')
    print("Sent: GET_CODE_1")
    resp = ser.readline().decode().strip()
    print("Received:", resp)
    time.sleep(0.5)

    ser.write(b'DISCONNECT\n')
    print("Sent: DISCONNECT")
    resp = ser.readline().decode().strip()
    print("Received:", resp)
else:
    print("Connection failed, STM did not respond with OK.")

ser.close()
print("Port closed.")

