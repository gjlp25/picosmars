# NewSMARS Robot Implementation

This implementation combines the best aspects of the picosmars and own_code implementations, using the HC-SR04 ultrasonic sensor for distance measurement.

## Features

- Object-oriented design with clean abstractions
- HC-SR04 ultrasonic distance sensor support
- Continuous and duration-based movement controls
- Obstacle avoidance functionality
- Basic movement testing routine

## Hardware Requirements

- Raspberry Pi Pico
- HC-SR04 Ultrasonic Distance Sensor
- Motor Driver (MX1508 or similar)
- DC Motors (2x)

## Pin Configuration

Default pin assignments:
- Motor A Forward: GPIO 18
- Motor A Reverse: GPIO 19
- Motor B Forward: GPIO 20
- Motor B Reverse: GPIO 21
- HC-SR04 Trigger: GPIO 17 
- HC-SR04 Echo: GPIO 16

## Usage

1. Upload the following files to your Raspberry Pi Pico:
   - rangefinder.py
   - smars.py
   - main.py
2. After uploading, the Pico will automatically run main.py
3. By default, it runs the obstacle avoidance demo
4. To test basic movements instead:
   - Edit main.py 
   - Comment out `main()`
   - Uncomment `test_movements()`
   - Upload the modified main.py

## Files

- `rangefinder.py`: HC-SR04 sensor driver
- `smars.py`: Main robot control class
- `main.py`: Demo program and movement tests
- `test_sensor.py`: Standalone distance sensor test program
- `autonomous.py`: Autonomous driving modes

## Autonomous Operation

The robot supports three autonomous driving modes:

1. Random Explorer:
   - Moves randomly while avoiding obstacles
   - Makes occasional random turns
   - Good for open area exploration

2. Wall Follower:
   - Maintains constant distance from walls
   - Follows walls while avoiding collisions
   - Useful for room perimeter mapping

3. Area Coverage:
   - Systematic back-and-forth pattern
   - Attempts to cover entire areas
   - Good for scanning/cleaning applications

To use autonomous modes:
1. Upload all files to your Pico
2. Run autonomous.py
3. Select desired mode (1-3)
4. Press Ctrl+C to stop

Configuration options in autonomous.py:
```python
controller = AutonomousController(robot)
controller.wall_follow_distance = 15  # cm
controller.obstacle_threshold = 10    # cm
controller.turn_duration = 0.5       # seconds
controller.move_duration = 0.5       # seconds
controller.scan_wait = 0.1          # seconds
```

## Testing the Distance Sensor

If you want to test just the HC-SR04 sensor before using the full robot:

1. Upload these files to your Pico:
   - rangefinder.py
   - test_sensor.py

2. Run test_sensor.py to see continuous distance readings:
   - Shows distances in both cm and mm
   - Displays a visual bar indicator
   - Warns when objects are very close
   
3. For a quick single reading test:
   - Edit test_sensor.py
   - Comment out `test_distance_sensor()`
   - Uncomment `test_single_reading()`

## Testing WiFi Connectivity

Before implementing web control, you can test your WiFi connectivity. Two test files are provided:

### Basic WiFi Test (test_wifi_basic.py)
For basic connection testing:
1. Upload test_wifi_basic.py to your Pico W
2. Edit WiFi credentials:
   ```python
   SSID = 'YourWiFiName'
   PASSWORD = 'YourWiFiPassword'
   ```
3. Run test_wifi_basic.py

This test will:
- Show if WiFi is active
- Scan for your network
- Show signal strength
- Try to connect
- Display detailed network info if successful
- Provide debugging info if connection fails

### Full WiFi Test (test_wifi.py)
For testing both connection and web server:
1. Upload test_wifi.py to your Pico W
2. Edit WiFi credentials as above
3. Run test_wifi.py

This test includes:
- All basic connection tests
- Web server setup
- Test webpage serving

If you're having connection issues:
1. Try test_wifi_basic.py first
2. Check the network scan results
3. Verify signal strength
4. If needed, move closer to your WiFi router
5. Restart your Pico W if connection fails

## Example Code

Basic usage example:
```python
# Save as your_program.py
from smars import SMARS

# Create robot instance
robot = SMARS()

# Basic movements
robot.forward(2)    # Move forward for 2 seconds
robot.backward(1)   # Move backward for 1 second
robot.turnleft(1)   # Turn left for 1 second
robot.turnright(1)  # Turn right for 1 second
robot.stop()        # Stop all motors

# Get distance reading
distance = robot.distance
print(f"Distance: {distance} cm")

# Check for obstacles
if robot.check_obstacle(threshold_cm=10):
    print("Obstacle detected!")
```

## Customization

You can customize pin assignments when creating the SMARS instance:

```python
robot = SMARS(
    trigger_pin=17,     # HC-SR04 trigger pin
    echo_pin=16,        # HC-SR04 echo pin
    motor_a_forward=18, # Motor A forward pin
    motor_a_reverse=19, # Motor A reverse pin
    motor_b_forward=20, # Motor B forward pin
    motor_b_reverse=21  # Motor B reverse pin
)
