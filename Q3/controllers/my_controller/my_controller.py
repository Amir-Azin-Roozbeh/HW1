from controller import Robot, Motor, GPS, Compass
import matplotlib.pyplot as plt
import math
import numpy as np
from sympy import symbols, Eq, solve
import time

TIME_STEP = 64

MAX_SPEED = 6.28

WHEEL_RADIUS = 0.0205

CHASIS_LENGTH = 0.052

CASE = 1
"""
case1: linear_velocity = const, angluar_velocity = 0
case2: linear_velocity = 0, angular_velocity = const

"""
plot_type1 = 'case1: linear_velocity = const, angluar_velocity = 0' 
plot_type2 = 'case2: linear_velocity = 0, angular_velocity = const'

FLAG = 0

# -----------------------------------------------

def my_plot(xlabel: str, ylabel: str, color: str, title: str, x_axis, y_axis):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x_axis, y_axis, color=color)
    plt.title(title)
    plt.show()

# -------------------------------------------------

def inverse_kinematics(x_dot: int, y_dot: int, theta_dot: int, angle):
    
    r_theta = np.array([[np.cos(angle), np.sin(angle), 0],[-np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    second_matrix = np.array([x_dot, y_dot, theta_dot])
    
    result = np.matmul(r_theta, np.transpose(second_matrix))
    
    # Y_dot_R should be Zero.
    result[1] = 0

    return result
    
# ----------------------------------------------

def solve_equation(x_dot_r, theta_dot_r):
    pi_1_dot, pi_2_dot = symbols('pi_1_dot,pi_2_dot')
    
    eq1 = Eq(((WHEEL_RADIUS)/2) * (pi_1_dot + pi_2_dot), x_dot_r)
    eq2 = Eq(((WHEEL_RADIUS)/(2 * CHASIS_LENGTH)) * (pi_1_dot - pi_2_dot), theta_dot_r)
    
    res = solve((eq1, eq2), (pi_1_dot, pi_2_dot))
    
    return res 
    
# ----------------------------------------------

def get_bearing(compass: Compass):
    north = compass.getValues()
    rad = math.atan2(north[0], north[1])
    return rad

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
    
    velocities = []
    
    if CASE == 1:
        x_dot = -0.1
        y_dot = -0.1
        theta_dot = 0
    else:
        x_dot = 0
        y_dot = 0
        theta_dot = 1
    
    while robot.step(TIME_STEP) != -1 and counter != 100:
        counter += 1
    
        if CASE == 2 or FLAG == 0:
            angle = get_bearing(compass)
        
        if CASE == 1:
            FLAG = 1
  
        interface_vector = inverse_kinematics(x_dot, y_dot, theta_dot, angle)

        pi_dots = solve_equation(interface_vector[0], interface_vector[2])
        for key, value in pi_dots.items():
            velocities.append(value)
         
        leftMotor.setVelocity((int)(velocities[0]) / MAX_SPEED)
        rightMotor.setVelocity((int)(velocities[1])/ MAX_SPEED)
        velocities.clear()
        
        gps_val = gps.getValues()
        x_axis.append(gps_val[0])
        y_axis.append(gps_val[1])
     
    if CASE == 1:
         movement_type = plot_type1
    else:
         movement_type = plot_type2
    my_plot('X_Axis', 'Y_Axis', 'red', movement_type, x_axis, y_axis)

        
