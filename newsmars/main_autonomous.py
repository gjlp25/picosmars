from machine import Pin
import time
import random
from rangefinder import HCSR04
from SimplyRobotics import KitronikSimplyRobotics

class AutonomousRobot:
    """
    Autonomous robot that uses HC-SR04 rangefinder for obstacle avoidance.
    Uses simple behaviors: move forward, turn when obstacle detected.
    """
    
    def __init__(self, obstacle_distance=20, speed=50):
        """
        Initialize the autonomous robot.
        
        Args:
            obstacle_distance (int): Distance in cm to trigger obstacle avoidance
            speed (int): Motor speed (0-100)
        """
        # Initialize hardware
        self.robot = KitronikSimplyRobotics(centreServos=False)  # Don't center servos
        self.sensor = HCSR04()  # Using default pins 17 (trigger) and 16 (echo)
        
        # Robot parameters
        self.obstacle_distance = obstacle_distance
        self.speed = speed
        self.is_running = False
        
        # Movement timing
        self.turn_time = 0.5  # Time to turn in seconds
        self.backup_time = 0.3  # Time to backup when obstacle detected
        
        print(f"Robot initialized - Obstacle distance: {obstacle_distance}cm, Speed: {speed}")
    
    def move_forward(self):
        """Move robot forward using both motors."""
        self.robot.motors[0].on("f", self.speed)  # Motor 0 forward
        self.robot.motors[3].on("f", self.speed)  # Motor 3 forward
    
    def move_backward(self):
        """Move robot backward using both motors."""
        self.robot.motors[0].on("r", self.speed)  # Motor 0 reverse
        self.robot.motors[3].on("r", self.speed)  # Motor 3 reverse
    
    def turn_left(self):
        """Turn robot left by spinning motors in opposite directions."""
        self.robot.motors[0].on("r", self.speed)  # Motor 0 reverse
        self.robot.motors[3].on("f", self.speed)  # Motor 3 forward
    
    def turn_right(self):
        """Turn robot right by spinning motors in opposite directions."""
        self.robot.motors[0].on("f", self.speed)  # Motor 0 forward
        self.robot.motors[3].on("r", self.speed)  # Motor 3 reverse
    
    def stop(self):
        """Stop all motors."""
        self.robot.motors[0].off()
        self.robot.motors[3].off()
    
    def get_distance(self):
        """Get distance reading from sensor with error handling."""
        distance = self.sensor.measure_distance()
        if distance is None:
            # If sensor fails, assume obstacle is close for safety
            return 0
        return distance
    
    def avoid_obstacle(self):
        """
        Obstacle avoidance behavior:
        1. Stop and backup slightly
        2. Turn in a random direction
        3. Check if path is clear
        """
        print("Obstacle detected! Avoiding...")
        
        # Stop and backup
        self.stop()
        time.sleep(0.1)
        
        print("Backing up...")
        self.move_backward()
        time.sleep(self.backup_time)
        
        # Stop and choose turn direction
        self.stop()
        time.sleep(0.1)
        
        # Random turn direction to avoid getting stuck in corners
        if random.random() < 0.5:
            print("Turning left...")
            self.turn_left()
        else:
            print("Turning right...")
            self.turn_right()
        
        # Turn for specified time
        time.sleep(self.turn_time)
        
        # Stop turning
        self.stop()
        time.sleep(0.1)
        
        # Check if new path is clear
        new_distance = self.get_distance()
        if new_distance < self.obstacle_distance:
            print(f"Path still blocked ({new_distance:.1f}cm), turning more...")
            # Turn a bit more if still blocked
            self.turn_right()
            time.sleep(self.turn_time * 0.5)
            self.stop()
            time.sleep(0.1)
    
    def run_autonomous(self):
        """
        Main autonomous driving loop.
        Continuously moves forward and avoids obstacles.
        """
        print("Starting autonomous mode...")
        print("Press Ctrl+C to stop")
        
        self.is_running = True
        
        try:
            while self.is_running:
                # Get current distance
                distance = self.get_distance()
                
                # Display current status
                print(f"Distance: {distance:.1f}cm", end=" - ")
                
                # Check if obstacle is detected
                if distance < self.obstacle_distance:
                    print("OBSTACLE!")
                    self.avoid_obstacle()
                else:
                    print("Path clear, moving forward")
                    self.move_forward()
                
                # Small delay to prevent sensor overload
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nAutonomous mode stopped by user")
        except Exception as e:
            print(f"\nError in autonomous mode: {str(e)}")
        finally:
            self.stop()
            self.is_running = False
            print("Robot stopped")
    
    def test_movements(self):
        """Test all movement functions."""
        print("Testing robot movements...")
        
        movements = [
            ("Forward", self.move_forward),
            ("Backward", self.move_backward),
            ("Left", self.turn_left),
            ("Right", self.turn_right)
        ]
        
        for name, movement in movements:
            print(f"Testing {name}...")
            movement()
            time.sleep(1)
            self.stop()
            time.sleep(0.5)
        
        print("Movement test complete")
    
    def test_sensor(self):
        """Test the distance sensor."""
        print("Testing distance sensor...")
        
        for i in range(10):
            distance = self.get_distance()
            print(f"Reading {i+1}: {distance:.1f}cm")
            time.sleep(0.5)
        
        print("Sensor test complete")

def main():
    """Main function to run the autonomous robot."""
    
    # Configuration
    OBSTACLE_DISTANCE = 15  # cm - distance to trigger avoidance
    ROBOT_SPEED = 20        # 0-100 - motor speed
    
    # Create robot instance
    robot = AutonomousRobot(
        obstacle_distance=OBSTACLE_DISTANCE,
        speed=ROBOT_SPEED
    )
    
    # Menu for different modes
    print("\n=== Autonomous Robot Control ===")
    print("1. Run autonomous mode")
    print("2. Test movements")
    print("3. Test sensor")
    print("4. Single distance reading")
    
    try:
        choice = input("Enter choice (1-4): ")
        
        if choice == "1":
            robot.run_autonomous()
        elif choice == "2":
            robot.test_movements()
        elif choice == "3":
            robot.test_sensor()
        elif choice == "4":
            distance = robot.get_distance()
            print(f"Current distance: {distance:.1f}cm")
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        robot.stop()

if __name__ == "__main__":
    main()