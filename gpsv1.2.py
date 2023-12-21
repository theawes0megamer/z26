from serial import Serial
from pyubx2 import UBXReader

try:
    stream = Serial('COM8', 38400)
    while True:
        ubr = UBXReader(stream)
        (raw_data, parsed_data) = ubr.read()
        # print(parsed_data)
        if parsed_data.identity == "NAV-PVT":
            lat, lon, alt = parsed_data.lat, parsed_data.lon, parsed_data.hMSL
            print(f"lat = {lat}, lon = {lon}, alt = {alt/1000} m")
except KeyboardInterrupt:
    print("Terminated by user")