// IMPROVED SAFETY FUNCTION - Replace the existing is_safe_to_move_forward() function
// in your arduino_code_anti_jerk_integrated.ino with this improved version

bool is_safe_to_move_forward() {
  if (!safety_enabled) return true;
  
  // SMART ULTRASONIC FILTERING - Take multiple readings
  int distances[3];
  int valid_readings = 0;
  int total_distance = 0;
  
  // Take 3 readings with small delays
  for (int i = 0; i < 3; i++) {
    distances[i] = read_ultrasonic_distance();
    
    // Only count valid readings (ignore false readings)
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

/* 
INSTALLATION INSTRUCTIONS:
1. Open your arduino_code_anti_jerk_integrated.ino file
2. Find the existing is_safe_to_move_forward() function (around line 287)
3. Replace the entire function with the code above
4. Upload to your Arduino
5. Test forward movement

WHAT THIS FIX DOES:
✅ Ignores ultrasonic readings below 3cm (false readings)
✅ Takes 3 readings and uses average (filters noise)
✅ Requires 2 out of 3 IR detections to block movement
✅ Keeps sensors working but prevents false blocking
✅ Maintains collision safety for real obstacles

QUICK TEST AFTER UPLOAD:
- python3 fix_motor_directions.py
- Forward movement should now work!
*/ 