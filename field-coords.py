import math
import motor_control

# Initialize current position and orientation
cur_pos_x = 0
cur_pos_y = 0
orient = 0
x_Sum = 0
y_Sum = 0
z_Sum = 0

# Setting start position
def startPos(sx, sy, so):
    global cur_pos_x, cur_pos_y, orient, x_Sum, y_Sum, z_Sum
    cur_pos_x = sx
    cur_pos_y = sy
    orient = so
    x_Sum = 0
    y_Sum = 0
    z_Sum = 0

# Move to target using pivot turn forwards
def move_to_pivot_forward(x, y):
    moveToForwards(x, y)

# Move to target using pivot turn backwards
def move_to_pivot_backward(x, y):
    moveToBackwards(x, y)

# Move to target using tank turn forwards
def move_to_tank_forward(x, y):
    moveToForwards(x, y)

# Move to target using tank turn backwards
def move_to_tank_backward(x, y):
    moveToBackwards(x, y)

def moveToForwards(x, y):
    global cur_pos_x, cur_pos_y, orient, x_Sum, y_Sum, z_Sum
    new_pos_x = x
    new_pos_y = y

    if cur_pos_x == new_pos_x:
        y_Sum += abs(new_pos_y - cur_pos_y)
        if new_pos_y > cur_pos_y:
            turn(90 - orient)
            forward(new_pos_y - cur_pos_y)
            orient = 90
        elif new_pos_y < cur_pos_y:
            taa = -90 - orient
            if abs(taa) > 181:
                taa = 270 - orient
            turn(taa)
            forward(abs(new_pos_y - cur_pos_y))
            orient = -90
    elif cur_pos_y == new_pos_y:
        x_Sum += abs(new_pos_x - cur_pos_x)
        if new_pos_x > cur_pos_x:
            turn(0 - orient)
            forward(new_pos_x - cur_pos_x)
            orient = 0
        elif new_pos_x < cur_pos_x:
            ta = 180 - orient
            if abs(ta) > 181:
                ta = -180 - orient
            turn(ta)
            forward(abs(new_pos_x - cur_pos_x))
            orient = 180
    else:
        if new_pos_x > cur_pos_x:
            dif_x = new_pos_x - cur_pos_x
            dif_y = new_pos_y - cur_pos_y
            distance = math.sqrt(dif_x ** 2 + dif_y ** 2)
            z_Sum += distance
            angle = math.degrees(math.asin(dif_y / distance))
            turn(angle - orient)
            forward(distance)
            orient = angle
        elif new_pos_x < cur_pos_x:
            dif_x = new_pos_x - cur_pos_x
            dif_y = new_pos_y - cur_pos_y
            distance = math.sqrt(dif_x ** 2 + dif_y ** 2)
            z_Sum += distance
            angle = math.degrees(math.asin(dif_y / distance))
            angle2 = 180 - 2 * angle + angle
            turn(angle2 - orient)
            forward(distance)
            orient = angle2

    cur_pos_x = new_pos_x
    cur_pos_y = new_pos_y

def moveToBackwards(x, y):
    global cur_pos_x, cur_pos_y, orient, x_Sum, y_Sum, z_Sum
    new_pos_x = x
    new_pos_y = y

    if cur_pos_x == new_pos_x:
        y_Sum += abs(new_pos_y - cur_pos_y)
        if new_pos_y > cur_pos_y:
            taaaa = -90 - orient
            if abs(taaaa) > 181:
                taaaa = 270 - orient
            turn(taaaa)
            backward(new_pos_y - cur_pos_y)
            orient = -90
        elif new_pos_y < cur_pos_y:
            taaa = 90 - orient
            if abs(taaa) > 181:
                taaa = -270 - orient
            turn(taaa)
            backward(abs(new_pos_y - cur_pos_y))
            orient = 90
    elif cur_pos_y == new_pos_y:
        x_Sum += abs(new_pos_x - cur_pos_x)
        if new_pos_x > cur_pos_x:
            taaa = 180 - orient
            if abs(taaa) > 181:
                taaa = -180 - orient
            turn(taaa)
            backward(new_pos_x - cur_pos_x)
            orient = 180
        elif new_pos_x < cur_pos_x:
            turn(0 - orient)
            backward(abs(new_pos_x - cur_pos_x))
            orient = 0
    else:
        if new_pos_x < cur_pos_x:
            dif_x = new_pos_x - cur_pos_x
            dif_y = new_pos_y - cur_pos_y
            distance = math.sqrt(dif_x ** 2 + dif_y ** 2)
            z_Sum += distance
            angle = math.degrees(math.asin(dif_y / distance))
            turn(-angle - orient)
            backward(distance)
            orient = -angle
        elif new_pos_x > cur_pos_x:
            dif_x = new_pos_x - cur_pos_x
            dif_y = new_pos_y - cur_pos_y
            distance = math.sqrt(dif_x ** 2 + dif_y ** 2)
            angle = math.degrees(math.asin(dif_y / distance))
            angle2 = 180 - 2 * angle + angle
            turn(-angle2 - orient)
            z_Sum += distance
            backward(distance)
            orient = -angle2

    cur_pos_x = new_pos_x
    cur_pos_y = new_pos_y

def forward(distance):
    motor_control.update_motor1(50)
    motor_control.update_motor2(50)
    motor_control.read_encoder(24)  # Example encoder pin for motor 1
    motor_control.read_encoder(22)  # Example encoder pin for motor 2

def backward(distance):
    motor_control.update_motor1(-50)
    motor_control.update_motor2(-50)
    motor_control.read_encoder(24)  # Example encoder pin for motor 1
    motor_control.read_encoder(22)  # Example encoder pin for motor 2

def turn(deg):
    # Implementation for turning
    pass

def end():
    print("End of movements.")
    motor_control.cleanup()


