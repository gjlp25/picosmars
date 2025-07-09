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

# Globale variabelen
robot = None
current_speed = DEFAULT_SPEED
safety_enabled = True

# Hardware initialisatie
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

# Motoren aansturen met safety check
def control_motors(action):
    global robot, current_speed, safety_enabled

    if not robot:
        return False

    try:
        if safety_enabled and action != "stop":
            print("Beweging geblokkeerd door veiligheid.")
            return False

        # Stop altijd eerst
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
        
        return True

    except Exception as e:
        print(f"Motorfout: {e}")
        return False

# HTML pagina met grid-layout zoals op jouw screenshot
def create_html(speed, safety_on):
    return f"""<!DOCTYPE html>
<html>
<head>
<title>Robot Control with Speed</title>
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
    font-size: 18px;
}}
.grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 10px;
    justify-items: center;
    margin: 20px 0;
}}
button {{
    font-size: 18px;
    padding: 15px;
    width: 80px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    color: white;
}}
.speed-btn {{
    background-color: #007bff;
}}
.speed-btn:hover {{
    background-color: #0056b3;
}}
.dir-btn {{
    background-color: #28a745;
}}
.dir-btn:hover {{
    background-color: #1e7e34;
}}
.stop-btn {{
    background-color: #dc3545;
}}
.stop-btn:hover {{
    background-color: #c82333;
}}
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
    <h2>🤖 Robot Control with Speed</h2>
    <div class="status">
        Current Speed: {speed}%<br>
        Safety: {"ON" if safety_on else "OFF"}
    </div>
    <form method="GET">
        <div>
            <button type="submit" name="action" value="speed_down" class="speed-btn">🔽 Slower</button>
            <button type="submit" name="action" value="speed_up" class="speed-btn">🔼 Faster</button>
        </div>
        <div class="grid">
            <div></div>
            <button type="submit" name="action" value="forward" class="dir-btn">⬆️</button>
            <div></div>
            <button type="submit" name="action" value="left" class="dir-btn">⬅️</button>
            <button type="submit" name="action" value="stop" class="stop-btn">⏹️</button>
            <button type="submit" name="action" value="right" class="dir-btn">➡️</button>
            <div></div>
            <button type="submit" name="action" value="reverse" class="dir-btn">⬇️</button>
            <div></div>
        </div>
        <button type="submit" name="action" value="toggle_safety" style="
            background-color: #ffc107; color: black; margin-top: 10px; border-radius: 8px; padding: 10px 20px;">
            {"Disable Safety" if safety_on else "Enable Safety"}
        </button>
    </form>
    <div class="footer">
        Kitronik Simply Robotics Configuration:<br>
        Motor: Variable Speed 0-100% | PWM: Auto<br>
        Speed Control Active
    </div>
</div>
</body>
</html>"""

# WiFi connectie
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Verbinding maken met WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 20
        while not wlan.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1
        print()

    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print(f"Verbonden: {ip}")
        return ip
    else:
        print("WiFi verbinding mislukt")
        return None

# Main programma
def main():
    global current_speed, safety_enabled

    print("Robot Control starten...")

    if not init_hardware():
        print("Herstarten wegens hardware fout...")
        machine.reset()

    ip = connect_wifi()
    if not ip:
        print("Geen WiFi, herstarten...")
        machine.reset()

    try:
        addr = socket.getaddrinfo(ip, 80)[0][-1]
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(addr)
        server.listen(1)
        print(f"Server draait op: http://{ip}")
    except Exception as e:
        print(f"Server fout: {e}")
        machine.reset()

    while True:
        try:
            print("Wacht op verbinding...")
            client, addr = server.accept()
            print(f"Client verbonden: {addr}")

            request = client.recv(1024).decode()
            print("Request ontvangen")

            if 'GET /?' in request:
                try:
                    params = request.split('GET /?')[1].split(' ')[0]
                    pairs = params.split('&')

                    for pair in pairs:
                        if '=' in pair:
                            key, value = pair.split('=', 1)
                            if key == 'action':
                                if value == 'toggle_safety':
                                    safety_enabled = not safety_enabled
                                    print(f"Safety toggled: {safety_enabled}")
                                elif value == 'speed_up':
                                    current_speed = min(100, current_speed + 10)
                                    print(f"Snelheid verhoogd naar: {current_speed}%")
                                elif value == 'speed_down':
                                    current_speed = max(10, current_speed - 10)
                                    print(f"Snelheid verlaagd naar: {current_speed}%")
                                else:
                                    print(f"Actie uitvoeren: {value}")
                                    control_motors(value)
                except Exception as e:
                    print(f"Fout bij parsen: {e}")

            html = create_html(current_speed, safety_enabled)
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"
            client.send(response.encode())
            client.send(html.encode())
            client.close()
            print("Response verzonden")

        except KeyboardInterrupt:
            print("Stoppen...")
            break
        except Exception as e:
            print(f"Fout: {e}")
            try:
                client.close()
            except:
                pass

    try:
        server.close()
        if robot:
            robot.motors[MOTOR_LEFT].off()
            robot.motors[MOTOR_RIGHT].off()
    except:
        pass

# Run
if __name__ == "__main__":
    main()
