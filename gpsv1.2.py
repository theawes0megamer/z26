import serial
import pyubx2

# Replace '/dev/ttyUSB0' with the correct serial port for your GPS device
serial_port = serial.Serial('/dev/ttyS0', 115200, timeout=1)
ubr = pyubx2.UBXReader(serial_port)

while True:
    try:
        raw_data, parsed_data = ubr.read()
        if parsed_data and hasattr(parsed_data, 'ground_speed'):  # Adjust the attribute name
            gspeed = parsed_data.ground_speed  # Adjust the attribute name
            mph = gspeed * 1.150779
            print(f"Ground Speed: {mph} mph")
    except (serial.SerialException, pyubx2.UBXStreamError):
        pass
