# MacroPad Light Control

This project allows you to run actions in Python on a Raspberry Pi(like control Elgato lights) using an Adafruit MacroPad RP2040. The MacroPad sends key codes via HID to a Python script on the Raspberry Pi that interprets these codes to have Python perform actions (like turning the lights on or off).

## Prerequisites

- Python 3.6+
- CircuitPython 9.x
- `hidapi` library
- `requests` library

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mhuot/padactions.git
   cd padactions
    ```
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure udev rules:
   Create a new file /etc/udev/rules.d/99-macropad.rules:
   ```bash
   sudo nano /etc/udev/rules.d/99-macropad.rules
   ```
4. Validate the VendorID is 239a and ProductID is 8108
   ```bash
   $ lsusb
   Bus 001 Device 029: ID 239a:8108 Adafruit Macropad RP2040
   $
   ```

5. Add the following line to the file:
   ```bash
   SUBSYSTEM=="hidraw", ATTRS{idVendor}=="239a", ATTRS{idProduct}=="8108", MODE="0666", GROUP="plugdev"
   ```
   Adjust the ID's if they are different. Save and close the file.

6. Reload udev rules:
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

7. Add your user to the plugdev group:
   ```bash
   sudo usermod -aG plugdev $USER
   ```

8. Log out and log back in for the group change to take effect.

## Running the Script
1. Change to the directory of the repository
   ```bash
   cd /path/to/your/repository
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Run the script:
   ```bash
   python padactions.py
   ```

## Script Overview
### padactions.py
This script listens for key presses from the MacroPad and sends requests to turn Elgato lights on or off based on the key codes received.

Key codes and actions:

Keycode 30: Turns the lights on
Keycode 31
: Turns the lights off

## Creating a systemd Service

1. Move your project to the /opt directory:
   ```bash
   sudo mv /path/to/your/repository /opt/padactions
   cd /opt/padactions
   ```
2. Create a systemd service file
    ```bash
    sudo nano /etc/systemd/system/padactions.service
    ```
3. Add the following content to the service file:
   ```bash
   [Unit]
   Description=MacroPad Light Control Service
   After=network.target

   [Service]
   Type=simple
   User=YOUR_USERNAME
   WorkingDirectory=/path/to/your/repository
   ExecStart=/opt/padactions/venv/bin/python /opt/padactions/padactions.py
   Restart=on-failure
   Environment="PYTHONUNBUFFERED=1"

   [Install]
   WantedBy=multi-user.target
   ```
   Replace YOUR_USERNAME with your actual username and /path/to/your/repository with the path to your project directory.
4. Reload systemd to apply the new service
   ```bash
   sudo systemctl daemon-reload
   ```
5. Enable the service to start on boot:
   ```bash
   sudo systemctl enable padactions.service
   ```
6. Start the service
   ```bash
   sudo systemctl start padactions
   ```
This will ensure your script runs as a systemd service and starts automatically on boot.

#### Debug mode:

Set the DEBUG variable to True to enable debug output.

## MacroPad code.py
You will need to install the macropad/code.py onto your MacroPad.

## MacroPad libs needed
This list is what I have on my MacroPad, it is possible I have more than needed. You should be able to put these in /lib on the MacroPad. See https://learn.adafruit.com/adafruit-macropad-rp2040/macropad-circuitpython-library for more information.
* adafruit_bitmap_font
* adafruit_debouncer
* adafruit_displayio_layout
* adafruit_display_shapes
* adafruit_display_text
* adafruit_hid
* adafruit_led_animation
* adafruit_macropad
* adafruit_midi
* adafruit_pixelbuf
* adafruit_simple_text_display
* adafruit_ticks
* neopixel

## TODO:
Add the MacroPad info to the README
Allow DEBUG, vendor ID and product ID to be specified by environment variables
Have the host send feedback on actions to set key and display
Add the encoder for making changes

## License
This project is licensed under the MIT License. See the LICENSE file for more details.