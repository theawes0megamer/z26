from tkinter import *
from tkinter import ttk
import gps
import time
import configparser
import os
from math import sin, cos, sqrt, atan2, radians

# create tkinter window
window = Tk()

window.geometry('1024x600')
window.config(bg="black")
window.title("Zero2Sixty Box")

session = gps.gps(mode=gps.WATCH_ENABLE)
start_time = None
quarter_mile_time = None
lat = 0
lon = 0
previous_lat = None
previous_lon = None
distance_traveled = 0.0
quarter_mile_reached = False

global config
config = configparser.ConfigParser(inline_comment_prefixes="#")

def create_config():
    if os.path.exists('config.ini'):
        print('Config file already exists... skipping')
    else:
        config['DEFAULT'] = {'units':'MPH',
                            'acceleration_top_speed': '60',
                            'file_path':'runs.csv'}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

create_config()
config.read('config.ini')
units = config.get('DEFAULT','units')

def save_runs(timer, lat, lon): # Save time, date, top speed, and GPS Coordinates of run
    with open('runs.txt','a') as runs:
        runstr = f"Time: {time.time()}, Latitude: {lat}, Longitude: {lon}, 0-{config.get('DEFAULT','acceleration_top_speed')}: {timer}, 1/4 Mile: {quarter_mile_time}\n"
        runs.write(runstr)

def update_time():
    time_str = session.fix.time
    timelbl.config(text=time_str)
    timelbl.after(100, update_time)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def update_mph():
    global lat
    global lon
    global previous_lat
    global previous_lon
    global distance_traveled
    global quarter_mile_reached
    global start_time
    global quarter_mile_time

    try:
        while 0 == session.read():
            if not (gps.MODE_SET & session.valid):
                return
            if (gps.isfinite)(session.fix.speed):
                if units == 'MPH':
                    mph = session.fix.speed * 2.23693629
                elif units == 'KPH':
                    mph = session.fix.speed * 3.6
                else:
                    print("Units in config file is misconfigured. Program cannot detect which one is chosen.")
                mphstr = f"{mph:.2f} {units}"
                mphlbl.config(text=mphstr)

                lat = session.fix.latitude
                lon = session.fix.longitude

                if previous_lat is not None and previous_lon is not None:
                    # Calculate distance traveled since last update
                    distance = haversine(previous_lat, previous_lon, lat, lon)
                    distance_traveled += distance

                    # Check for quarter mile (0.402336 km)
                    if not quarter_mile_reached and distance_traveled >= 0.402336:
                        quarter_mile_time = time.time() - start_time
                        quarter_mile_reached = True
                        qtrmilelbl.config(text=f"{format_time(quarter_mile_time)}")

                previous_lat = lat
                previous_lon = lon

                if mph > 1 and start_time is None:
                    start_timer()
    except KeyboardInterrupt:
        window.after_cancel(update_mph)
        session.close()
        print("Bye bye.")
        return
    except Exception as e:
        print("Error:", e)
    finally:
        window.after(10, update_mph)

def start_timer():
    global start_time
    if start_time is None:
        start_time = time.time()
        update_timer()

def update_timer():
    global start_time
    global mph
    global elapsed_time
    global timer

    if start_time is not None and mph > 0:
        elapsed_time = time.time() - start_time
        timer_str = format_time(elapsed_time)
        timerlbl.config(text=timer_str)
        timerlbl.after(5, update_timer)

def format_time(seconds):
    return "{:.2f}s".format(seconds)

def reset_timer():
    global start_time
    global elapsed_time
    global distance_traveled
    global quarter_mile_reached
    global previous_lat
    global previous_lon
    global quarter_mile_time
    start_time = None
    elapsed_time = 0
    distance_traveled = 0.0
    quarter_mile_reached = False
    previous_lat = None
    previous_lon = None
    quarter_mile_time = None
    timerlbl.config(text="")
    qtrmilelbl.config(text="")

# UI Elements
z26lbl = Label(window, text="  Zero2Sixty Box", font=("Lato", 20), fg="white", bg="black")
z26lbl.grid(column=1, row=1, padx=20, pady=20, sticky="w")
z26lbl.columnconfigure(1, weight=1)

timelbl = Label(window, text="", font=("Lato", 20), fg="white", bg="black", width=45)
timelbl.grid(row=1, column=2, padx=20, pady=20, sticky="w")

mphlbl = Label(window, text="", font=("Lato", 60), fg="white", bg="black", width=10)
mphlbl.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

timerlbl = Label(window, text="", font=("Lato", 60), fg="white", bg="black", width=7)
timerlbl.grid(row=2, column=2, padx=20, pady=20, sticky="w")

qtrmilelbl = Label(window, text="", font=("Lato", 30), fg="white", bg="black")
qtrmilelbl.grid(row=3, column=1, padx=20, pady=20, sticky="w")

reset_timer_button = Button(window, text="Reset Timer", command=reset_timer)
reset_timer_button.grid(row=4, column=2)

save_runs_button = Button(window, text="Save Run", command=lambda: save_runs(elapsed_time, lat, lon))
save_runs_button.grid(row=4, column=1)

update_time()
window.after(10, update_mph)
window.mainloop()
