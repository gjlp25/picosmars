import time
from smars import SMARS

def main():
    """
    Main program demonstrating SMARS robot capabilities
    with continuous obstacle avoidance.
    """
    robot = None
    try:
        # Create SMARS robot instance with default pin configuration
        robot = SMARS()
        print(f"Initialized {robot.name}")
        print("Starting obstacle avoidance demo...")
        
        while True:
            # Get current distance
            distance = robot.distance
            
            if distance is not None:
                print(f"Distance: {distance:.1f} cm")
                
                if distance < 10:
                    # Obstacle detected - back up and turn
                    print("Obstacle detected!")
                    robot.backward(1)
                    robot.turnright(1)
                else:
                    # Clear path - move forward
                    robot.forward()
            else:
                # Error in distance measurement - stop and wait
                print("Error reading distance sensor")
                robot.stop()
                time.sleep(0.5)
                
            time.sleep(0.1)  # Small delay between measurements
            
    except KeyboardInterrupt:
        # Clean shutdown on Ctrl+C
        print("\nStopping robot")
        robot.stop()
    except Exception as e:
        # Handle other errors gracefully
        print(f"\nError: {e}")
        try:
            robot.stop()
        except:
            pass  # In case robot wasn't initialized

def test_movements():
    """
    Simple test routine to verify basic movements.
    """
    robot = None
    try:
        robot = SMARS()
        print(f"Testing {robot.name} movements")
        
        # Test forward movement
        print("Testing forward movement...")
        robot.forward(2)
        time.sleep(1)
        
        # Test backward movement
        print("Testing backward movement...")
        robot.backward(2)
        time.sleep(1)
        
        # Test turning left
        print("Testing left turn...")
        robot.turnleft(2)
        time.sleep(1)
        
        # Test turning right
        print("Testing right turn...")
        robot.turnright(2)
        time.sleep(1)
        
        # Test distance sensor
        print("\nTesting distance sensor...")
        for _ in range(5):
            distance = robot.distance
            if distance is not None:
                print(f"Distance: {distance:.1f} cm")
            else:
                print("Error reading distance")
            time.sleep(0.5)
        
        print("\nTest complete")
    except Exception as e:
        print(f"\nError during test: {e}")
        if robot:
            robot.stop()

if __name__ == "__main__":
    # Run the main program
    # Uncomment test_movements() to run movement tests instead
    main()
    # test_movements()
