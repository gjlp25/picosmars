# NewSMARS_pico

A Python-based robotics control system for SMARS robots using the Raspberry Pi Pico microcontroller. This project provides both autonomous and manual control capabilities through a web interface.

## Features

- Basic movement control (forward, backward, turns)
- Distance sensing with HC-SR04 sensor
- Web-based control interface
- WiFi connectivity
- Multiple autonomous modes:
  - Random Explorer
  - Wall Follower
  - Area Coverage
- Real-time distance monitoring
- Configurable movement parameters

## Documentation

Comprehensive project documentation is maintained in the memory-bank directory:

- [Project Brief](memory-bank/projectbrief.md) - Core requirements and goals
- [Product Context](memory-bank/productContext.md) - Why this project exists
- [System Patterns](memory-bank/systemPatterns.md) - Architecture and technical decisions
- [Technical Context](memory-bank/techContext.md) - Technologies and development setup
- [Active Context](memory-bank/activeContext.md) - Current work and next steps
- [Progress](memory-bank/progress.md) - Project status and tracking

## Hardware Requirements

- Raspberry Pi Pico
- HC-SR04 Ultrasonic Range Finder
- Dual DC motors
- SMARS robot chassis
- Power supply
- WiFi connectivity

## Pin Configuration

- Motor A: Forward (18), Reverse (19)
- Motor B: Forward (20), Reverse (21)
- HC-SR04: Trigger (17), Echo (16)

## Quick Start

1. Flash MicroPython firmware to Raspberry Pi Pico
2. Upload project files to the Pico
3. Configure WiFi credentials in webcontrol.py
4. Connect to web interface for control
5. Or run autonomous modes through main.py

## Usage

### Web Control
```python
from webcontrol import WebController
from smars import SMARS

robot = SMARS()
controller = WebController(robot, ssid='your_wifi', password='your_password')
controller.serve()
```

### Autonomous Mode
```python
from autonomous import AutonomousController
from smars import SMARS

robot = SMARS()
controller = AutonomousController(robot)
controller.random_explorer()  # or wall_follower() or area_coverage()
```

## Contributing

Project is in active development. See [Progress](memory-bank/progress.md) for current status and upcoming features.

## License

Open source - feel free to use and modify as needed.
