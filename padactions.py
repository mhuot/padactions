'''This module will listen for a MacroPad keys and perform actions'''
import sys
import os
import importlib
import hid
import actions
from actions.actions import lightson, lightsoff

# Import the actions module specified by the environment variable or default to 'actions.actions'
actions_module_name = os.getenv('ACTIONS_MODULE', 'actions.actions')
try:
    actions = importlib.import_module(actions_module_name)
except ImportError:
    print(f"Error: Failed to import '{actions_module_name}'. 
          Ensure it is in the Python path and install required packages.")
    sys.exit(1)

# Define the vendor ID and product ID for the MacroPad
VENDOR_ID = 0x239A  # Adafruit vendor ID (9114 in decimal)
PRODUCT_ID = 0x8108  # MacroPad RP2040 product ID (33032 in decimal)
DEBUG = False
DRYRUN = False

actions.debug = DEBUG
actions.dryrun = DRYRUN
# Find the device
def find_device(vendor_id, product_id):
    '''This is used to find the devie based on the vendor and product IDs'''
    for device_info in hid.enumerate(vendor_id, product_id):
        if device_info['vendor_id'] == vendor_id and device_info['product_id'] == product_id:
            return device_info['path']
    return None

def handle_key_press(kpdata):
    '''Used to handle the key presses received'''
    report_id = kpdata[0]
    if DEBUG:
        print(f"data {kpdata[0]} {kpdata[1]} {kpdata[2]} {kpdata[3]} ")
        print(f"Received report: {kpdata} with report id: {report_id}")
    if report_id == 1:  # Report ID for consumer control usage
        key_code = kpdata[3]
        if DEBUG:
            print(f"Received consumer key code: {key_code}")
        if key_code == 30:
            lightson()
        elif key_code == 31:
            lightsoff()
        else:
            if DEBUG:
                print(f"Got {key_code}")

device_path = find_device(VENDOR_ID, PRODUCT_ID)

if device_path is None:
    print(f"Failed to find device with VID={VENDOR_ID} and PID={PRODUCT_ID}")

try:
    device = hid.Device(path=device_path)
    print(f"Connected to device at path: {device_path}")
    print(f"Manufacturer: {device.manufacturer}")
    print(f"Product: {device.product}")
    print(f"Serial: {device.serial}")
    print("MyVersion: 1.0")
except hid.HIDException as e:
    print(f"Failed to connect to the device: {e}")

if DEBUG:
    print("In DEBUG mode")

# Read input from the MacroPad
print("Listening for key presses...(Press Ctrl+C to exit)")
try:
    data = device.read(64)  # Adjust the buffer size based on your MacroPad's report size
    if data:
        handle_key_press(data)
    else:
        print("No data received")
except hid.HIDException as e:
    print(f"Error reading from the device: {e}")
except KeyboardInterrupt as e:
    print(f"Normal exit {e}")
finally:
    # Close the device when done
    device.close()
