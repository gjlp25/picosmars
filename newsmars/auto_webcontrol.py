import time
import socket
import random
from newsmars.main import WebController
from smars import SMARS

class SimulatedSMARS:
    """Simulated SMARS robot for testing without hardware."""
    def __init__(self):
        self.name = "SimulatedSMARS"
        self._distance = 50  # Start with 50cm distance
        self._moving_forward = False
        
    def forward(self, duration=None):
        self._moving_forward = True
        self._distance = max(5, self._distance - 5)  # Move closer to obstacles
        if duration:
            time.sleep(duration)
            self._moving_forward = False
            
    def backward(self, duration=None):
        self._moving_forward = False
        self._distance = min(100, self._distance + 10)  # Move away from obstacles
        if duration:
            time.sleep(duration)
            
    def turnleft(self, duration=None):
        if duration:
            time.sleep(duration)
            
    def turnright(self, duration=None):
        if duration:
            time.sleep(duration)
            
    def stop(self):
        self._moving_forward = False
        
    @property
    def distance(self):
        # Simulate more realistic distance changes
        if self._moving_forward:
            # When moving forward, gradually decrease distance
            self._distance = max(5, self._distance - 1)
        
        # Add small random variations to simulate sensor noise
        variation = (random.random() - 0.5) * 2
        return max(5, min(100, self._distance + variation))

class AutoWebController(WebController):
    def __init__(self, smars, ssid, password):
        """Initialize AutoWebController with SMARS robot instance and WiFi credentials."""
        super().__init__(smars, ssid, password)
        self.current_movement = "Stopped"
        self.autonomous_mode = False
        self.obstacle_threshold = 10  # cm
        self.last_action_time = time.time()
        
    def update_movement_state(self, state):
        """Update the current movement state."""
        self.current_movement = state
        self.last_action_time = time.time()
        
    def handle_request(self, request):
        """Handle incoming web requests with autonomous mode support."""
        if request == '/toggleauto?':
            self.autonomous_mode = not self.autonomous_mode
            self.smars.stop()
            self.current_movement = "Stopped"
            return
            
        if not self.autonomous_mode:
            # Handle manual control requests
            if request == '/forward?':
                self.smars.forward(None if self.continuous_mode else 0.5)
                self.update_movement_state("Forward")
            elif request == '/backward?':
                self.smars.backward(None if self.continuous_mode else 0.5)
                self.update_movement_state("Backward")
            elif request == '/left?':
                self.smars.turnleft(None if self.continuous_mode else 0.5)
                self.update_movement_state("Turning Left")
            elif request == '/right?':
                self.smars.turnright(None if self.continuous_mode else 0.5)
                self.update_movement_state("Turning Right")
            elif request == '/stop?':
                self.smars.stop()
                self.update_movement_state("Stopped")
            elif request == '/togglemode?':
                self.continuous_mode = not self.continuous_mode
                self.smars.stop()
                self.update_movement_state("Stopped")
    
    def autonomous_control(self):
        """Perform one cycle of autonomous control."""
        if not self.autonomous_mode:
            return
            
        distance = self.smars.distance
        if distance is None:
            self.smars.stop()
            self.update_movement_state("Error: Sensor Reading Failed")
            return
            
        # Check if enough time has passed since last action
        if time.time() - self.last_action_time < 0.1:
            return
            
        if distance < self.obstacle_threshold:
            self.smars.backward(1)
            self.update_movement_state("Backward - Avoiding Obstacle")
            time.sleep(1)
            self.smars.turnright(1)
            self.update_movement_state("Turning Right - Avoiding Obstacle")
            time.sleep(1)
        else:
            self.smars.forward()
            self.update_movement_state("Forward - Autonomous")
    
    def generate_webpage(self):
        """Generate the HTML for the enhanced control interface."""
        distance = self.smars.distance
        distance_str = f"{distance:.1f}" if distance is not None else "Error"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SMARS Robot Control</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ 
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    text-align: center;
                }}
                .dashboard {{
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .status {{
                    background: #f0f0f0;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .controls {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 10px;
                    margin-bottom: 20px;
                }}
                .btn {{
                    background: #007bff;
                    color: white;
                    border: none;
                    padding: 20px;
                    font-size: 18px;
                    border-radius: 5px;
                    cursor: pointer;
                    min-height: 80px;
                }}
                .btn:hover {{ background: #0056b3; }}
                .stop {{ background: #dc3545; }}
                .stop:hover {{ background: #bd2130; }}
                .mode {{ background: #28a745; }}
                .mode:hover {{ background: #218838; }}
                .autonomous {{ background: #17a2b8; }}
                .autonomous:hover {{ background: #138496; }}
                .active {{ border: 3px solid #ffc107; }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="status">
                    <h2>SMARS Robot Status</h2>
                    <p>Distance: {distance_str} cm</p>
                    <p>Current Movement: {self.current_movement}</p>
                    <p>Control Mode: {"Autonomous" if self.autonomous_mode else "Manual"}</p>
                    <p>Movement Mode: {"Continuous" if self.continuous_mode else "Single"}</p>
                </div>
                
                <div class="controls">
                    <div></div>
                    <form action="./forward">
                        <input type="submit" value="Forward" class="btn" 
                               {"disabled" if self.autonomous_mode else ""}>
                    </form>
                    <div></div>
                    
                    <form action="./left">
                        <input type="submit" value="Left" class="btn"
                               {"disabled" if self.autonomous_mode else ""}>
                    </form>
                    <form action="./stop">
                        <input type="submit" value="STOP" class="btn stop">
                    </form>
                    <form action="./right">
                        <input type="submit" value="Right" class="btn"
                               {"disabled" if self.autonomous_mode else ""}>
                    </form>
                    
                    <div></div>
                    <form action="./backward">
                        <input type="submit" value="Backward" class="btn"
                               {"disabled" if self.autonomous_mode else ""}>
                    </form>
                    <div></div>
                </div>
                
                <form action="./togglemode" style="margin-bottom: 10px;">
                    <input type="submit" value="Toggle Movement Mode" 
                           class="btn mode" {"disabled" if self.autonomous_mode else ""}>
                </form>
                
                <form action="./toggleauto">
                    <input type="submit" 
                           value="Toggle Autonomous Mode" 
                           class="btn autonomous {" active" if self.autonomous_mode else ""}">
                </form>
            </div>
            
            <script>
                // Auto-refresh status every second
                setInterval(function() {{
                    location.reload();
                }}, 1000);
            </script>
        </body>
        </html>
        """
        return str(html)
    
    def serve(self):
        """Start the web server with autonomous control support."""
        ip = self.connect_wifi()
        if not ip:
            print("Cannot start web server - WiFi connection failed")
            return
            
        try:
            addr = (ip, 80)
            connection = socket.socket()
            # Allow address/port reuse
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                connection.bind(addr)
            except OSError as e:
                print(f"Port 80 in use, waiting 10 seconds...")
                time.sleep(10)  # Wait for potential cleanup
                connection.bind(addr)  # Try again
            connection.listen(1)
            print(f'\nWeb server running at http://{ip}')
            print('Use a web browser to control your robot')
            print('Press Ctrl+C to stop')
            
            last_auto_check = time.time()
            
            while True:
                # Quick autonomous control check if needed
                if self.autonomous_mode and time.time() - last_auto_check > 0.1:
                    self.autonomous_control()
                    last_auto_check = time.time()
                
                client = connection.accept()[0]
                request = client.recv(1024)
                request = str(request)
                
                try:
                    request = request.split()[1]
                    self.handle_request(request)
                except (IndexError, KeyError):
                    pass
                
                html = self.generate_webpage()
                response = f"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n{html}"
                client.send(response.encode())
                client.close()
                
        except KeyboardInterrupt:
            print('\nShutting down...')
            self.smars.stop()
        except Exception as e:
            print(f'\nError: {str(e)}')
        finally:
            try:
                connection.close()
            except:
                pass
            self.smars.stop()

def main():
    """Example usage of AutoWebController."""
    try:
        # Try to create real SMARS robot instance
        try:
            robot = SMARS()
            print("Using real SMARS robot")
        except:
            # Fall back to simulation if hardware not available
            robot = SimulatedSMARS()
            print("Using simulated SMARS robot")
        
        # Create and start web controller
        controller = AutoWebController(
            smars=robot,
            ssid='WiCaRo_IoT',     # Change to your WiFi name
            password='Test@2021'    # Change to your WiFi password
        )
        
        # Start web server
        controller.serve()
        
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == '__main__':
    main()
