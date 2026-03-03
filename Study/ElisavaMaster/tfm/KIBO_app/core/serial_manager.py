import serial
import threading
from kivy.clock import Clock
from serial.tools import list_ports  # Add this at the top

class SerialManager:
    _instance = None

    def __init__(self, port='/dev/cu.wchusbserial550D0119401', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.thread = None
        self.running = False
        self.callbacks = {}

    def detect_port(self):
        ports = list(list_ports.comports())
        if not ports:
            print("❌ No serial ports found.")
            return '/dev/ttyUSB0'  # Fallback
        for port in ports:
            if 'USB' in port.device or 'ttyACM' in port.device:
                print(f"🔍 Detected serial port: {port.device}")
                return port.device
        print("⚠️ No matcEhing USB serial device found, using fallback.")
        return ports[0].device

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SerialManager()
        return cls._instance

    def start(self):
        try:
            self.ser = serial.Serial(
                self.port,
                self.baudrate,
                timeout=1,
                write_timeout=1,
                dsrdtr=False,  # Avoid RTS/DTR reset
                rtscts=False
            )
            self.ser.dtr = False  # Explicitly disable DTR
            self.ser.rts = False  # Explicitly disable RTS

            self.running = True
            self.thread = threading.Thread(target=self.read_loop)
            self.thread.daemon = True
            self.thread.start()
            print("🔌 Serial connection started.")
        except serial.SerialException as e:
            print(f"❌ Serial connection error: {e}")

    def stop(self):
        self.running = False
        if self.ser:
            self.ser.close()
            print("🛑 Serial connection closed.")

    def read_loop(self):
        while self.running and self.ser:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    Clock.schedule_once(lambda dt: self.dispatch(line))
            except Exception as e:
                print(f"⚠️ Serial read error: {e}")

    def dispatch(self, message):
        callback = self.callbacks.get(message)
        if callback:
            callback()

    def bind_message(self, message, callback):
        self.callbacks[message] = callback

    def unbind_message(self, message):
        if message in self.callbacks:
            del self.callbacks[message]

    def unbind_all(self):
        self.callbacks.clear()

    def send(self, message):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write((message + '\n').encode('utf-8'))
                print(f"sent: {message}")
            except Exception as e:
                print(f"⚠️ Serial send error: {e}")
