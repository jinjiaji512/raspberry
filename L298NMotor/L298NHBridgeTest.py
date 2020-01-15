# Autor:	Ingmar Stapel
# Date:		20141229
# Version:	1.0
# Homepage:	www.raspberry-pi-car.com

import sys, tty, termios, os, time, threading
from L298NHBridge import HBridge

speed = 0
angle = 0
speedleft = 0
speedright = 0

Motors = HBridge(17, 18, 27, 22, 23, 24)
# Instructions for when the user has an interface
print("w/s: direction")
print("a/d: steering")
print("q: stops the motors")
print("p: print motor speed (L/R)")
print("x: exit")

# The catch method can determine which key has been pressed
# by the user on the keyboard.
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Infinite loop
# The loop will not end until the user presses the
# exit key 'X' or the program crashes...

def printscreen():
	# Print the motor speed just for interest
	# os.system('clear')
	print("w/s: direction")
	print("a/d: steering")
	print("q: stops the motors")
	print("x: exit")
	print("========== Speed Control ==========")
	print "speed:  ", speed
	print "angle:  ", angle
	print "left motor:  ", speedleft
	print "right motor: ", speedright

def setMotorSpeed():
	# generate the left motor speed and right motor speed with the speed and angle
	global speedleft
	global speedright
	global speed
	global angle
	speedleft = speed - angle * speed 
	speedright = speed + angle * speed
	if speedleft < -1:
		speedleft = -1
	if speedleft > 1:
		speedleft = 1
	if speedright < -1:
		speedright = -1
	if speedright > 1:
		speedright = 1
	Motors.setMotorLeft(speedleft)
	Motors.setMotorRight(speedright)
	printscreen()

def anglexx():
	global angle
	angle = angle * 0.9
	setMotorSpeed()

t = threading.Timer(0.01, anglexx)
t.start()

while True:
    # Keyboard character retrieval method. This method will save
    # the pressed key into the variable char
	char = getch()

	# The car will drive forward when the "w" key is pressed
	if(char == "w"):
		# synchronize after a turning the motor speed
		# accelerate the RaPi car
		speed = speed + 0.1
		if speed > 1:
			speed = 1

	# The car will reverse when the "s" key is pressed
	if(char == "s"):
		speed = speed - 0.1
		if speed < -1:
			speed = -1

	# Stop the motors
	if(char == "q"):
		angle = 0 
		speed = 0


	# The "d" key will toggle the steering right
	if(char == "a"):		
		angle = angle - 0.1
		if angle < -1:
			angle = -1
		
	# The "a" key will toggle the steering left
	if(char == "d"):
		angle = angle + 0.1
		if angle > 1:
			angle = 1

	# The "x" key will break the loop and exit the program
	if(char == "x"):
		angle = 0 
		speed = 0
		setMotorSpeed()
		Motors.exit()
		print("Program Ended")
		break
	
	# The keyboard character variable char has to be set blank. We need
	# to set it blank to save the next key pressed by the user
	char = ""
	setMotorSpeed()
# End
