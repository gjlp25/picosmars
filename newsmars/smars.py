from machine import Pin
from time import sleep
from rangefinder import HCSR04

class SMARS:
    """
    SMARS (Screwless/Screwed Modular Assemblable Robotic System) robot control class.
    Adapted from original picosmars implementation with HC-SR04 sensor support.
    """
    
    def __init__(self, name=None, trigger_pin=17, echo_pin=16,
                 motor_a_forward=18, motor_a_reverse=19,
                 motor_b_forward=20, motor_b_reverse=21):
        """
        Initialize the SMARS robot.
        
        Args:
            name (str): Robot name
            trigger_pin (int): HC-SR04 trigger pin
            echo_pin (int): HC-SR04 echo pin
            motor_a_forward (int): Motor A forward control pin
            motor_a_reverse (int): Motor A reverse control pin
            motor_b_forward (int): Motor B forward control pin
            motor_b_reverse (int): Motor B reverse control pin
            
        Raises:
            RuntimeError: If initialization of any component fails
        """

        try:
            # Set robot name
            self.name = name if name else "PicoSMARS"
            
            # Initialize motors
            self.motor_a_forward = Pin(motor_a_forward, Pin.OUT)
            self.motor_a_reverse = Pin(motor_a_reverse, Pin.OUT)
            self.motor_b_forward = Pin(motor_b_forward, Pin.OUT)
            self.motor_b_reverse = Pin(motor_b_reverse, Pin.OUT)
            
            # Initialize distance sensor
            self.range_finder = HCSR04(trigger_pin, echo_pin)
            
            # Test distance sensor
            if self.distance is None:
                raise RuntimeError("Failed to get reading from distance sensor")
        except Exception as e:
            # Cleanup on initialization failure
            self.cleanup()
            raise RuntimeError(f"Failed to initialize SMARS robot: {str(e)}")
            
        # Ensure motors are stopped
        self.stop()
    
    def forward(self, duration=None):
        """Move forward. If duration is None, move continuously."""
        self.motor_a_forward.value(1)
        self.motor_b_forward.value(1)
        self.motor_a_reverse.value(0)
        self.motor_b_reverse.value(0)
        
        if duration:
            sleep(duration)
            self.stop()
    
    def backward(self, duration=None):
        """Move backward. If duration is None, move continuously."""
        self.motor_a_forward.value(0)
        self.motor_b_forward.value(0)
        self.motor_a_reverse.value(1)
        self.motor_b_reverse.value(1)
        
        if duration:
            sleep(duration)
            self.stop()
    
    def turnleft(self, duration=None):
        """Turn left. If duration is None, turn continuously."""
        self.motor_a_forward.value(1)
        self.motor_b_forward.value(0)
        self.motor_a_reverse.value(0)
        self.motor_b_reverse.value(1)
        
        if duration:
            sleep(duration)
            self.stop()
    
    def turnright(self, duration=None):
        """Turn right. If duration is None, turn continuously."""
        self.motor_a_forward.value(0)
        self.motor_b_forward.value(1)
        self.motor_a_reverse.value(1)
        self.motor_b_reverse.value(0)
        
        if duration:
            sleep(duration)
            self.stop()
    
    def stop(self):
        """Stop all motors."""
        self.motor_a_forward.value(0)
        self.motor_b_forward.value(0)
        self.motor_a_reverse.value(0)
        self.motor_b_reverse.value(0)
    
    @property
    def distance(self):
        """Get current distance measurement in centimeters."""
        return self.range_finder.measure_distance()
    
    def check_obstacle(self, threshold_cm=10):
        """Check if there is an obstacle within threshold distance."""
        return self.range_finder.check_obstacle(threshold_cm)
    
    def avoid_obstacles(self, threshold_cm=10):
        """
        Basic obstacle avoidance behavior.
        Returns True if obstacle was avoided, False if no obstacle.
        """
        if self.check_obstacle(threshold_cm):
            self.backward(0.5)  # Back up for 0.5 seconds
            self.turnright(1)   # Turn right for 1 second
            return True
        return False
        
    def cleanup(self):
        """Clean up resources and ensure motors are stopped."""
        try:
            self.stop()
        except:
            pass
        # Any additional cleanup can be added here
        
    def __del__(self):
        """Destructor to ensure cleanup on object deletion."""
        self.cleanup()
