from tkinter import *
from datetime import datetime
import time
import gps

# create tkinter window
window = Tk()

window.geometry('1024x600')
window.config(bg="black")
window.title("Zero2Sixty Box")

gpsd = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

def update_time(): # Update the time in the UI
    time = datetime.now().strftime("%B %d, %Y, %I:%M:%S %p")
    timelbl.config(text=time)
    timelbl.after(1000, update_time)

def update_mph(): 
    global mph  
    global sats
    mph = 0
    try:
        report = gpsd.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'speed'):
                mph = int(report.speed * 2.23694)  # Convert m/s to MPH

    except StopIteration:
        pass
    mphstr=str(mph) + " MPH"
    
    # GPS INTEGRATION
    
    mphlbl.config(text=mphstr)
    timelbl.after(100,update_mph)
    if mph > 1:
        start_timer()

        


def start_timer(): # Start the 0-60 MPH timer
    global mph
    global start_time
    
    if mph > 1 and not start_time:
        start_time = time.time()
        update_timer()

def update_timer(): # Update the timer with new values
    current_speed = mph
    if current_speed > 0 and current_speed <= 60:
        elapsed_time = time.time() - start_time
        timer_str = format_time(elapsed_time)
        timerlbl.config(text=timer_str)
        timerlbl.after(10, update_timer)
    elif current_speed > 60 and start_time:
        timerlbl.config(text=format_time(time.time() - start_time))
    else:
        timerlbl.config(text="")

def format_time(seconds): # Format the time for display
    return "{:.2f}s".format(seconds)

def save_top_speed():
    global top_speed
    if top_speed < mph:
        top_speed = mph
        topspeed_string=str(top_speed) + " MPH Top speed"
        tspdlbl.config(text=topspeed_string)
        tspdlbl.after(100,save_top_speed)


mph=0
start_time = None
top_speed=0
previous_runs = []

z26lbl = Label(window, text="  Zero2Sixty Box", font=("Lato",20), fg="white",bg="black") # Zero2Sixty Box Label
z26lbl.grid(column=1, row=1, padx=20, pady=20, sticky="w") 
z26lbl.columnconfigure(1, weight=1)

timelbl = Label(window, text="", font=("Lato",20), fg="white",bg="black",width=45) # Time Label
timelbl.columnconfigure(1,weight=0)
timelbl.rowconfigure(1,weight=0)
timelbl.grid(row=1, column=2,padx=20, pady=20, sticky="w")

mphlbl = Label(window, text="",font=("Lato",60), fg="white",bg="black",width=7) # MPH Label
mphlbl.grid(row=2,column=1,padx=20,pady=20, sticky="ew")

tspdlbl = Label(window, text="",font=("Lato",30), fg="white",bg="black")
tspdlbl.grid(row=3,column=1,padx=60,pady=10,sticky="w")

timerlbl = Label(window, text="", font=("Lato",60), fg="white",bg="black")
timerlbl.grid(row=2,column=2,padx=20,pady=20)


update_time() # Call the funtion to update time
update_mph()
save_top_speed()

window.mainloop()
