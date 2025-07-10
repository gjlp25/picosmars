import network
import socket
import time
import machine
from SimplyRobotics import KitronikSimplyRobotics
from secrets import WIFI_SSID, WIFI_PASSWORD

# Configuratie
DEFAULT_SPEED = 50
MOTOR_LEFT = 0
MOTOR_RIGHT = 3

robot = None
current_speed = DEFAULT_SPEED
safety_enabled = True
program = []  # voor het routeprogramma
led = machine.Pin("LED", machine.Pin.OUT)

# Init hardware
def init_hardware():
    global robot
    try:
        print("Hardware initialiseren...")
        robot = KitronikSimplyRobotics()
        print("Hardware gereed")
        return True
    except Exception as e:
        print(f"Fout bij hardware init: {e}")
        return False

# Motor control
def control_motors(action, duration=0):
    global robot, current_speed, safety_enabled
    if not robot:
        return False
    try:
        if safety_enabled and action != "stop":
            print("Beweging geblokkeerd door veiligheid.")
            return False

        robot.motors[MOTOR_LEFT].off()
        robot.motors[MOTOR_RIGHT].off()

        if action == "forward":
            robot.motors[MOTOR_LEFT].on("r", current_speed)
            robot.motors[MOTOR_RIGHT].on("r", current_speed)
        elif action == "reverse":
            robot.motors[MOTOR_LEFT].on("f", current_speed)
            robot.motors[MOTOR_RIGHT].on("f", current_speed)
        elif action == "left":
            robot.motors[MOTOR_LEFT].on("r", current_speed)
            robot.motors[MOTOR_RIGHT].on("f", current_speed)
        elif action == "right":
            robot.motors[MOTOR_LEFT].on("f", current_speed)
            robot.motors[MOTOR_RIGHT].on("r", current_speed)

        if duration > 0:
            time.sleep(duration)
            robot.motors[MOTOR_LEFT].off()
            robot.motors[MOTOR_RIGHT].off()
        return True
    except Exception as e:
        print(f"Motorfout: {e}")
        return False

# Program afspelen
def play_program():
    print("Start programma...")
    for step in program:
        print(f"Uitvoeren: {step}")
        if step == "forward":
            control_motors("forward", 0.5)
        elif step == "left":
            control_motors("left", 0.6)
        elif step == "right":
            control_motors("right", 0.6)
    print("Programma klaar.")

# HTML genereren
def create_html(speed, safety_on, program_list):
    route_str = " → ".join(program_list) if program_list else "Leeg"
    return f"""<!DOCTYPE html>
<html>
<head>
<title>Robot Control met Route</title>
<meta charset="UTF-8">
<style>
body {{
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}
.container {{
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    text-align: center;
    width: 300px;
}}
.status {{
    background: #e9f1fb;
    padding: 10px;
    margin-bottom: 20px;
    border-radius: 8px;
    font-size: 16px;
}}
button {{
    font-size: 16px;
    padding: 10px;
    margin: 5px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    color: white;
}}
.speed-btn {{ background-color: #007bff; }}
.speed-btn:hover {{ background-color: #0056b3; }}
.dir-btn {{ background-color: #28a745; }}
.dir-btn:hover {{ background-color: #1e7e34; }}
.stop-btn {{ background-color: #dc3545; }}
.stop-btn:hover {{ background-color: #c82333; }}
.prog-btn {{ background-color: #6f42c1; }}
.prog-btn:hover {{ background-color: #563d7c; }}
.footer {{
    background: #f0f0f0;
    padding: 10px;
    margin-top: 20px;
    border-radius: 8px;
    font-size: 14px;
}}
</style>
</head>
<body>
<div class="container">
    <h2>🤖 Robot Route Planner</h2>
    <div class="status">
        Speed: {speed}%<br>
        Safety: {"ON" if safety_on else "OFF"}<br>
        <strong>Route:</strong> {route_str}
    </div>
    <form method="GET">
        <button name="action" value="add_forward" class="prog-btn">+ Forward</button>
        <button name="action" value="add_left" class="prog-btn">+ Left</button>
        <button name="action" value="add_right" class="prog-btn">+ Right</button><br>
        <button name="action" value="play" class="speed-btn">▶️ Play</button>
        <button name="action" value="clear" class="stop-btn">🗑 Clear</button>
    </form>
    <div class="footer">
        Kitronik Simply Robotics + Programmeerbare Route
    </div>
</div>
</body>
</html>"""

# WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140)
    if not wlan.isconnected():
        print("WiFi verbinden...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 20
        while not wlan.isconnected() and timeout > 0:
            led.toggle()
            time.sleep(0.5)
            timeout -= 1
        led.off()
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print(f"Verbonden: {ip}")
        led.on()
        return ip
    else:
        print("Geen WiFi verbinding")
        led.off()
        return None

# Main
def main():
    global current_speed, safety_enabled, program

    print("Robot Control starten...")
    if not init_hardware():
        led.off()
        machine.reset()

    ip = connect_wifi()
    if not ip:
        led.off()
        machine.reset()

    try:
        addr = socket.getaddrinfo(ip, 80)[0][-1]
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(addr)
        server.listen(1)
        print(f"Server draait op: http://{ip}")
    except Exception as e:
        led.off()
        machine.reset()

    while True:
        try:
            client, addr = server.accept()
            request = client.recv(1024).decode()

            if 'GET /?' in request:
                params = request.split('GET /?')[1].split(' ')[0]
                pairs = params.split('&')
                for pair in pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        if key == 'action':
                            if value == 'add_forward':
                                program.append("forward")
                            elif value == 'add_left':
                                program.append("left")
                            elif value == 'add_right':
                                program.append("right")
                            elif value == 'clear':
                                program.clear()
                            elif value == 'play':
                                play_program()

            html = create_html(current_speed, safety_enabled, program)
            client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n".encode())
            client.send(html.encode())
            client.close()

        except Exception as e:
            try:
                client.close()
            except:
                pass

if __name__ == "__main__":
    main()
