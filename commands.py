import motor_control
import time

# Forward movement command
def forward(feet):
    target_speed = 50  # Define target speed
    duration = feet / 0.5  # Example conversion: 1 foot = 0.5 seconds at target speed
    start_time = time.time()
    while time.time() - start_time < duration:
        motor_control.update_motor1(target_speed)
        motor_control.update_motor2(target_speed)
    motor_control.update_motor1(0)  # Stop motors
    motor_control.update_motor2(0)

# Backward movement command
def backward(feet):
    target_speed = -50  # Negative target speed for backward movement
    duration = feet / 0.5
    start_time = time.time()
    while time.time() - start_time < duration:
        motor_control.update_motor1(target_speed)
        motor_control.update_motor2(target_speed)
    motor_control.update_motor1(0)
    motor_control.update_motor2(0)

# Pivot turn command (one wheel stationary)
def pivot_turn(degrees):
    target_speed = 50
    if degrees < 0:
        duration = abs(degrees) / 90  # Example conversion
        start_time = time.time()
        while time.time() - start_time < duration:
            motor_control.update_motor1(target_speed)  # Only one motor moves
            motor_control.update_motor2(0)
        motor_control.update_motor1(0)
        motor_control.update_motor2(0)
    else:
        duration = degrees / 90
        start_time = time.time()
        while time.time() - start_time < duration:
            motor_control.update_motor1(0)
            motor_control.update_motor2(target_speed)  # Only one motor moves
        motor_control.update_motor1(0)
        motor_control.update_motor2(0)

# Tank turn command (both wheels move in opposite directions)
def tank_turn(degrees):
    target_speed = 50
    duration = abs(degrees) / 90  # Example conversion
    start_time = time.time()
    if degrees < 0:
        while time.time() - start_time < duration:
            motor_control.update_motor1(target_speed)  # Opposite directions
            motor_control.update_motor2(-target_speed)
    else:
        while time.time() - start_time < duration:
            motor_control.update_motor1(-target_speed)  # Opposite directions
            motor_control.update_motor2(target_speed)
    motor_control.update_motor1(0)
    motor_control.update_motor2(0)

