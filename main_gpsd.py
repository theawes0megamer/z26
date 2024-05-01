from tkinter import *
from tkinter import ttk
#import datetime as time
import gps # type: ignore
import time
import configparser
import os



# create tkinter window
window = Tk()

window.geometry('1024x600')
window.config(bg="black")
window.title("Zero2Sixty Box")

session = gps.gps(mode=gps.WATCH_ENABLE)
start_time = None
lock=None
config.read() # Read config
#rbstyle = ttk.Style()
#rbstyle.configure('TButton',font=("Lato",15,'bold'))


def create_config():
    global config
    config = configparser.ConfigParser(inline_comment_prefixes="#")
    if os.path.exists('config.ini'): # If config file already exists, skip creating a new one
        print('Config file already exists... skipping')
    if not os.path.exists('config.ini'): # If it doesn't exist, create it with default values
        config['DEFAULT'] = {'units':'MPH # MPH OR KPH',
                            'acceleration_stop_speed': '60 # do not put any units here, only number',
                            'file_path':'runs.csv'}
        with open('config.ini', 'w') as configfile: # Write the config file
            config.write(configfile)

create_config()

global units
units = config.get('DEFAULT','units')
print(units)

def update_time():  # Update the time in the UI
    # if gps.TIME_SET & session.valid:
    #     time_iso = parser.parse(str(session.fix.time))  # CODE ISN'T WORKING.. NEED TO PARSE ISO8601 TIME INTO READABLE EG. December 24 2024, 6:15PM
    #     print(time_iso)
        # time_str = time_iso.strptime("%B %d, %Y, %I:%M:%S %p")
    time_str = session.fix.time
    timelbl.config(text=time_str)
    timelbl.after(100, update_time)

def update_mph():
    global mph
    global start_time
    global units
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
                lock = session.fix.mode
                
            if lock == 1:
                sat_lock = "No Lock"
            if lock == 2:
                sat_lock = "2D"
            if lock == 3:
                sat_lock = "3D"
                satslbl.config(text=f"{sat_lock}")

            if mph > 1:
                start_timer()
    except KeyboardInterrupt:
        window.after_cancel(update_mph)
        session.close()
        print("Bye bye.")
        return
    except Exception as e:
        print("Error:", e)
    finally:
        window.after(10,update_mph)
        

def start_timer():  # Start the 0-60 MPH timer
    global start_time
    if mph > 2 and mph < 4 and not start_time:
        start_time = time.time()
        update_timer()

def update_timer():  # Update the timer with new values
    global start_time
    global mph
    global elapsed_time
    current_speed = mph
    if current_speed > 0 and current_speed < config.get('DEFAULT','acceleration_top_speed'):
        elapsed_time = time.time() - start_time
        timer_str = format_time(elapsed_time)
        timerlbl.config(text=timer_str)
        timerlbl.after(10, update_timer)
    elif current_speed >= config.get('DEFAULT','acceleration_top_speed') and start_time:
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
    global mph
    if mph > top_speed:
        top_speed = mph
        topspeed_string = f"{top_speed:.1f} {units} Top speed"
        tspdlbl.config(text=topspeed_string)

def reset_timer():
    global start_time
    global elapsed_time
    start_time=0
    elapsed_time=0

z26lbl = Label(window, text="  Zero2Sixty Box", font=("Lato", 20), fg="white", bg="black")  # Zero2Sixty Box Label
z26lbl.grid(column=1, row=1, padx=20, pady=20, sticky="w")
z26lbl.columnconfigure(1, weight=1)

timelbl = Label(window, text="", font=("Lato", 20), fg="white", bg="black", width=45)  # Time Label
timelbl.columnconfigure(1, weight=0)
timelbl.rowconfigure(1, weight=0)
timelbl.grid(row=1, column=2, padx=20, pady=20, sticky="w")

mphlbl = Label(window, text="", font=("Lato", 60), fg="white", bg="black", width=10)  # MPH Label
mphlbl.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

tspdlbl = Label(window, text="", font=("Lato", 30), fg="white", bg="black")
tspdlbl.grid(row=3, column=1, padx=60, pady=10, sticky="w")

timerlbl = Label(window, text="", font=("Lato", 60), fg="white", bg="black",width=7)
timerlbl.grid(row=2, column=2, padx=20, pady=20,sticky="w")

satslbl = Label(window, text="", font=("Lato", 20), fg="white", bg="black")
satslbl.grid(row=3, column=2, sticky="we", padx=10)

verlbl = Label(window,text="v0.1.0-alpha.3", font=("Lato", 20), fg="white", bg="black") # Version Label
verlbl.grid(row=6, column=1, sticky="w", padx=10)

reset_timer_button = Button(window,text="Reset Timer",command=reset_timer)
reset_timer_button.grid(row=4,column=2)
update_time()
window.after(100,save_top_speed)
window.after(10,update_mph)


window.mainloop()
