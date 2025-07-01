/*
  AI Robot Motor Control - Arduino Code Template (ANTI-JERK VERSION)
  This code eliminates jerky movement by implementing simultaneous motor control
  with PWM speed calibration for smooth operation
*/

// Motor pins - adjust these to match your wiring
// Motor A (Front Left)
int motorA_pin1 = 2;
int motorA_pin2 = 3;
int motorA_enable = 9;

// Motor B (Front Right)  
int motorB_pin1 = 4;
int motorB_pin2 = 5;
int motorB_enable = 10;

// Motor C (Back Left)
int motorC_pin1 = 6;
int motorC_pin2 = 7;
int motorC_enable = 11;

// Motor D (Back Right)
int motorD_pin1 = 8;
int motorD_pin2 = 12;
int motorD_enable = 13;

void setup() {
  Serial.begin(9600);
  
  // Initialize motor pins
  pinMode(motorA_pin1, OUTPUT);
  pinMode(motorA_pin2, OUTPUT);
  pinMode(motorA_enable, OUTPUT);
  
  pinMode(motorB_pin1, OUTPUT);
  pinMode(motorB_pin2, OUTPUT);
  pinMode(motorB_enable, OUTPUT);
  
  pinMode(motorC_pin1, OUTPUT);
  pinMode(motorC_pin2, OUTPUT);
  pinMode(motorC_enable, OUTPUT);
  
  pinMode(motorD_pin1, OUTPUT);
  pinMode(motorD_pin2, OUTPUT);
  pinMode(motorD_enable, OUTPUT);
  
  Serial.println("AI Robot Motor Controller Ready (Anti-Jerk Version)");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readString();
    command.trim();
    
    // SIMULTANEOUS MOVEMENT COMMANDS (ANTI-JERK)
    if (command.startsWith("MOVE_FORWARD:")) {
      String speeds = command.substring(13);
      move_forward_with_speeds(speeds);
      Serial.println("Command executed: MOVE_FORWARD with speeds");
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
      stop_all_motors_immediately();
      Serial.println("Command executed: STOP_ALL");
    }
    
    // ORIGINAL Individual Motor Commands (for fallback)
    else if (command == "MOTOR_A_FORWARD") {
      motorA_forward();
    } else if (command == "MOTOR_A_BACKWARD") {
      motorA_backward();
    } else if (command == "MOTOR_A_STOP") {
      motorA_stop();
    }
    
    else if (command == "MOTOR_B_FORWARD") {
      motorB_forward();
    } else if (command == "MOTOR_B_BACKWARD") {
      motorB_backward();
    } else if (command == "MOTOR_B_STOP") {
      motorB_stop();
    }
    
    else if (command == "MOTOR_C_FORWARD") {
      motorC_forward();
    } else if (command == "MOTOR_C_BACKWARD") {
      motorC_backward();
    } else if (command == "MOTOR_C_STOP") {
      motorC_stop();
    }
    
    else if (command == "MOTOR_D_FORWARD") {
      motorD_forward();
    } else if (command == "MOTOR_D_BACKWARD") {
      motorD_backward();
    } else if (command == "MOTOR_D_STOP") {
      motorD_stop();
    }
    
    // Combined Movement Commands (for backward compatibility)
    else if (command == "MOVE_FORWARD") {
      move_forward();
    } else if (command == "MOVE_BACKWARD") {
      move_backward();
    } else if (command == "MOVE_LEFT") {
      move_left();
    } else if (command == "MOVE_RIGHT") {
      move_right();
    }
    
    else {
      Serial.println("Unknown command: " + command);
    }
  }
}

// ANTI-JERK SIMULTANEOUS MOVEMENT FUNCTIONS
void move_forward_with_speeds(String speeds) {
  int speedA, speedB, speedC, speedD;
  parse_speeds(speeds, speedA, speedB, speedC, speedD);
  
  // Set all directions SIMULTANEOUSLY
  digitalWrite(motorA_pin1, HIGH); digitalWrite(motorA_pin2, LOW);
  digitalWrite(motorB_pin1, HIGH); digitalWrite(motorB_pin2, LOW);
  digitalWrite(motorC_pin1, HIGH); digitalWrite(motorC_pin2, LOW);
  digitalWrite(motorD_pin1, HIGH); digitalWrite(motorD_pin2, LOW);
  
  // Enable all motors SIMULTANEOUSLY with calibrated speeds
  analogWrite(motorA_enable, speedA);
  analogWrite(motorB_enable, speedB);
  analogWrite(motorC_enable, speedC);
  analogWrite(motorD_enable, speedD);
}

void move_backward_with_speeds(String speeds) {
  int speedA, speedB, speedC, speedD;
  parse_speeds(speeds, speedA, speedB, speedC, speedD);
  
  // Set all directions SIMULTANEOUSLY
  digitalWrite(motorA_pin1, LOW); digitalWrite(motorA_pin2, HIGH);
  digitalWrite(motorB_pin1, LOW); digitalWrite(motorB_pin2, HIGH);
  digitalWrite(motorC_pin1, LOW); digitalWrite(motorC_pin2, HIGH);
  digitalWrite(motorD_pin1, LOW); digitalWrite(motorD_pin2, HIGH);
  
  // Enable all motors SIMULTANEOUSLY with calibrated speeds
  analogWrite(motorA_enable, speedA);
  analogWrite(motorB_enable, speedB);
  analogWrite(motorC_enable, speedC);
  analogWrite(motorD_enable, speedD);
}

void turn_left_with_speeds(String speeds) {
  int speedA, speedB, speedC, speedD;
  parse_speeds(speeds, speedA, speedB, speedC, speedD);
  
  // Left motors backward, right motors forward SIMULTANEOUSLY
  digitalWrite(motorA_pin1, LOW); digitalWrite(motorA_pin2, HIGH);  // A backward
  digitalWrite(motorB_pin1, HIGH); digitalWrite(motorB_pin2, LOW);  // B forward
  digitalWrite(motorC_pin1, LOW); digitalWrite(motorC_pin2, HIGH);  // C backward
  digitalWrite(motorD_pin1, HIGH); digitalWrite(motorD_pin2, LOW);  // D forward
  
  // Enable all motors SIMULTANEOUSLY with calibrated speeds
  analogWrite(motorA_enable, speedA);
  analogWrite(motorB_enable, speedB);
  analogWrite(motorC_enable, speedC);
  analogWrite(motorD_enable, speedD);
}

void turn_right_with_speeds(String speeds) {
  int speedA, speedB, speedC, speedD;
  parse_speeds(speeds, speedA, speedB, speedC, speedD);
  
  // Left motors forward, right motors backward SIMULTANEOUSLY
  digitalWrite(motorA_pin1, HIGH); digitalWrite(motorA_pin2, LOW);  // A forward
  digitalWrite(motorB_pin1, LOW); digitalWrite(motorB_pin2, HIGH);  // B backward
  digitalWrite(motorC_pin1, HIGH); digitalWrite(motorC_pin2, LOW);  // C forward
  digitalWrite(motorD_pin1, LOW); digitalWrite(motorD_pin2, HIGH);  // D backward
  
  // Enable all motors SIMULTANEOUSLY with calibrated speeds
  analogWrite(motorA_enable, speedA);
  analogWrite(motorB_enable, speedB);
  analogWrite(motorC_enable, speedC);
  analogWrite(motorD_enable, speedD);
}

void stop_all_motors_immediately() {
  // Stop ALL motors SIMULTANEOUSLY for smooth stopping
  digitalWrite(motorA_pin1, LOW); digitalWrite(motorA_pin2, LOW);
  digitalWrite(motorB_pin1, LOW); digitalWrite(motorB_pin2, LOW);
  digitalWrite(motorC_pin1, LOW); digitalWrite(motorC_pin2, LOW);
  digitalWrite(motorD_pin1, LOW); digitalWrite(motorD_pin2, LOW);
  
  analogWrite(motorA_enable, 0);
  analogWrite(motorB_enable, 0);
  analogWrite(motorC_enable, 0);
  analogWrite(motorD_enable, 0);
}

// Helper function to parse speed values
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

// Individual Motor Control Functions (for backward compatibility)
void motorA_forward() {
  digitalWrite(motorA_pin1, HIGH);
  digitalWrite(motorA_pin2, LOW);
  analogWrite(motorA_enable, 255);
}

void motorA_backward() {
  digitalWrite(motorA_pin1, LOW);
  digitalWrite(motorA_pin2, HIGH);
  analogWrite(motorA_enable, 255);
}

void motorA_stop() {
  digitalWrite(motorA_pin1, LOW);
  digitalWrite(motorA_pin2, LOW);
  analogWrite(motorA_enable, 0);
}

void motorB_forward() {
  digitalWrite(motorB_pin1, HIGH);
  digitalWrite(motorB_pin2, LOW);
  analogWrite(motorB_enable, 255);
}

void motorB_backward() {
  digitalWrite(motorB_pin1, LOW);
  digitalWrite(motorB_pin2, HIGH);
  analogWrite(motorB_enable, 255);
}

void motorB_stop() {
  digitalWrite(motorB_pin1, LOW);
  digitalWrite(motorB_pin2, LOW);
  analogWrite(motorB_enable, 0);
}

void motorC_forward() {
  digitalWrite(motorC_pin1, HIGH);
  digitalWrite(motorC_pin2, LOW);
  analogWrite(motorC_enable, 255);
}

void motorC_backward() {
  digitalWrite(motorC_pin1, LOW);
  digitalWrite(motorC_pin2, HIGH);
  analogWrite(motorC_enable, 255);
}

void motorC_stop() {
  digitalWrite(motorC_pin1, LOW);
  digitalWrite(motorC_pin2, LOW);
  analogWrite(motorC_enable, 0);
}

void motorD_forward() {
  digitalWrite(motorD_pin1, HIGH);
  digitalWrite(motorD_pin2, LOW);
  analogWrite(motorD_enable, 255);
}

void motorD_backward() {
  digitalWrite(motorD_pin1, LOW);
  digitalWrite(motorD_pin2, HIGH);
  analogWrite(motorD_enable, 255);
}

void motorD_stop() {
  digitalWrite(motorD_pin1, LOW);
  digitalWrite(motorD_pin2, LOW);
  analogWrite(motorD_enable, 0);
}

// Combined Movement Functions (backward compatibility)
void move_forward() {
  motorA_forward();
  motorB_forward();
  motorC_forward();
  motorD_forward();
}

void move_backward() {
  motorA_backward();
  motorB_backward();
  motorC_backward();
  motorD_backward();
}

void move_left() {
  motorA_backward();  // Left motors backward
  motorC_backward();
  motorB_forward();   // Right motors forward
  motorD_forward();
}

void move_right() {
  motorA_forward();   // Left motors forward
  motorC_forward();
  motorB_backward();  // Right motors backward
  motorD_backward();
} 