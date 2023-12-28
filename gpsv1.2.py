from pyubx2 import UBXReader
stream = Serial('/dev/ttyS0', 115200, timeout=3)
ubr = UBXReader(stream, protfilter=2)
for (raw_data, parsed_data) in ubr: print(parsed_data)
