from machine import Pin
import time
from rangefinder import HCSR04

def test_distance_sensor():
    """
    Test program for the HC-SR04 ultrasonic distance sensor.
    Continuously reads and displays distance measurements.
    """
    print("HC-SR04 Distance Sensor Test")
    print("---------------------------")
    
    # Create sensor instance with default pins (trigger=17, echo=16)
    try:
        sensor = HCSR04()
        print("Sensor initialized successfully")
        print("\nStarting measurements (Ctrl+C to stop)...")
        print("Distance will be shown in both cm and mm")
        
        while True:
            # Get distance in centimeters
            distance_cm = sensor.measure_distance()
            
            # Get distance in millimeters
            distance_mm = sensor.measure_distance_mm()
            
            if distance_cm is not None:
                print(f"Distance: {distance_cm:.1f} cm ({distance_mm:.1f} mm)")
                
                # Show a simple visual indicator
                bars = int(min(distance_cm, 100) / 5)  # Max 20 bars for distances up to 100cm
                print("Distance: " + "█" * bars)
                
                # Check if object is close
                if distance_cm < 10:
                    print("Warning: Object very close!")
            else:
                print("Error: Could not read sensor")
                
            # Wait before next reading
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_single_reading():
    """
    Take a single distance reading.
    Useful for quick sensor verification.
    """
    try:
        sensor = HCSR04()
        distance = sensor.measure_distance()
        if distance is not None:
            print(f"Distance: {distance:.1f} cm")
        else:
            print("Error reading sensor")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Uncomment test_single_reading() and comment out test_distance_sensor()
    # if you just want a single reading
    test_distance_sensor()
    # test_single_reading()
