import serial
import time

# Replace '/dev/cu.usbmodem11201' with your Arduino's port
arduino = serial.Serial('/dev/cu.usbmodem11201', 9600)
time.sleep(2)  # Wait for the connection to initialize

def send_command_to_arduino(command):
    """Send a command to the Arduino."""
    try:
        arduino.write((command + '\n').encode())  # Send command
        print(f"Command '{command}' sent to Arduino.")
    except Exception as e:
        print(f"Error sending command to Arduino: {e}")

def klaus_control(text):
    # Check for negation first
    if "do not rotate" in text.lower() or "don't rotate" in text.lower():
        return "I will not rotate the motor as per your request."
    elif "rotate" in text.lower():
        send_command_to_arduino("rotate")
        return "Rotating the motor!"
    elif "reset" in text.lower():
        send_command_to_arduino("reset")
        return "Resetting the motor!"
    else:
        return "I can't understand that command."