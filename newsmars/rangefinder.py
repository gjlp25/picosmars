from machine import Pin, time_pulse_us
import time

class HCSR04:
    """
    HC-SR04 ultrasonic distance sensor driver for MicroPython.
    Provides a clean abstraction similar to VL53L0X implementation.
    """
    """
    HC-SR04 ultrasonic distance sensor driver for MicroPython.
    Provides a clean abstraction similar to VL53L0X implementation.
    """
    def __init__(self, trigger_pin=17, echo_pin=16):
        """
        Initialize the HC-SR04 sensor.
        
        Args:
            trigger_pin (int): GPIO pin number for trigger (default: 17)
            echo_pin (int): GPIO pin number for echo (default: 16)
        """
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.trigger.off()  # Initialize trigger pin to low

    def measure_distance(self):
        """
        Measure the distance to an object.
        
        Returns:
            float: Distance in centimeters, or None if measurement failed
        """
        # Clear trigger
        self.trigger.off()
        time.sleep_us(2)
        
        # Send trigger pulse
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()
        
        try:
            # Get pulse duration with timeout of 30ms
            duration = time_pulse_us(self.echo, 1, 30000)
            
            if duration < 0:
                return None
            
            # Calculate distance in centimeters
            # Speed of sound = 343m/s = 34300cm/s
            # Time is in microseconds, distance is half of total path
            # Formula: (duration * 34300) / (2 * 1000000)
            distance = duration * 0.01715  # Simplified calculation
            return distance
            
        except OSError:
            # Return None if measurement times out
            return None

    def measure_distance_mm(self):
        """
        Measure the distance in millimeters.
        
        Returns:
            float: Distance in millimeters, or None if measurement failed
        """
        distance_cm = self.measure_distance()
        if distance_cm is not None:
            return distance_cm * 10
        return None

    def check_obstacle(self, threshold_cm=10):
        """
        Check if there is an obstacle within the specified threshold distance.
        
        Args:
            threshold_cm (float): Distance threshold in centimeters
            
        Returns:
            bool: True if obstacle detected, False otherwise
        """
        distance = self.measure_distance()
        if distance is not None:
            return distance <= threshold_cm
        return False
