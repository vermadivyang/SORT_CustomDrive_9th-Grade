import RPi.GPIO as GPIO
import time
from pid import PID

GPIO.setmode(GPIO.BCM)

# Motor pins
MOTOR1_PWM = 18
MOTOR1_DIR = 23
MOTOR1_ENC_A = 24
MOTOR1_ENC_B = 25

MOTOR2_PWM = 19
MOTOR2_DIR = 27
MOTOR2_ENC_A = 22
MOTOR2_ENC_B = 21

# Set up GPIO pins
GPIO.setup(MOTOR1_PWM, GPIO.OUT)
GPIO.setup(MOTOR1_DIR, GPIO.OUT)
GPIO.setup(MOTOR1_ENC_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MOTOR1_ENC_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(MOTOR2_PWM, GPIO.OUT)
GPIO.setup(MOTOR2_DIR, GPIO.OUT)
GPIO.setup(MOTOR2_ENC_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MOTOR2_ENC_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# PWM setup
motor1_pwm = GPIO.PWM(MOTOR1_PWM, 1000)
motor2_pwm = GPIO.PWM(MOTOR2_PWM, 1000)
motor1_pwm.start(0)
motor2_pwm.start(0)

# PID setup
Kp, Ki, Kd = 1.0, 0.1, 0.05
pid_motor1 = PID(Kp, Ki, Kd, 0)
pid_motor2 = PID(Kp, Ki, Kd, 0)

# Encoder counts
encoder_count1 = 0
encoder_count2 = 0

def encoder_callback_motor1(channel):
    global encoder_count1
    if GPIO.input(MOTOR1_ENC_A) == GPIO.input(MOTOR1_ENC_B):
        encoder_count1 += 1
    else:
        encoder_count1 -= 1

def encoder_callback_motor2(channel):
    global encoder_count2
    if GPIO.input(MOTOR2_ENC_A) == GPIO.input(MOTOR2_ENC_B):
        encoder_count2 += 1
    else:
        encoder_count2 -= 1

# Set up interrupts
GPIO.add_event_detect(MOTOR1_ENC_A, GPIO.BOTH, callback=encoder_callback_motor1)
GPIO.add_event_detect(MOTOR2_ENC_A, GPIO.BOTH, callback=encoder_callback_motor2)

def read_encoder(encoder_pin):
    if encoder_pin == MOTOR1_ENC_A:
        return encoder_count1
    elif encoder_pin == MOTOR2_ENC_A:
        return encoder_count2

def update_motor1(target_speed):
    current_speed1 = read_encoder(MOTOR1_ENC_A)
    pwm1 = pid_motor1.compute(current_speed1)
    motor1_pwm.ChangeDutyCycle(max(0, min(100, pwm1)))

def update_motor2(target_speed):
    current_speed2 = read_encoder(MOTOR2_ENC_A)
    pwm2 = pid_motor2.compute(current_speed2)
    motor2_pwm.ChangeDutyCycle(max(0, min(100, pwm2)))

def cleanup():
    GPIO.cleanup()

# Main control loop
try:
    while True:
        target_speed = 50  # Example target speed
        update_motor1(target_speed)
        update_motor2(target_speed)
        time.sleep(0.01)
except KeyboardInterrupt:
    cleanup()

