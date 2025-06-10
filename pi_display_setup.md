# Raspberry Pi Display Setup Guide

## Hardware Requirements

### Recommended Displays
- **3.5" TFT Display (480x320)** - Perfect size for desktop robots
- **5" HDMI Display (800x480)** - Larger, better visibility
- **7" Official Raspberry Pi Display (800x480)** - Touch capability
- **Small OLED Displays (128x64)** - Minimal setup, lower cost

### Connection Options
1. **HDMI Displays** - Plug and play, best quality
2. **GPIO Displays** - Direct connection, requires drivers
3. **USB Displays** - Portable, good for prototyping

## Software Setup

### 1. Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install pygame and dependencies
sudo apt install python3-pygame python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# Install additional Python packages
pip3 install pygame numpy Pillow
```

### 2. Configure Display

#### For HDMI Displays
```bash
# Edit config file
sudo nano /boot/config.txt

# Add/modify these lines:
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt=480 320 60 6 0 0 0  # For 480x320 resolution
```

#### For GPIO Displays (3.5" TFT)
```bash
# Install display drivers (example for common 3.5" displays)
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./LCD35-show
```

### 3. Configure AI Assistant for Display

#### Update main.py configuration:
```python
# For 3.5" display (480x320)
self.display_manager = DisplayManager(
    screen_width=480,
    screen_height=320,
    fullscreen=True  # Use full screen on Pi
)

# For 5" display (800x480)
self.display_manager = DisplayManager(
    screen_width=800,
    screen_height=480,
    fullscreen=True
)
```

## Auto-Start Configuration

### 1. Create systemd service
```bash
sudo nano /etc/systemd/system/ai-assistant.service
```

```ini
[Unit]
Description=AI Assistant with Display
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ai_assistant
Environment=DISPLAY=:0
ExecStart=/usr/bin/python3 /home/pi/ai_assistant/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Enable auto-start
```bash
sudo systemctl enable ai-assistant.service
sudo systemctl start ai-assistant.service
```

## Display Features

### Visual States
- **🔵 STANDBY** - Blue pulsing background, "AI Assistant Ready"
- **🟢 LISTENING** - Green wave animation, "Listening..."
- **🟣 PROCESSING** - Purple spinning animation, "Thinking..."
- **🟠 SPEAKING** - Orange bouncing animation, "Speaking"
- **🔵 GAME_ACTIVE** - Cyan rainbow background, "Game Active"
- **🔴 ERROR** - Red flashing background, "Error"

### Information Displayed
- Current AI state
- Active user (Sophia, Eladriel, Parent)
- Current message/context
- Timestamp
- Game status (when active)

## Troubleshooting

### Display Issues
```bash
# Check display detection
tvservice -s

# Test pygame
python3 -c "import pygame; pygame.init(); print('Pygame working!')"

# For headless testing
export SDL_VIDEODRIVER=dummy
```

### Permission Issues
```bash
# Add user to video group
sudo usermod -a -G video pi

# Set display permissions
sudo chmod 666 /dev/fb0
```

### Performance Optimization
```python
# In display_manager.py, reduce FPS for slower Pi models
clock.tick(30)  # Instead of 60 FPS

# Reduce animation complexity
# Comment out complex background effects for Pi Zero
```

## Testing

### Run Display Demo
```bash
cd /home/pi/ai_assistant
python3 display_demo.py
```

### Check Integration
```bash
# Quick test
python3 -c "from display_manager import DisplayManager, AIState; print('Display ready!')"
```

## Hardware-Specific Notes

### Raspberry Pi Zero/Zero 2
- Use 480x320 resolution max
- Reduce animation complexity
- Consider 30 FPS instead of 60

### Raspberry Pi 3/4
- Can handle 800x480 or higher
- Full animation support
- 60 FPS smooth operation

### Raspberry Pi 5
- Supports high-resolution displays
- Can handle multiple displays
- Best performance with all features

## Power Considerations

### For Battery Operation
- Reduce display brightness
- Lower refresh rate
- Use smaller displays
- Consider auto-sleep functionality

### USB Power
- Ensure sufficient power supply (3A+ recommended)
- Some displays need separate power

## Example Configurations

### Compact Robot (3.5" display)
```python
DisplayManager(screen_width=480, screen_height=320, fullscreen=True)
```

### Desktop Assistant (7" display)
```python
DisplayManager(screen_width=800, screen_height=480, fullscreen=True)
```

### Development/Testing (windowed)
```python
DisplayManager(screen_width=800, screen_height=600, fullscreen=False)
``` 