from controller import Robot, Motor, GPS

TIME_STEP = 64

MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()
gps = GPS('gps')
gps.enable(1000)

# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

# set up the motor speeds at 10% of the MAX_SPEED.
leftMotor.setVelocity(0.1 * MAX_SPEED)
rightMotor.setVelocity(0.1 * MAX_SPEED)


while robot.step(TIME_STEP) != -1:
    res = gps.getValues()
    print('res: ', res)
