
# temperature tool returns the temperature of the room in celsius
import json
import datetime
import time
import serial

# ---------- CONFIGURATIONS ----------
SERIAL_PORT = 'COM8'   # Change to your Arduino port
BAUD_RATE = 115200  # Standard baud rate for Arduino


class Arduino:
    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)  # Allow Arduino to reset
        except Exception as e:
            print(f"Error initializing serial port: {e}")
            self.ser = None

    def temp(self):

        temp = None
        while temp is None:
            if self.ser and self.ser.in_waiting:
                try:
                    raw_data = self.ser.readline().decode('utf-8').strip()
                    if raw_data:
                        json_data = json.loads(raw_data)
                        if json_data:
                            # Extract values from the incoming data
                            temp =  json_data.get('Temperature')
                            humid = json_data.get('Humidity')
                            light = json_data.get('Light')
                            return temp
                except json.JSONDecodeError:
                    print("Received invalid JSON from Arduino.")
                except Exception as e:
                    print(f"Error reading serial: {e}")

    def light_on(self):
        if self.ser:
                try:
                    self.ser.write(b'LEDON\n')
                    print("Sent Relay 2 OFF command")
                except Exception as e:
                    print(f"Failed to send command: {e}")
    
    def light_off(self):
        if self.ser:
                try:
                    self.ser.write(b'LEDOFF\n')
                    print("Sent Relay 2 OFF command")
                except Exception as e:
                    print(f"Failed to send command: {e}")
    
    def relay1_on(self):
        if self.ser:
                try:
                    self.ser.write(b'RELAY1ON\n')
                    print("Sent Relay 1 ON command")
                except Exception as e:
                    print(f"Failed to send command: {e}")
    
    def relay1_off(self):
        if self.ser:
            try:
                self.ser.write(b'RELAY1OFF\n')
                print("Sent Relay 1 OFF command")
            except Exception as e:
                print(f"Failed to send command: {e}")
    
    def servo_on(self):
         if self.ser:
            try:
                self.ser.write(b'SERVOON\n')
                print("Sent Relay 1 OFF command")
            except Exception as e:
                print(f"Failed to send command: {e}")

    def servo_off(self):
            if self.ser:
                try:
                    self.ser.write(b'SERVOOFF\n')
                    print("Sent Relay 1 OFF command")
                except Exception as e:
                    print(f"Failed to send command: {e}")