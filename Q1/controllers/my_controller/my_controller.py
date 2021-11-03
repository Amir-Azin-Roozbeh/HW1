from controller import Robot, Motor, GPS, Compass
import matplotlib.pyplot as plt
import math

TIME_STEP = 64

MAX_SPEED = 6.28

# -----------------------------------------------

def my_plot(xlabel: str, ylabel: str, color: str, title: str, x_axis, y_axis):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x_axis, y_axis, color=color)
    plt.title(title)
    plt.show()

# -------------------------------------------------

def set_wheels(leftMotor, rightMotor, pi_1, pi_2):
    leftMotor.setVelocity(pi_1 * MAX_SPEED)
    rightMotor.setVelocity(pi_2 * MAX_SPEED)
        
    if pi_1 == pi_2:
        movement_type = 'pi_1 == pi_2'
        
    elif pi_1 == -pi_2:
        movement_type = 'pi_1 == -pi_2'
        
    elif pi_1 != 0 and pi_2 == 0:
        movement_type = 'pi_2 == 0'
        
    elif pi_1 < pi_2:
        movement_type = 'pi_1 < pi_2'
        
    else:
        movement_type = 'unsupported'
        
    return movement_type
    
# ----------------------------------------------

def get_bearing_in_degrees(compass: Compass):
    north = compass.getValues()
    rad = math.atan2(north[0], north[1])
    bearing = (rad - 1.5708) / math.pi * 180.0
    if (bearing < 0.0):
        bearing += 360.0
    return bearing

# ----------------------------------------------

if __name__ == '__main__':
    
    # Creating Robot
    robot = Robot()
    
    # Creating GPS
    gps = GPS('gps')
    gps.enable(1000)
    
    # Creating Compass
    compass = Compass('compass')
    compass.enable(1000)
    
    # Setting Motor Wheels
    leftMotor = robot.getDevice('left wheel motor')
    rightMotor = robot.getDevice('right wheel motor')
    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))
    
    counter = 0
    time = []
    x_axis = []
    y_axis = []
    theta = []
    
    movement_type = set_wheels(leftMotor, rightMotor, pi_1 = 1, pi_2 = 1)
    print('movment_type: ', movement_type)
    
    while robot.step(TIME_STEP) != -1 and counter != 100:
        time.append(counter)
        counter += 1
        
        gps_val = gps.getValues()
        x_axis.append(gps_val[0])
        y_axis.append(gps_val[1])
        
        res = get_bearing_in_degrees(compass)
        theta.append(res)
       
    my_plot('X_Axis', 'Y_Axis', 'red', movement_type, x_axis, y_axis)
    my_plot('Time', 'Theta', 'green', movement_type, time, theta)