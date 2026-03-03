# esp32_protocol/protocol.py - ESP32 communication protocol definitions
import serial
import serial.tools.list_ports
import threading
import time

# Global singleton for the serial connection
_serial_instance = None
_serial_lock = threading.Lock()

# Automatically find the ESP32 serial port
def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "UART" in port.description:
            return port.device
    raise IOError("ESP32 not found")

# Initialize or return existing serial connection
def get_serial_connection(baudrate=115200, timeout=1):
    global _serial_instance
    if _serial_instance is None:
        port = find_esp32_port()
        _serial_instance = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        time.sleep(2)  # Allow time for ESP32 to reset
    return _serial_instance

# Send a message to ESP32
def send_message(message: str):
    with _serial_lock:
        ser = get_serial_connection()
        ser.write((message + '\n').encode())

# Read a single line (if available)
def read_message():
    with _serial_lock:
        ser = get_serial_connection()
        if ser.in_waiting > 0:
            return ser.readline().decode().strip()
    return None

