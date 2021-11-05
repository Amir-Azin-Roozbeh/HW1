from controller import Robot, Motor, GPS, Compass
import matplotlib.pyplot as plt
import numpy as np
import math

TIME_STEP = 64

MAX_SPEED = 5

WHEEL_RADIUS = 0.0205

CHASIS_LENGTH = 0.052

RADIUS = WHEEL_RADIUS

# -----------------------------------------------

def my_plot(xlabel: str, ylabel: str, color: str, title: str, x_axis, y_axis):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x_axis, y_axis, color=color)
    plt.title(title)
    plt.show()

# -------------------------------------------------

def get_bearing(compass: Compass):
    north = compass.getValues()
    rad = math.atan2(north[0], north[1])
    return rad


# ----------------------------------------------

# Question3 Part1
def go_circle(leftMotor, rightMotor):     
    leftMotor.setVelocity(((RADIUS - 2 * CHASIS_LENGTH) * MAX_SPEED))
    rightMotor.setVelocity(RADIUS * MAX_SPEED)

# ----------------------------------------------

# Question3 Part2
def archimedean_spiral(leftMotor, rightMotor, RADIUS): 
    print('RADIUS: ', RADIUS)    
    leftMotor.setVelocity(((RADIUS - 2 * CHASIS_LENGTH) * MAX_SPEED))
    rightMotor.setVelocity(RADIUS * MAX_SPEED)    
    


# ----------------------------------------------

if __name__ == '__main__':
    
    # Creating Robot
    robot = Robot()
    
    # Creating GPS
    gps = GPS('gps')
    gps.enable(10)
    
    # Creating Compass
    compass = Compass('compass')
    compass.enable(10)
    
    # Setting Motor Wheels
    leftMotor = robot.getDevice('left wheel motor')
    rightMotor = robot.getDevice('right wheel motor')
    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))
    
    counter = 0

    x_axis = []
    y_axis = []
    theta = []
    
    go_circle(leftMotor, rightMotor)
    #archimedean_spiral(leftMotor, rightMotor)
    co = 1
    
    while robot.step(TIME_STEP) != -1 and counter != 5000:
        counter += 1
        angle = get_bearing(compass)
        
        gps_val = gps.getValues()
        x_axis.append(gps_val[0])
        y_axis.append(gps_val[1])

        print('location: ', gps_val)
        # Check if the robot has traversed a whole Circle
        if gps_val[0]**2 + gps_val[1]**2 >= RADIUS**2:
            RADIUS += WHEEL_RADIUS
            print(RADIUS) 
        
#        print(angle)
        #archimedean_spiral(leftMotor, rightMotor, RADIUS)
 
        co += math.pi/180

    my_plot('X_Axis', 'Y_Axis', 'red', 'circle', x_axis, y_axis)

        
