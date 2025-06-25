# Technical Context: NewSMARS_pico

## Architecture Overview

### 1. Core Components
- MicroPython runtime on Raspberry Pi Pico W
- SMARS robot hardware interface
- Web-based control system
- **CONFIRMED WORKING**: Sensor integration system via rangefinder.py → smars.py → main_new.py
- Autonomous behavior system
- **VALIDATED**: Real-time distance sensing in web interface

### 2. Network Architecture
- WiFi connectivity using network.WLAN
- HTTP server on port 80
- Non-blocking socket operations
- Connection recovery system
- Network status monitoring
- Enhanced error handling for network operations

### 3. Control Interface
- HTML5-based web interface
- Real-time status updates
- Touch-optimized controls
- Responsive design
- Auto-refresh mechanism (500ms for distance sensing)
- Dual movement modes (continuous/single)
- **CONFIRMED**: main_new.py web interface working with rangefinder integration
- **VALIDATED**: Clean architecture with SMARS abstraction layer

## Implementation Details

### 1. WiFi Connection Management
```python
def connect_wifi():
    # Enhanced WiFi connection with:
    - Network scanning
    - Signal strength monitoring
    - Status reporting
    - Connection recovery
    - Timeout handling
    - Error diagnostics
```

### 2. Web Server Implementation
```python
def serve():
    # Improved server with:
    - Non-blocking operations
    - Request validation
    - Error handling
    - Connection recovery
    - Resource cleanup
    - Client connection management
```

### 3. Movement Control
```python
def handle_movement():
    # Movement control with:
    - Duration-based control
    - Continuous mode
    - Emergency stop
    - Directional control
    - Mode switching
```

## Technical Specifications

### 1. Network
- Protocol: HTTP
- Port: 80
- Socket Type: Non-blocking TCP
- Connection Timeout: 30s
- Recovery Attempts: 3
- Status Monitoring: Active

### 2. Web Interface
- Technology: HTML5/CSS3
- Refresh Rate: 2s
- Input Methods: Touch/Mouse
- Response Time: <100ms
- Error Handling: Graceful degradation
- Mobile Support: Yes

### 3. Control System
- Update Frequency: Real-time
- Movement Modes: 2 (Single/Continuous)
- Command Types: 5 (Forward/Back/Left/Right/Stop)
- Status Updates: Continuous
- Error Recovery: Automatic

## Dependencies

### 1. Hardware
- Raspberry Pi Pico W
- SMARS robot chassis
- Motors (2x)
- **CONFIRMED WORKING**: Distance sensor (HC-SR04) with rangefinder.py
- Jumper wires
- Battery pack

### 2. Software
- MicroPython 1.19+
- network module
- socket module
- machine module
- time module

### 3. Libraries
- **CONFIRMED WORKING**: Custom SMARS class with rangefinder integration
- WebController class
- Network management
- **VALIDATED**: HCSR04 sensor interface in rangefinder.py
- **CONFIRMED**: Clean modular architecture maintained

## Error Handling

### 1. Network Errors
- Connection loss recovery
- Timeout management
- Invalid request handling
- Socket error recovery
- Resource cleanup

### 2. Hardware Errors
- Motor failure detection
- Sensor reading validation
- Power monitoring
- Pin state management
- Emergency shutdown

### 3. Software Errors
- Request validation
- Input sanitization
- Resource management
- Exception handling
- Status monitoring

## Performance Considerations

### 1. Memory Management
- Request buffer size: 1024 bytes
- HTML template caching
- Resource cleanup
- Connection pooling
- Garbage collection

### 2. Network Performance
- Non-blocking operations
- Connection timeouts
- Request rate limiting
- Response optimization
- Status monitoring

### 3. Power Efficiency
- Sleep modes
- Sensor polling optimization
- Network connection management
- Motor control efficiency
- Status update frequency

## Security Measures

### 1. Network Security
- Request validation
- Path sanitization
- Error masking
- Resource limits
- Connection timeouts

### 2. Control Security
- Command validation
- State management
- Error recovery
- Resource protection
- Access control

### 3. System Security
- Resource limits
- Error handling
- Status monitoring
- Recovery procedures
- Fail-safes

## Known Limitations

### 1. Hardware Limitations
- Processing power
- Memory constraints
- Network bandwidth
- Sensor accuracy (HC-SR04 working within expected parameters)
- Battery life

### 2. Software Limitations
- Single client support
- Request queue size
- Update frequency (distance sensing optimized at 500ms intervals)
- Error recovery scope
- Status monitoring depth

### 3. Network Limitations
- WiFi range
- Connection stability
- Request handling capacity
- Recovery capabilities
- Status monitoring granularity

## Architecture Validation Summary
- **Rangefinder Integration**: CONFIRMED working via SMARS abstraction
- **main_new.py Status**: OPERATIONAL with real-time distance display
- **Modular Design**: USER VALIDATED as optimal approach
- **Clean Separation**: rangefinder.py → smars.py → main_new.py pattern working effectively
