import RPi.GPIO as GPIO
import time

# Constants
WHEEL_DIAMETER_CM = 6.0  # Diameter of the wheel in cm
ENCODER_TICKS_PER_REV = 360  # Encoder ticks per revolution
DISTANCE_PER_TICK = (WHEEL_DIAMETER_CM * 3.14159) / ENCODER_TICKS_PER_REV
CM_PER_FOOT = 30.48

# GPIO Pins
MOTOR_LEFT_PIN = 18
MOTOR_RIGHT_PIN = 19
ENCODER_LEFT_PIN_A = 23
ENCODER_RIGHT_PIN_A = 24

# PID Parameters
Kp = 1.0
Ki = 0.1
Kd = 0.01

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_LEFT_PIN, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_PIN, GPIO.OUT)
GPIO.setup(ENCODER_LEFT_PIN_A, GPIO.IN)
GPIO.setup(ENCODER_RIGHT_PIN_A, GPIO.IN)

# PWM setup
pwm_left = GPIO.PWM(MOTOR_LEFT_PIN, 100)
pwm_right = GPIO.PWM(MOTOR_RIGHT_PIN, 100)
pwm_left.start(0)
pwm_right.start(0)

# Encoder variables
left_position = 0
right_position = 0

def encoder_left_callback(channel):
    global left_position
    left_position += 1

def encoder_right_callback(channel):
    global right_position
    right_position += 1

GPIO.add_event_detect(ENCODER_LEFT_PIN_A, GPIO.RISING, callback=encoder_left_callback)
GPIO.add_event_detect(ENCODER_RIGHT_PIN_A, GPIO.RISING, callback=encoder_right_callback)

# PID control function
def pid_control(setpoint, current_position, last_error, error_sum, last_time):
    error = setpoint - current_position
    current_time = time.time()
    dt = current_time - last_time

    error_sum += error * dt
    d_error = (error - last_error) / dt if dt > 0 else 0

    output = Kp * error + Ki * error_sum + Kd * d_error
    output = max(min(output, 100), -100)  # Constrain output to -100 to 100

    last_error = error
    last_time = current_time

    return output, error_sum, last_error, last_time

# Method to drive forward
def drive_forward(distance_ft):
    global left_position, right_position
    left_position = 0
    right_position = 0

    distance_cm = distance_ft * CM_PER_FOOT
    target_ticks = distance_cm / DISTANCE_PER_TICK
    error_sum = last_error = 0
    last_time = time.time()

    while left_position < target_ticks or right_position < target_ticks:
        output, error_sum, last_error, last_time = pid_control(
            target_ticks, (left_position + right_position) / 2, last_error, error_sum, last_time
        )
        pwm_left.ChangeDutyCycle(output)
        pwm_right.ChangeDutyCycle(output)
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)

# Example usage
try:
    drive_forward(1)  # Drive forward 1 foot
except KeyboardInterrupt:
    pwm_left.stop()
    pwm_right.stop()
    GPIO.cleanup()
