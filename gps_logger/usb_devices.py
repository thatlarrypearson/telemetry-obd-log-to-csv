# telemetry-gps/gps_logger/usb_devices.py

from serial.tools.list_ports import comports

# The following are specific to the u-blox GNSS receiver
DEFAULT_USB_VID = 5446
DEFAULT_USB_PID = 424
GPS_DEVICE_NAME = "u-blox GNSS receiver"

# This default is the default device name on a Raspberry Pi when the GPS is the only attached serial USB device.
DEFAULT_SERIAL_DEVICE="/dev/ttyACM0"

def get_serial_device_name(verbose=False)->str:
    """Get serial device name for GPS"""

    for p in comports():
        if p.vid and p.vid == DEFAULT_USB_VID and p.pid == DEFAULT_USB_PID:
            return p.device

    logging.error(f"USB attached GPS device <{GPS_DEVICE_NAME}> not found.")
    logging.error(f"Trying serial port device <{DEFAULT_SERIAL_DEVICE}>.")

    return DEFAULT_SERIAL_DEVICE

def main():
    print("Candidate Serial Device List (non-USB devices excluded)")
    i = 0
    for p in comports():
        if not p.vid:
            # not a USB device
            continue
        i += 1
        print(f"\t+{i} {p.device}")
        print(f"\t\tName: {p.name}")
        print(f"\t\tUSB VID: {p.vid}")
        print(f"\t\tUSB PID: {p.pid}")
        print(f"\t\tDescription: {p.description}")
        print(f"\t\tHardware ID: {p.hwid}")
        print(f"\t\tManufacturer: {p.manufacturer}")
        print(f"\t\tProduct: {p.product}")
        print(f"\t\tSerial Number: {p.serial_number}")
        print(f"\t\tLocation: {p.location}")
        print(f"\t\tinterface: {p.interface}")

    print(f"\nFound {i} USB Serial Device(s)")

    if sdn := get_serial_device_name():
        print(f"USB Serial Device <{GPS_DEVICE_NAME}> Name {sdn} found")

if __name__ == "__main__":
    main()

