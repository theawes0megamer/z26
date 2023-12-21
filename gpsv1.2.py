import serial
import pynmea2

# Replace '/dev/ttyUSB0' with the correct serial port for your GPS device
serial_port = serial.Serial('/dev/ttyS0', 115200, timeout=1)

def get_gps_data():
    try:
        raw_data = serial_port.readline().decode('utf-8')
        if raw_data.startswith('$GPGGA'):  # Example NMEA sentence, adjust based on your GPS device
            msg = pynmea2.parse(raw_data)
            return msg
    except serial.SerialException:
        pass

# Example usage:
while True:
    data = get_gps_data()
    if data:
        print(f" \r Latitude: {data.latitude}, Longitude: {data.longitude}, Speed: {data.spd_over_grnd}")
