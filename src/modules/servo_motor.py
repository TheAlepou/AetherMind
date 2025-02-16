import serial
import time

# Try to detect Arduino connection
try:
    arduino = serial.Serial('/dev/cu.usbmodem11301', 9600)  # Replace with your actual port
    time.sleep(2)  # Give the connection some time to initialize
    ARDUINO_CONNECTED = True
    print("✅ Arduino connected successfully!")
except Exception as e:
    print(f"⚠️ Arduino not detected: {e}")
    ARDUINO_CONNECTED = False

def send_command_to_arduino(command):
    """Send a command to the Arduino if connected; otherwise, print a debug message."""
    if ARDUINO_CONNECTED:
        try:
            arduino.write((command + '\n').encode())  # Send command
            print(f"🟢 Command '{command}' sent to Arduino.")
        except Exception as e:
            print(f"❌ Error sending command: {e}")
    else:
        print(f"🟡 Debug Mode: Command '{command}' would be sent to Arduino.")