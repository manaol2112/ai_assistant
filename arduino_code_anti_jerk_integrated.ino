#include <Servo.h>

// Motor pins (L298N) - Your existing configuration
int motorA1 = 2, motorA2 = 4, ENA = 3;
int motorB1 = 6, motorB2 = 7, ENB = 5;
int motorC1 = 8, motorC2 = 10, ENC = 9;
int motorD1 = 12, motorD2 = 13, END = 11;

// Servo pins - Your existing configuration
Servo myServo;     // First servo (left/right)
Servo myServo2;    // Second servo (up/down)
int servoPin1 = A0;
int servoPin2 = A5;

// Ultrasonic sensor - Your existing configuration
const int trigPin = A4;
const int echoPin = A3;

// IR sensors - Your existing configuration
const int irLeftPin = A1;
const int irRightPin = A2;

// SAFETY SETTINGS - Prevent collisions during movement
const int SAFE_DISTANCE = 15;  // Stop if obstacle within 15cm
bool safety_enabled = true;    // Enable collision avoidance

void setup() {
  // Motor setup - Your existing configuration
  pinMode(motorA1, OUTPUT); pinMode(motorA2, OUTPUT); pinMode(ENA, OUTPUT);
  pinMode(motorB1, OUTPUT); pinMode(motorB2, OUTPUT); pinMode(ENB, OUTPUT);
  pinMode(motorC1, OUTPUT); pinMode(motorC2, OUTPUT); pinMode(ENC, OUTPUT);
  pinMode(motorD1, OUTPUT); pinMode(motorD2, OUTPUT); pinMode(END, OUTPUT);

  // Initialize motors in stopped state
  digitalWrite(ENA, LOW); digitalWrite(ENB, LOW);
  digitalWrite(ENC, LOW); digitalWrite(END, LOW);

  // Servo setup - Your existing configuration
  myServo.attach(servoPin1);
  myServo2.attach(servoPin2);
  myServo.write(90);   // Center position
  myServo2.write(90);  // Center position

  // Sensor setup - Your existing configuration
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(irLeftPin, INPUT);
  pinMode(irRightPin, INPUT);

  Serial.begin(9600);
  Serial.println("AI Robot Motor Controller Ready (Anti-Jerk + Safety Version)");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    Serial.print("Received command: ");
    Serial.println(command);

    // ANTI-JERK SIMULTANEOUS MOVEMENT COMMANDS (NEW)
    if (command.startsWith("MOVE_FORWARD:")) {
      String speeds = command.substring(13);
      if (is_safe_to_move_forward()) {
        move_forward_with_speeds(speeds);
        Serial.println("Command executed: MOVE_FORWARD with speeds");
      } else {
        emergency_stop_all();
        Serial.println("SAFETY: Forward movement blocked - obstacle detected");
      }
    } 
    else if (command.startsWith("MOVE_BACKWARD:")) {
      String speeds = command.substring(14);
      move_backward_with_speeds(speeds);
      Serial.println("Command executed: MOVE_BACKWARD with speeds");
    }
    else if (command.startsWith("TURN_LEFT:")) {
      String speeds = command.substring(10);
      turn_left_with_speeds(speeds);
      Serial.println("Command executed: TURN_LEFT with speeds");
    }
    else if (command.startsWith("TURN_RIGHT:")) {
      String speeds = command.substring(11);
      turn_right_with_speeds(speeds);
      Serial.println("Command executed: TURN_RIGHT with speeds");
    }
    else if (command == "STOP_ALL") {
      emergency_stop_all();
      Serial.println("Command executed: STOP_ALL");
    }
    else if (command == "SAFETY_ON") {
      safety_enabled = true;
      Serial.println("Safety collision avoidance: ENABLED");
    }
    else if (command == "SAFETY_OFF") {
      safety_enabled = false;
      Serial.println("Safety collision avoidance: DISABLED");
    }

    // SERVO CONTROL - Your existing functionality preserved
    else if (command.startsWith("SERVO_")) {
      int angle = command.substring(6).toInt();
      if (angle >= 0 && angle <= 180) {
        myServo.write(angle);
        Serial.print("Servo 1 moved to ");
        Serial.println(angle);
      }
    }
    else if (command.startsWith("SERVO2_")) {
      int angle2 = command.substring(7).toInt();
      if (angle2 >= 0 && angle2 <= 180) {
        myServo2.write(angle2);
        Serial.print("Servo 2 moved to ");
        Serial.println(angle2);
      }
    }

    // INDIVIDUAL MOTOR COMMANDS - Your existing functionality preserved (with safety)
    else if (command == "MOTOR_A_FORWARD") {
      if (is_safe_to_move_forward()) {
        digitalWrite(ENA, HIGH); digitalWrite(motorA1, HIGH); digitalWrite(motorA2, LOW);
      } else {
        Serial.println("SAFETY: Motor A forward blocked");
      }
    } else if (command == "MOTOR_A_BACKWARD") {
      digitalWrite(ENA, HIGH); digitalWrite(motorA1, LOW); digitalWrite(motorA2, HIGH);
    } else if (command == "MOTOR_A_STOP") {
      digitalWrite(ENA, LOW); digitalWrite(motorA1, LOW); digitalWrite(motorA2, LOW);

    } else if (command == "MOTOR_B_FORWARD") {
      if (is_safe_to_move_forward()) {
        digitalWrite(ENB, HIGH); digitalWrite(motorB1, HIGH); digitalWrite(motorB2, LOW);
      } else {
        Serial.println("SAFETY: Motor B forward blocked");
      }
    } else if (command == "MOTOR_B_BACKWARD") {
      digitalWrite(ENB, HIGH); digitalWrite(motorB1, LOW); digitalWrite(motorB2, HIGH);
    } else if (command == "MOTOR_B_STOP") {
      digitalWrite(ENB, LOW); digitalWrite(motorB1, LOW); digitalWrite(motorB2, LOW);

    } else if (command == "MOTOR_C_FORWARD") {
      if (is_safe_to_move_forward()) {
        digitalWrite(ENC, HIGH); digitalWrite(motorC1, HIGH); digitalWrite(motorC2, LOW);
      } else {
        Serial.println("SAFETY: Motor C forward blocked");
      }
    } else if (command == "MOTOR_C_BACKWARD") {
      digitalWrite(ENC, HIGH); digitalWrite(motorC1, LOW); digitalWrite(motorC2, HIGH);
    } else if (command == "MOTOR_C_STOP") {
      digitalWrite(ENC, LOW); digitalWrite(motorC1, LOW); digitalWrite(motorC2, LOW);

    } else if (command == "MOTOR_D_FORWARD") {
      if (is_safe_to_move_forward()) {
        digitalWrite(END, HIGH); digitalWrite(motorD1, HIGH); digitalWrite(motorD2, LOW);
      } else {
        Serial.println("SAFETY: Motor D forward blocked");
      }
    } else if (command == "MOTOR_D_BACKWARD") {
      digitalWrite(END, HIGH); digitalWrite(motorD1, LOW); digitalWrite(motorD2, HIGH);
    } else if (command == "MOTOR_D_STOP") {
      digitalWrite(END, LOW); digitalWrite(motorD1, LOW); digitalWrite(motorD2, LOW);

    // SENSOR COMMANDS - Your existing functionality preserved
    } else if (command == "READ_ULTRASONIC") {
      int distance = read_ultrasonic_distance();
      Serial.print("ULTRASONIC_DISTANCE:");
      Serial.println(distance);

    } else if (command == "READ_IR_LEFT") {
      int val = digitalRead(irLeftPin);
      Serial.print("IR_LEFT:");
      Serial.println(val);
    } else if (command == "READ_IR_RIGHT") {
      int val = digitalRead(irRightPin);
      Serial.print("IR_RIGHT:");
      Serial.println(val);
    } else if (command == "READ_IR_BOTH") {
      int left = digitalRead(irLeftPin);
      int right = digitalRead(irRightPin);
      Serial.print("IR_BOTH:");
      Serial.print(left);
      Serial.print(",");
      Serial.println(right);

    // COMBINED MOVEMENT COMMANDS (for backward compatibility)
    } else if (command == "MOVE_FORWARD") {
      if (is_safe_to_move_forward()) {
        move_forward_basic();
      } else {
        emergency_stop_all();
        Serial.println("SAFETY: Forward movement blocked");
      }
    } else if (command == "MOVE_BACKWARD") {
      move_backward_basic();
    } else if (command == "MOVE_LEFT") {
      move_left_basic();
    } else if (command == "MOVE_RIGHT") {
      move_right_basic();

    } else {
      Serial.println("Invalid command received!");
    }
  }
}

// ANTI-JERK SIMULTANEOUS MOVEMENT FUNCTIONS (NEW)
void move_forward_with_speeds(String speeds) {
  int speedA, speedB, speedC, speedD;
  parse_speeds(speeds, speedA, speedB, speedC, speedD);
  
  // Set all directions SIMULTANEOUSLY for smooth movement
  digitalWrite(motorA1, HIGH); digitalWrite(motorA2, LOW);
  digitalWrite(motorB1, HIGH); digitalWrite(motorB2, LOW);
  digitalWrite(motorC1, HIGH); digitalWrite(motorC2, LOW);
  digitalWrite(motorD1, HIGH); digitalWrite(motorD2, LOW);
  
  // Enable all motors SIMULTANEOUSLY with calibrated speeds
  analogWrite(ENA, speedA);
  analogWrite(ENB, speedB);
  analogWrite(ENC, speedC);
  analogWrite(END, speedD);
}

void move_backward_with_speeds(String speeds) {
  int speedA, speedB, speedC, speedD;
  parse_speeds(speeds, speedA, speedB, speedC, speedD);
  
  // Set all directions SIMULTANEOUSLY for smooth movement
  digitalWrite(motorA1, LOW); digitalWrite(motorA2, HIGH);
  digitalWrite(motorB1, LOW); digitalWrite(motorB2, HIGH);
  digitalWrite(motorC1, LOW); digitalWrite(motorC2, HIGH);
  digitalWrite(motorD1, LOW); digitalWrite(motorD2, HIGH);
  
  // Enable all motors SIMULTANEOUSLY with calibrated speeds
  analogWrite(ENA, speedA);
  analogWrite(ENB, speedB);
  analogWrite(ENC, speedC);
  analogWrite(END, speedD);
}

void turn_left_with_speeds(String speeds) {
  int speedA, speedB, speedC, speedD;
  parse_speeds(speeds, speedA, speedB, speedC, speedD);
  
  // Left motors backward, right motors forward SIMULTANEOUSLY
  digitalWrite(motorA1, LOW); digitalWrite(motorA2, HIGH);  // A backward
  digitalWrite(motorB1, HIGH); digitalWrite(motorB2, LOW);  // B forward
  digitalWrite(motorC1, LOW); digitalWrite(motorC2, HIGH);  // C backward
  digitalWrite(motorD1, HIGH); digitalWrite(motorD2, LOW);  // D forward
  
  // Enable all motors SIMULTANEOUSLY with calibrated speeds
  analogWrite(ENA, speedA);
  analogWrite(ENB, speedB);
  analogWrite(ENC, speedC);
  analogWrite(END, speedD);
}

void turn_right_with_speeds(String speeds) {
  int speedA, speedB, speedC, speedD;
  parse_speeds(speeds, speedA, speedB, speedC, speedD);
  
  // Left motors forward, right motors backward SIMULTANEOUSLY
  digitalWrite(motorA1, HIGH); digitalWrite(motorA2, LOW);  // A forward
  digitalWrite(motorB1, LOW); digitalWrite(motorB2, HIGH);  // B backward
  digitalWrite(motorC1, HIGH); digitalWrite(motorC2, LOW);  // C forward
  digitalWrite(motorD1, LOW); digitalWrite(motorD2, HIGH);  // D backward
  
  // Enable all motors SIMULTANEOUSLY with calibrated speeds
  analogWrite(ENA, speedA);
  analogWrite(ENB, speedB);
  analogWrite(ENC, speedC);
  analogWrite(END, speedD);
}

void emergency_stop_all() {
  // Stop ALL motors SIMULTANEOUSLY for immediate stopping
  digitalWrite(motorA1, LOW); digitalWrite(motorA2, LOW);
  digitalWrite(motorB1, LOW); digitalWrite(motorB2, LOW);
  digitalWrite(motorC1, LOW); digitalWrite(motorC2, LOW);
  digitalWrite(motorD1, LOW); digitalWrite(motorD2, LOW);
  
  digitalWrite(ENA, LOW);
  digitalWrite(ENB, LOW);
  digitalWrite(ENC, LOW);
  digitalWrite(END, LOW);
}

// SAFETY FUNCTIONS - Prevent collisions (IMPROVED WITH SMART FILTERING)
bool is_safe_to_move_forward() {
  if (!safety_enabled) return true;
  
  // SMART ULTRASONIC FILTERING - Take multiple readings
  int distances[3];
  int valid_readings = 0;
  int total_distance = 0;
  
  // Take 3 readings with small delays
  for (int i = 0; i < 3; i++) {
    distances[i] = read_ultrasonic_distance();
    
    // Only count valid readings (ignore false readings below 3cm)
    if (distances[i] > 3 && distances[i] < 400) {  
      valid_readings++;
      total_distance += distances[i];
    }
    delay(10);  // Small delay between readings
  }
  
  // Only block movement if we have consistent valid readings
  if (valid_readings >= 2) {
    int avg_distance = total_distance / valid_readings;
    
    // Block only if average distance shows real obstacle
    if (avg_distance < SAFE_DISTANCE) {
      Serial.print("SAFETY: Confirmed obstacle at ");
      Serial.print(avg_distance);
      Serial.println("cm (filtered average)");
      return false;
    }
  }
  
  // SMART IR FILTERING - Require consistent detections
  int ir_left_detections = 0;
  int ir_right_detections = 0;
  
  // Take 3 quick IR readings
  for (int i = 0; i < 3; i++) {
    if (digitalRead(irLeftPin) == 0) ir_left_detections++;
    if (digitalRead(irRightPin) == 0) ir_right_detections++;
    delay(5);
  }
  
  // Block only if IR sensors consistently detect obstacle (2 out of 3 readings)
  if (ir_left_detections >= 2 || ir_right_detections >= 2) {
    Serial.println("SAFETY: IR sensors consistently detected obstacle");
    return false;
  }
  
  // If we get here, it's safe to move forward
  return true;
}

int read_ultrasonic_distance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH, 30000); // 30ms timeout
  if (duration == 0) return -1; // No echo received
  
  int distance = duration * 0.034 / 2;
  return distance;
}

// HELPER FUNCTIONS
void parse_speeds(String speeds, int &speedA, int &speedB, int &speedC, int &speedD) {
  // Format: "200,200,200,200" (A,B,C,D speeds)
  int commaIndex1 = speeds.indexOf(',');
  int commaIndex2 = speeds.indexOf(',', commaIndex1 + 1);
  int commaIndex3 = speeds.indexOf(',', commaIndex2 + 1);
  
  if (commaIndex1 > 0 && commaIndex2 > 0 && commaIndex3 > 0) {
    speedA = speeds.substring(0, commaIndex1).toInt();
    speedB = speeds.substring(commaIndex1 + 1, commaIndex2).toInt();
    speedC = speeds.substring(commaIndex2 + 1, commaIndex3).toInt();
    speedD = speeds.substring(commaIndex3 + 1).toInt();
    
    // Safety limits
    speedA = constrain(speedA, 0, 255);
    speedB = constrain(speedB, 0, 255);
    speedC = constrain(speedC, 0, 255);
    speedD = constrain(speedD, 0, 255);
  } else {
    // Default speeds if parsing fails
    speedA = speedB = speedC = speedD = 200;
  }
}

// BASIC MOVEMENT FUNCTIONS (for backward compatibility)
void move_forward_basic() {
  digitalWrite(ENA, HIGH); digitalWrite(motorA1, HIGH); digitalWrite(motorA2, LOW);
  digitalWrite(ENB, HIGH); digitalWrite(motorB1, HIGH); digitalWrite(motorB2, LOW);
  digitalWrite(ENC, HIGH); digitalWrite(motorC1, HIGH); digitalWrite(motorC2, LOW);
  digitalWrite(END, HIGH); digitalWrite(motorD1, HIGH); digitalWrite(motorD2, LOW);
}

void move_backward_basic() {
  digitalWrite(ENA, HIGH); digitalWrite(motorA1, LOW); digitalWrite(motorA2, HIGH);
  digitalWrite(ENB, HIGH); digitalWrite(motorB1, LOW); digitalWrite(motorB2, HIGH);
  digitalWrite(ENC, HIGH); digitalWrite(motorC1, LOW); digitalWrite(motorC2, HIGH);
  digitalWrite(END, HIGH); digitalWrite(motorD1, LOW); digitalWrite(motorD2, HIGH);
}

void move_left_basic() {
  // Left motors backward, right motors forward
  digitalWrite(ENA, HIGH); digitalWrite(motorA1, LOW); digitalWrite(motorA2, HIGH);
  digitalWrite(ENB, HIGH); digitalWrite(motorB1, HIGH); digitalWrite(motorB2, LOW);
  digitalWrite(ENC, HIGH); digitalWrite(motorC1, LOW); digitalWrite(motorC2, HIGH);
  digitalWrite(END, HIGH); digitalWrite(motorD1, HIGH); digitalWrite(motorD2, LOW);
}

void move_right_basic() {
  // Left motors forward, right motors backward
  digitalWrite(ENA, HIGH); digitalWrite(motorA1, HIGH); digitalWrite(motorA2, LOW);
  digitalWrite(ENB, HIGH); digitalWrite(motorB1, LOW); digitalWrite(motorB2, HIGH);
  digitalWrite(ENC, HIGH); digitalWrite(motorC1, HIGH); digitalWrite(motorC2, LOW);
  digitalWrite(END, HIGH); digitalWrite(motorD1, LOW); digitalWrite(motorD2, HIGH);
} 