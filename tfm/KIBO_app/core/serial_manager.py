import os
import serial
import threading
from kivy.clock import Clock

class SerialManager:
    _instance = None

    def __init__(self, port="/dev/ttyUSB0", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.thread = None
        self.running = False
        self.message_callbacks = {}  # 🔁 Stores {message: callback}

    def connect(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            self.running = True
            self.thread = threading.Thread(target=self.read_loop, daemon=True)
            self.thread.start()
            print(f"🔌 Connected to {self.port} at {self.baudrate} baud.")
        except Exception as e:
            print(f"❌ Failed to connect to serial port: {e}")

    def disconnect(self):
        self.running = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("🔌 Serial connection closed.")

    def read_loop(self):
        while self.running:
            if self.serial_conn.in_waiting:
                try:
                    line = self.serial_conn.readline().decode('utf-8').strip()
                    if line:
                        print(f"📥 Received: {line}")
                        Clock.schedule_once(lambda dt: self.handle_message(line))
                except Exception as e:
                    print(f"⚠️ Serial read error: {e}")

    def handle_message(self, message):
        callback = self.message_callbacks.get(message)
        if callback:
            try:
                callback()
            except Exception as e:
                print(f"⚠️ Error in callback for '{message}': {e}")
        else:
            print(f"⚠️ No handler for message: {message}")

    def send(self, message):
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write((message + "\n").encode('utf-8'))
                print(f"📤 Sent: {message}")
            except Exception as e:
                print(f"⚠️ Serial write error: {e}")
        else:
            print("⚠️ Serial connection not open.")

    def bind_message(self, message, callback):
        self.message_callbacks[message] = callback
        print(f"🔗 Bound message '{message}' to callback '{callback.__name__}'")

    def unbind_message(self, message):
        if message in self.message_callbacks:
            del self.message_callbacks[message]
            print(f"🔓 Unbound message '{message}'")

    def unbind_all(self):
        self.message_callbacks.clear()
        print("🔁 All message callbacks cleared.")

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = SerialManager()
            cls._instance.connect()
        return cls._instance
