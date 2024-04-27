from tkinter import *
import time
import serial
import gps


# create tkinter window
window = Tk()

window.geometry('1024x600')
window.config(bg="black")
window.title("Zero2Sixty Box")

# stream = serial.Serial('/dev/ttyS0', 115200, timeout=3)
session = gps.gps(mode=gps.WATCH_ENABLE)


def update_time():  # Update the time in the UI
    time_str = session.fix.time
    timelbl.config(text=time_str)
    timelbl.after(1000, update_time)

# def update_gps_info():
#     global sats,lock,sat_lock
#     sats,lock=session.sky.uSat,session.fix.mode
#     if lock == 1:
#         sat_lock = "No Lock"
#     if lock == 2:
#         sat_lock = "2D"
#     if lock == 3:
#         sat_lock = "3D"
    
    
#     satslbl.config(text=f"{sats} Sats {sat_lock}")

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

# def update_mph():

#     #while True:
#     ubr = pyubx2.UBXReader(stream)
#     (raw_data, parsed_data) = ubr.read()
#     if parsed_data:
#         mph = parsed_data

    # mphstr = f"{mph:.1f} MPH"
    # mphlbl.config(text=mphstr)
    # save_top_speed()  # Call save_top_speed here instead of after loop
    # timelbl.after(100, update_mph)

    # if mph > 1:
    #     start_timer()
# def update_mph(): # Version 2 of function (hopefully works lol)
#     ubr = pyubx2.UBXReader(stream)
#     (raw_data,parsed_data) = ubr.read()
#     print(f"Parsed data: {parsed_data}\n Raw data: {raw_data}")
#     print(parsed_data.speed)

def update_mph():
    try:
        while 0 == session.read():
            if not (gps.MODE_SET & session.valid):
                continue
            if (gps.isfinite)(session.fix.speed):
                mph = session.fix.speed * 2.23693629

        mphstr = f"{mph:.2f} MPH"
        mphlbl.config(text=mphstr)
        #   save_top_speed()  # Call save_top_speed here instead of after loop
        timelbl.after(100, update_mph)
        print(mph)

        if mph > 1:
            start_timer()
    except KeyboardInterrupt:
        print("Bye bye.")
        

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
window.after(10,update_mph)


window.mainloop()