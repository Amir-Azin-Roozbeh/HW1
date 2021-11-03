from controller import Robot, Motor, GPS
import matplotlib.pyplot as plt

TIME_STEP = 64

MAX_SPEED = 6.28

def my_plot(xlabel: str, ylabel: str, color: str, title: str, x_axis, y_axis):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x_axis, y_axis, color=color)
    plt.title(title)
    plt.show()



def set_wheels(leftMotor, rightMotor, pi_1, pi_2):
    if pi_1 == pi_2:
        leftMotor.setVelocity(1 * MAX_SPEED)
        rightMotor.setVelocity(1 * MAX_SPEED)
        movement_type = 'pi_1 == pi_2'
        
    elif pi_1 == -pi_2:
        leftMotor.setVelocity(1 * MAX_SPEED)
        rightMotor.setVelocity(-1 * MAX_SPEED)
        movement_type = 'pi_1 == -pi_2'
        
    elif pi_1 != 0 and pi_2 == 0:
        leftMotor.setVelocity(1 * MAX_SPEED)
        rightMotor.setVelocity(0 * MAX_SPEED)
        movement_type = 'pi_2 == 0'
        
    elif pi_1 < pi_2:
        leftMotor.setVelocity(1 * MAX_SPEED)
        rightMotor.setVelocity(0.5 * MAX_SPEED)        
        movement_type = 'pi_1 < pi_2'
 
    else:
        movement_type = 'unsupported'
        
    return movement_type

if __name__ == '__main__':
    robot = Robot()
    gps = GPS('gps')
    gps.enable(1000)
    leftMotor = robot.getDevice('left wheel motor')
    rightMotor = robot.getDevice('right wheel motor')
    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))
    
    counter = 0
    x_axis = []
    y_axis = []
    
    movement_type = set_wheels(leftMotor, rightMotor, pi_1 = 1, pi_2 = -1)
    print('movment_type: ', movement_type)
    
    while robot.step(TIME_STEP) != -1 and counter != 5000:
        res = gps.getValues()
        x_axis.append(res[0])
        y_axis.append(res[1])
        counter += 10
    print(len(x_axis))
    my_plot('X axis', 'Y axis', 'green', movement_type, x_axis, y_axis)