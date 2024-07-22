import hid
import signal
import sys
import actions.myactions as actions
from actions.myactions import lightson, lightsoff 

# Define the vendor ID and product ID for the MacroPad
VENDOR_ID = 0x239A  # Adafruit vendor ID (9114 in decimal)
PRODUCT_ID = 0x8108  # MacroPad RP2040 product ID (33032 in decimal)
DEBUG = False
DRYRUN = False

actions.DEBUG = DEBUG
actions.DRYRUN = DRYRUN
# Find the device
def find_device(vendor_id, product_id):
    for device_info in hid.enumerate(vendor_id, product_id):
        if device_info['vendor_id'] == vendor_id and device_info['product_id'] == product_id:
            return device_info['path']
    return None

def handle_key_press(data):
    report_id = data[0]
    if DEBUG:
        print(f"data {data[0]} {data[1]} {data[2]} {data[3]} ")
        print(f"Received report: {data} with report id: {report_id}")
    if report_id == 1:  # Report ID for consumer control usage
        key_code = data[3]
        if DEBUG:
            print(f"Received consumer key code: {key_code}")
        if key_code == 30:
            lightson()
        elif key_code == 31:
            lightsoff()
        else:
            if DEBUG:
                print(f"Got {key_code}")


# Function to handle SIGINT (Ctrl+C)
def signal_handler(signal, frame):
    global RUNNING
    RUNNING = False
    print("Exiting...")    
    device.close()
    sys.exit(0)

# Global variable to track program state
RUNNING = True
device_path = find_device(VENDOR_ID, PRODUCT_ID)

if device_path is None:
    print(f"Failed to find device with VID={VENDOR_ID} and PID={PRODUCT_ID}")
    exit(1)

try:
    device = hid.Device(path=device_path)
    print(f"Connected to device at path: {device_path}")
    print(f"Manufacturer: {device.manufacturer}")
    print(f"Product: {device.product}")
    print(f"Serial: {device.serial}")
    print(f"MyVersion: 1.0")
except Exception as e:
    print(f"Failed to connect to the device: {e}")
    exit(1)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

if DEBUG:
    print("In DEBUG mode")

# Read input from the MacroPad
print("Listening for key presses...(Press Ctrl+C to exit)")
try:
    while RUNNING:
        data = device.read(64)  # Adjust the buffer size based on your MacroPad's report size
        if data:
            handle_key_press(data)
        else:
            print("No data received")
except hid.HIDException as e:
    print(f"Error reading from the device: {e}")
finally:
    # Close the device when done
    device.close()
