import network
import socket
import time

# WiFi credentials - change these to match your network
SSID = 'WiCaRo_IoT'
PASSWORD = 'Test@2021'

def test_wifi_connection():
    """
    Test WiFi connectivity and show network information.
    Returns the IP address if connection is successful.
    """
    print("WiFi Connection Test")
    print("-" * 20)
    
    # Initialize WiFi
    print("\nInitializing WiFi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Show current status
    print(f"WiFi Active: {wlan.active()}")
    print(f"Current Connection: {wlan.isconnected()}")
    
    if wlan.isconnected():
        print("Disconnecting from any existing networks...")
        wlan.disconnect()
        time.sleep(2)
    
    # Scan for networks
    print("\nScanning for your network...")
    found_networks = wlan.scan()
    network_found = False
    
    for net in found_networks:
        if net[0].decode('utf-8') == SSID:
            network_found = True
            print(f"Found your network: {SSID}")
            print(f"Signal strength: {net[3]}dBm")
            break
    
    if not network_found:
        print(f"Warning: Could not find {SSID} in available networks!")
        print("\nAvailable networks:")
        for net in found_networks:
            print(f"- {net[0].decode('utf-8')}")
        return None
    
    print(f"\nAttempting to connect to {SSID}...")
    wlan.connect(SSID, PASSWORD)
    
    # Wait for connection with timeout
    print("Waiting for connection (30 seconds timeout)...")
    timeout = 30
    while timeout > 0:
        if wlan.isconnected():
            break
        print(".", end="")
        time.sleep(1)
        timeout -= 1
    print()
    
    if wlan.isconnected():
        print("\nConnection successful!")
        network_info = wlan.ifconfig()
        print(f"IP Address: {network_info[0]}")
        print(f"Subnet Mask: {network_info[1]}")
        print(f"Gateway: {network_info[2]}")
        print(f"DNS Server: {network_info[3]}")
        return network_info[0]
    else:
        print("\nConnection failed!")
        print("\nDebug Information:")
        print(f"Status code: {wlan.status()}")
        print(f"Active: {wlan.active()}")
        print("Try:")
        print("1. Double-check SSID and password")
        print("2. Restart your Pico W")
        print("3. Make sure you're within range of the network")
        return None

def test_simple_webserver(ip):
    """
    Start a simple test webserver to verify network functionality.
    """
    if not ip:
        return
    
    print("\nStarting test web server...")
    addr = (ip, 80)
    
    # Create socket
    connection = socket.socket()
    connection.bind(addr)
    connection.listen(1)
    
    print(f"\nTest server running at http://{ip}")
    print("Connect to this IP address from a web browser on your network")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            client = connection.accept()[0]
            request = client.recv(1024)
            
            # Create simple test page
            html = """
            <!DOCTYPE html>
            <html>
            <head><title>PicoSMARS WiFi Test</title></head>
            <body>
                <h1>WiFi Test Successful!</h1>
                <p>Your Pico W is connected and web server is working.</p>
            </body>
            </html>
            """
            
            client.send(html)
            client.close()
            print("Client connected and page served!")
            
    except KeyboardInterrupt:
        print("\nTest server stopped by user")
    finally:
        connection.close()
        print("Server socket closed")

def main():
    """Main test function."""
    try:
        # Test WiFi connection
        ip = test_wifi_connection()
        
        if ip:
            # If connection successful, start test server
            test_simple_webserver(ip)
            
    except KeyboardInterrupt:
        print("\nTests stopped by user")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
