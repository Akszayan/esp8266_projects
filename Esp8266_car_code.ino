// ===============================================================
// Project: WiFi-Controlled Car Using ESP8266
// Author: Akszayan
// Description:
// This code enables a car to be controlled via WiFi using the ESP8266.  
// The car receives commands from a client connected to a TCP server 
// and moves in different directions at adjustable speeds.
// ===============================================================

#include <ESP8266WiFi.h>

// -------------------------- Wi-Fi Credentials ---------------------------
const char* ssid = "YOUR_SSID";          // Please enter your Wi-Fi SSID
const char* password = "PASSWORD";     // please enter your Wi-Fi Password

// Static IP configuration
IPAddress local_IP(192, 168, 137, 155); // Static IP address for the ESP8266
IPAddress gateway(192, 168, 137, 1);    // Gateway IP
IPAddress subnet(255, 255, 255, 0);     // Subnet Mask

// -------------------------- TCP Server Settings --------------------------
WiFiServer server(8080);               // Initialize server on port 8080
WiFiClient client;                     // Client object

// -------------------------- Motor Driver Pins ---------------------------
const int IN1 = 5;   // Motor A input pin 1 (D1 -> GPIO5)
const int IN2 = 4;   // Motor A input pin 2 (D2 -> GPIO4)
const int IN3 = 0;   // Motor B input pin 1 (D3 -> GPIO0)
const int IN4 = 2;   // Motor B input pin 2 (D4 -> GPIO2)

// -------------------------- Global Variables ----------------------------
int motorSpeed = 512; // Default motor speed (Range: 0 to 1023)

// -------------------------- Setup Function -----------------------------
void setup() {
  Serial.begin(115200); // Initialize serial communication for debugging

  // Configure motor driver pins as outputs
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Stop motors initially
  stopMotors();

  // Connect to Wi-Fi
  Serial.println("Connecting to Wi-Fi...");
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("Static IP configuration failed!");
  }
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected. IP address: ");
  Serial.println(WiFi.localIP());

  // Start TCP server
  server.begin();
  Serial.println("Server started. Waiting for client...");
}

// -------------------------- Main Loop ----------------------------------
void loop() {
  // Check for client connection
  if (!client || !client.connected()) {
    client = server.available();
    if (client) {
      Serial.println("Client connected.");
    }
  }

  // Handle incoming data
  if (client && client.available()) {
    String command = client.readStringUntil('\n'); // Read command until newline
    Serial.print("Received command: ");
    Serial.println(command);

    // Process the received command
    processCommand(command);
  }
}

// --------------------- Command Processing Function ---------------------
void processCommand(String command) {
  String direction = command.substring(0, 1);  // Extract direction (F, B, L, R, S)
  int speedIndex = command.indexOf("Speed:");
  if (speedIndex != -1) {
    motorSpeed = command.substring(speedIndex + 6).toInt(); // Extract speed value
  }

  // Execute command based on direction
  if (direction == "F") {
    moveForward();
  } else if (direction == "B") {
    moveBackward();
  } else if (direction == "L") {
    turnLeft();
  } else if (direction == "R") {
    turnRight();
  } else if (direction == "S") {
    stopMotors();
  } else {
    stopMotors();
    Serial.println("Unknown command");
  }

  // Print updated motor speed
  Serial.print("Updated motor speed: ");
  Serial.println(motorSpeed);
}

// ----------------------- Motor Control Functions -----------------------
void moveForward() {
  analogWrite(IN1, motorSpeed);
  analogWrite(IN2, 0);
  analogWrite(IN3, 0);
  analogWrite(IN4, motorSpeed);
  Serial.println("Moving forward");
}

void moveBackward() {
  analogWrite(IN1, 0);
  analogWrite(IN2, motorSpeed);
  analogWrite(IN3, motorSpeed);
  analogWrite(IN4, 0);
  Serial.println("Moving backward");
}

void turnLeft() {
  analogWrite(IN1, 0);
  analogWrite(IN2, motorSpeed / 2);
  analogWrite(IN3, 0);
  analogWrite(IN4, motorSpeed);
  Serial.println("Turning left");
}

void turnRight() {
  analogWrite(IN1, motorSpeed);
  analogWrite(IN2, 0);
  analogWrite(IN3, motorSpeed / 2);
  analogWrite(IN4, 0);
  Serial.println("Turning right");
}

void stopMotors() {
  analogWrite(IN1, 0);
  analogWrite(IN2, 0);
  analogWrite(IN3, 0);
  analogWrite(IN4, 0);
  Serial.println("Stopping motors");
}
