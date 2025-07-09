# TwoServoTest.py
# Simple test code for servos 0 and 1 on the Kitronik Simply Robotics board
# Demonstrates individual control and synchronized movement

from SimplyRobotics import KitronikSimplyRobotics
import utime

# Create board instance
board = KitronikSimplyRobotics()

print("Starting servo 0 and 1 test...")
print("Test 1: Individual servo control")

# Test 1: Individual servo control
# Move servo 0 while servo 1 stays centered
print("Moving servo 0 from 0° to 180°, servo 1 stays at 90°")
board.servos[1].goToPosition(90)  # Keep servo 1 centered
utime.sleep(1)

for angle in range(0, 181, 10):
    board.servos[0].goToPosition(angle)
    utime.sleep_ms(100)

utime.sleep(1)

# Move servo 1 while servo 0 stays centered  
print("Moving servo 1 from 0° to 180°, servo 0 stays at 90°")
board.servos[0].goToPosition(90)  # Keep servo 0 centered
utime.sleep(1)

for angle in range(0, 181, 10):
    board.servos[1].goToPosition(angle)
    utime.sleep_ms(100)

utime.sleep(2)

print("Test 2: Synchronized movement")

# Test 2: Synchronized movement - both servos move together
while True:
    print("Sweeping both servos from 0° to 180°")
    for angle in range(0, 181, 5):
        board.servos[0].goToPosition(angle)
        board.servos[1].goToPosition(angle)
        utime.sleep_ms(50)
    
    print("Sweeping both servos from 180° to 0°")
    for angle in range(180, -1, -5):
        board.servos[0].goToPosition(angle)
        board.servos[1].goToPosition(angle)
        utime.sleep_ms(50)
    
    utime.sleep(1)
