#include <Servo.h>

Servo klausMotor; // Create servo object

void setup() {
  Serial.begin(9600); // Start serial communication
  klausMotor.attach(9); // Attach servo to pin 9
  klausMotor.write(90); // Initialize servo to the middle position
}

void loop() {
  if (Serial.available() > 0) { // Check if data is available
    String command = Serial.readStringUntil('\n'); // Read the incoming command
    command.trim(); // Remove any trailing newline or whitespace

    if (command == "rotate") {
      klausMotor.write(180); // Rotate to 180 degrees
      delay(1000); // Wait for 1 second
      klausMotor.write(90);  // Return to center
    } else if (command == "reset") {
      klausMotor.write(90); // Reset servo to the center
    } else {
      Serial.println("Unknown command"); // Handle unknown commands
    }
  }
}