from tkinter import *
from datetime import datetime
import time
import pyubx2.ubxreader
import serial
import pyubx2
import threading

# create tkinter window
window = Tk()

window.geometry('1024x600')
window.config(bg="black")
window.title("Zero2Sixty Box")

stream = serial.Serial('/dev/ttyS0', 115200, timeout=3)



def update_time():  # Update the time in the UI
    time_str = datetime.now().strftime("%B %d, %Y, %I:%M:%S %p")
    timelbl.config(text=time_str)
    timelbl.after(1000, update_time)

# def update_gps_info():  # number of sats, 2d/3d lock info
#     global sats, lock_status

#     if stream.inWaiting():  # Check if there is data available from the serial port
#         raw_data = stream.read(stream.inWaiting())  # Read the incoming data from the serial port
#         report = pyubx2.parse(raw_data)  # Parse the received UBX messages
#         if 'NAV-SOL' in report:
#             sats = report['NAV-SOL']['numSV']
#         else:
#             sats = 0

#         if 'NAV-STATUS' in report:
#             lock_status = '2D' if report['NAV-STATUS']['fixType'] == 1 else '3D'
#         else:
#             lock_status = ''

#     satslbl.config(text=f"{sats} Sats {lock_status}")
global mph

def update_mph():

    ubr = pyubx2.UBXReader(stream)
    (raw_data, parsed_data) = ubr.read()
    # if parsed_data is not None and hasattr(parsed_data, 'gSpeed'):
    #     mph = parsed_data.gSpeed * 2.23694
    print(parsed_data)


    # mphstr = f"{mph:.1f} MPH"
    # mphlbl.config(text=mphstr)
    # save_top_speed()  # Call save_top_speed here instead of after loop
    # timelbl.after(100, update_mph)

    # if mph > 1:
    #     start_timer()

def start_timer():  # Start the 0-60 MPH timer
    global start_time
    start_time = None

    if mph > 1 and not start_time:
        start_time = time.time()
        update_timer()

def update_timer():  # Update the timer with new values
    current_speed = mph
    if current_speed > 0 and current_speed <= 60:
        elapsed_time = time.time() - start_time
        timer_str = format_time(elapsed_time)
        timerlbl.config(text=timer_str)
        timerlbl.after(10, update_timer)
    elif current_speed > 60 and start_time:
        timerlbl.config(text=format_time(time.time() - start_time))
    elif current_speed == 0 and start_time:  # reset timer when you go below 1mph
        start_time = 0
    else:
        timerlbl.config(text="")

def format_time(seconds):  # Format the time for display
    return "{:.2f}s".format(seconds)

top_speed = 0

def save_top_speed():
    global top_speed
    if mph > top_speed:
        top_speed = mph
        topspeed_string = f"{top_speed:.1f} MPH Top speed"
        tspdlbl.config(text=topspeed_string)

z26lbl = Label(window, text="  Zero2Sixty Box", font=("Lato", 20), fg="white", bg="black")  # Zero2Sixty Box Label
z26lbl.grid(column=1, row=1, padx=20, pady=20, sticky="w")
z26lbl.columnconfigure(1, weight=1)

timelbl = Label(window, text="", font=("Lato", 20), fg="white", bg="black", width=45)  # Time Label
timelbl.columnconfigure(1, weight=0)
timelbl.rowconfigure(1, weight=0)
timelbl.grid(row=1, column=2, padx=20, pady=20, sticky="w")

mphlbl = Label(window, text="", font=("Lato", 60), fg="white", bg="black", width=7)  # MPH Label
mphlbl.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

tspdlbl = Label(window, text="", font=("Lato", 30), fg="white", bg="black")
tspdlbl.grid(row=3, column=1, padx=60, pady=10, sticky="w")

timerlbl = Label(window, text="", font=("Lato", 60), fg="white", bg="black")
timerlbl.grid(row=2, column=2, padx=20, pady=20)

satslbl = Label(window, text="", font=("Lato", 20), fg="white", bg="black")
satslbl.grid(row=3, column=2, sticky="we", padx=10)

update_time()
update_mph()
# update_gps_info()


window.mainloop()