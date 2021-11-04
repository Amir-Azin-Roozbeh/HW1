from controller import Robot, Motor, GPS, Compass
import matplotlib.pyplot as plt
import math
import numpy as np
from sympy import symbols, Eq, solve

TIME_STEP = 64

MAX_SPEED = 6.28

WHEEL_RADIUS = 0.0205

# -----------------------------------------------

def my_plot(xlabel: str, ylabel: str, color: str, title: str, x_axis, y_axis):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x_axis, y_axis, color=color)
    plt.title(title)
    plt.show()

# -------------------------------------------------

def inverse_kinematics(case: int):
    
    if case == 1:
        print('Case1: Linear_velocity = const, angular_velocity = 0')
        x_dot = 1
        y_dot = 1
        theta_dot = 0
        second_matrix = np.array([x_dot, y_dot, theta_dot])
        r_theta = np.array([[np.cos(0), np.sin(0), 0],[-np.sin(0), np.cos(0), 0], [0, 0, 1]])
        
        result = np.matmul(r_theta, np.transpose(second_matrix))
        
        # Y_dot_R = 0; in order not to slip
        result[1] = 0
        print('result: ', result)
 
 
    elif case == 2:
        print('Case2: Linear_velocity = 0, angular_velocity = const')
        x_dot = 0
        y_dot = 0
        theta_dot = 1
        second_matrix = np.array([x_dot, y_dot, theta_dot])
        r_theta = np.array([[np.cos(math.pi/4), np.sin(math.pi/4), 0],[-np.sin(math.pi/4), np.cos(math.pi/4), 0], [0, 0, 1]])
        
        result = np.matmul(r_theta, np.transpose(second_matrix))
        
        # Y_dot_R = 0; in order not to slip
        result[1] = 0
        print('result: ', result)
    
    else:
        print('Unsupported')
    
# ----------------------------------------------

def solve_equation(x_dot_r, theta_dot_r):
    pi_1_dot, pi_2_dot = symbols('x,y')
    
    eq1 = Eq(((WHEEL_RADIUS)/2) * (x + y), x_dot_r)
    eq2 = Eq(((WHEEL_RADIUS)/2) * (x - y), theta_dot_r)
    
    solve((eq1, eq2), (pi_1_dot, pi_2_dot))
    
    return pi_1_dot, pi_2_dot
    
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
    
    inverse_kinematics(1)
    while robot.step(TIME_STEP) != -1 and counter != 100:
        time.append(counter)
        counter += 1
        
        gps_val = gps.getValues()
        x_axis.append(gps_val[0])
        y_axis.append(gps_val[1])
        
        res = get_bearing_in_degrees(compass)
        theta.append(res)
        
      
        
   
