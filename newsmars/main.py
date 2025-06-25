import network
import socket
from time import sleep
import machine
import gc
from machine import Pin
from smars import SMARS

# Initialize SMARS robot with default pins
robot = SMARS()

# WiFi Configuration
SSID = 'Your_Network_Name'
PASSWORD = 'Your_WiFi_Password'

# Optional: LED for status indication (built-in LED on Pico 2 W)
status_led = Pin("LED", Pin.OUT)

def move_forward():
    print("Forward")
    robot.forward()
    
def move_backward():
    print("Backward")
    robot.backward()
    
def move_stop():
    print("Stop")
    robot.stop()
    
def move_left():
    print("Left")
    robot.turnleft()
    
def move_right():
    print("Right")
    robot.turnright()

def get_distance():
    """Get current distance from sensor in cm"""
    return robot.distance

def connect_wifi():
    """Connect to WiFi with improved error handling"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if wlan.isconnected():
        print('Already connected to WiFi')
        return wlan.ifconfig()[0]
    
    print(f'Connecting to WiFi: {SSID}')
    wlan.connect(SSID, PASSWORD)
    
    # Wait for connection with timeout
    max_wait = 20
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        status_led.toggle()
        sleep(1)
    
    if wlan.status() != 3:
        status_led.off()
        raise RuntimeError('Network connection failed')
    else:
        status_led.on()
        print('Connected successfully')
        status = wlan.ifconfig()
        print(f'IP: {status[0]}')
        print(f'Subnet: {status[1]}')
        print(f'Gateway: {status[2]}')
        print(f'DNS: {status[3]}')
        return status[0]

def create_socket(ip):
    """Create and bind socket with proper error handling"""
    try:
        addr = socket.getaddrinfo(ip, 80)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        print(f'Web server listening on http://{ip}:80')
        return s
    except Exception as e:
        print(f'Socket creation failed: {e}')
        raise

def get_webpage():
    """Generate HTML webpage with improved styling"""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Pico 2 W Robot Control</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
        }
        .control-btn {
            height: 80px;
            width: 80px;
            font-size: 14px;
            font-weight: bold;
            margin: 5px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        .control-btn:hover {
            background: #45a049;
        }
        .control-btn:active {
            background: #3d8b40;
            transform: scale(0.95);
        }
        .stop-btn {
            background: #f44336;
        }
        .stop-btn:hover {
            background: #da190b;
        }
        table {
            margin: 10px auto;
        }
        .status {
            margin-top: 20px;
            font-size: 12px;
            color: #666;
        }
        .distance {
            margin: 20px 0;
            padding: 10px;
            background: #e8f5e9;
            border-radius: 5px;
            font-size: 16px;
            color: #2e7d32;
        }
        .distance.warning {
            background: #fff3e0;
            color: #e65100;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Robot Control</h1>
        
        <form action="/forward" method="get">
            <input type="submit" value="⬆️ Forward" class="control-btn" />
        </form>
        
        <table>
            <tr>
                <td>
                    <form action="/left" method="get">
                        <input type="submit" value="⬅️ Left" class="control-btn" />
                    </form>
                </td>
                <td>
                    <form action="/stop" method="get">
                        <input type="submit" value="⏹️ Stop" class="control-btn stop-btn" />
                    </form>
                </td>
                <td>
                    <form action="/right" method="get">
                        <input type="submit" value="➡️ Right" class="control-btn" />
                    </form>
                </td>
            </tr>
        </table>
        
        <form action="/back" method="get">
            <input type="submit" value="⬇️ Back" class="control-btn" />
        </form>
        
        <div class="distance" id="distance">
            Distance: -- cm
        </div>
        
        <div class="status">
            <p>Raspberry Pi Pico 2 W - MicroPython v1.25.0</p>
        </div>
    </div>
    
    <script>
        // Auto-refresh distance every 500ms
        setInterval(function() {
            fetch('/distance')
                .then(response => response.text())
                .then(distance => {
                    const distanceDiv = document.getElementById('distance');
                    distanceDiv.textContent = `Distance: ${distance} cm`;
                    distanceDiv.className = distance <= 10 ? 'distance warning' : 'distance';
                })
                .catch(console.error);
        }, 500);
    </script>
</body>
</html>"""
    return html

def handle_request(client):
    """Handle individual client requests with proper HTTP responses"""
    try:
        # Receive request with timeout
        client.settimeout(5.0)
        request = client.recv(1024)
        request_str = request.decode('utf-8')
        
        # Parse the request
        try:
            method, path, protocol = request_str.split('\r\n')[0].split(' ')
        except ValueError:
            path = '/'
        
        print(f'Request: {path}')
        
        # Route handling
        if path == '/forward' or path == '/forward?':
            move_forward()
        elif path == '/left' or path == '/left?':
            move_left()
        elif path == '/stop' or path == '/stop?':
            move_stop()
        elif path == '/right' or path == '/right?':
            move_right()
        elif path == '/back' or path == '/back?':
            move_backward()
        elif path == '/distance':
            # Return just the distance value for AJAX requests
            distance = get_distance()
            if distance is not None:
                response = str(round(distance, 1))
            else:
                response = "Error"
            response_headers = (
                'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/plain\r\n'
                'Content-Length: {}\r\n'
                'Connection: close\r\n'
                '\r\n'
            ).format(len(response))
            client.send(response_headers.encode('utf-8'))
            client.send(response.encode('utf-8'))
            return
            
        # Generate response
        html = get_webpage()
        response_headers = (
            'HTTP/1.1 200 OK\r\n'
            'Content-Type: text/html; charset=utf-8\r\n'
            'Content-Length: {}\r\n'
            'Connection: close\r\n'
            '\r\n'
        ).format(len(html.encode('utf-8')))
        
        # Send response
        client.send(response_headers.encode('utf-8'))
        client.send(html.encode('utf-8'))
        
    except Exception as e:
        print(f'Error handling request: {e}')
        # Send error response
        error_response = (
            'HTTP/1.1 500 Internal Server Error\r\n'
            'Content-Type: text/plain\r\n'
            'Connection: close\r\n'
            '\r\n'
            'Server Error'
        )
        try:
            client.send(error_response.encode('utf-8'))
        except:
            pass
    finally:
        try:
            client.close()
        except:
            pass

def run_server():
    """Main server loop with improved error handling and memory management"""
    print('Starting Pico 2 W Robot Control Server...')
    
    try:
        # Connect to WiFi
        ip = connect_wifi()
        
        # Create socket
        server_socket = create_socket(ip)
        
        print('Server ready! Open your browser and navigate to:')
        print(f'http://{ip}')
        print('Press Ctrl+C to stop the server')
        
        # Main server loop
        while True:
            try:
                # Accept client connection
                client, addr = server_socket.accept()
                print(f'Client connected from {addr}')
                
                # Handle the request
                handle_request(client)
                
                # Periodic garbage collection to free memory
                gc.collect()
                
            except OSError as e:
                if e.args[0] == 104:  # Connection reset by peer
                    print('Client disconnected')
                else:
                    print(f'OSError: {e}')
            except Exception as e:
                print(f'Server error: {e}')
                
    except KeyboardInterrupt:
        print('\nShutting down server...')
    except Exception as e:
        print(f'Fatal error: {e}')
    finally:
        # Cleanup
        try:
            server_socket.close()
        except:
            pass
        status_led.off()
        print('Server stopped')

# Main execution
if __name__ == '__main__':
    try:
        run_server()
    except KeyboardInterrupt:
        machine.reset()
