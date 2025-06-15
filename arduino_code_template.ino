/*
  AI Robot Motor Control - Arduino Code Template
  This template shows the correct implementation for 4-motor control
  Make sure your Arduino code includes these backward movement commands
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
  
  Serial.println("AI Robot Motor Controller Ready");
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readString();
    command.trim();
    
    // Individual Motor Commands
    if (command == "MOTOR_A_FORWARD") {
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
    
    // Combined Movement Commands
    else if (command == "MOVE_FORWARD") {
      move_forward();
    } else if (command == "MOVE_BACKWARD") {
      move_backward();  // THIS IS CRITICAL FOR YOUR ISSUE
    } else if (command == "MOVE_LEFT") {
      move_left();
    } else if (command == "MOVE_RIGHT") {
      move_right();
    } else if (command == "STOP_ALL") {
      stop_all_motors();
    }
    
    Serial.println("Command executed: " + command);
  }
}

// Individual Motor Control Functions
void motorA_forward() {
  digitalWrite(motorA_pin1, HIGH);
  digitalWrite(motorA_pin2, LOW);
  analogWrite(motorA_enable, 255);
}

void motorA_backward() {
  digitalWrite(motorA_pin1, LOW);   // REVERSE THE PINS
  digitalWrite(motorA_pin2, HIGH);  // FOR BACKWARD MOVEMENT
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
  digitalWrite(motorB_pin1, LOW);   // REVERSE THE PINS
  digitalWrite(motorB_pin2, HIGH);  // FOR BACKWARD MOVEMENT
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
  digitalWrite(motorC_pin1, LOW);   // REVERSE THE PINS
  digitalWrite(motorC_pin2, HIGH);  // FOR BACKWARD MOVEMENT
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
  digitalWrite(motorD_pin1, LOW);   // REVERSE THE PINS
  digitalWrite(motorD_pin2, HIGH);  // FOR BACKWARD MOVEMENT
  analogWrite(motorD_enable, 255);
}

void motorD_stop() {
  digitalWrite(motorD_pin1, LOW);
  digitalWrite(motorD_pin2, LOW);
  analogWrite(motorD_enable, 0);
}

// Combined Movement Functions
void move_forward() {
  motorA_forward();
  motorB_forward();
  motorC_forward();
  motorD_forward();
}

void move_backward() {
  // THIS IS THE KEY FUNCTION FOR YOUR BACKWARD MOVEMENT ISSUE
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

void stop_all_motors() {
  motorA_stop();
  motorB_stop();
  motorC_stop();
  motorD_stop();
} 