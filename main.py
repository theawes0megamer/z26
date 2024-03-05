from tkinter import *
from datetime import datetime
import time
import serial
import pyubx2




# create tkinter window
window = Tk()

window.geometry('1024x600')
window.config(bg="black")
window.title("Zero2Sixty Box")

stream = serial.Serial('/dev/ttyS0', 115200, timeout=3)

def receive_data():
    while True:
        data = ser.read(ser.inWaiting())
        print("Received data:", data.decode('utf-8'))
        # Process the data as needed

receive_data()

def update_time(): # Update the time in the UI
    time = datetime.now().strftime("%B %d, %Y, %I:%M:%S %p")
    timelbl.config(text=time)
    timelbl.after(1000, update_time)

### THIS IS AN EXAMPLE FUNCTION FOR REPORTING THE NUMBER OF SATS IT IS NOT FINISHED!!! ###

# def update_gps_info(): # number of sats, 2d/3d lock info
#     global sats
#     global lock_status
    
 
#       sats = report['satellites']
 #       satslbl.config(text=str(sats) + lock_status)
    

def update_gps_info(): # number of sats, 2d/3d lock info
    global sats, lock_status
    
    if stream.inWaiting(): # Check if there is data available from the serial port
        raw_data = stream.read(stream.inWaiting()) # Read the incoming data from the serial port
        report = pyubx2.parse(raw_data) # Parse the received UBX messages
        sats = report['NAV-SOL']['numSV'] if 'NAV-SOL' in report else 0
        lock_status = '2D' if report['NAV-STATUS']['fixType'] == 1 else '3D'
    
    satslbl.config(text=str(sats)) # Update the status label with the number of satellites acquired

def update_mph(): 
    global mph  

    try:
        ubr = pyubx2.UBXReader(stream)
        (raw_data,parsed_data) = ubr.read()
        if parsed_data is not None:
            if hasattr(parsed_data,'gSpeed'):
                mph = parsed_data.gSpeed * 2.23694
                #sats = parsed_data.numSV
    except StopIteration:
        pass
    mphstr=str(mph) + " MPH"
    
    mphlbl.config(text=mphstr)
    timelbl.after(100,update_mph)
    if mph > 1:
        start_timer()

        


def start_timer(): # Start the 0-60 MPH timer
    global start_time
    start_time = None
    
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
    elif current_speed == 0 and start_time > 0: # reset timer when you go below 1mph 
        start_time=0
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

satslbl = Label(window, text="34 Sats", font=("Lato",20), fg="white",bg="black")
satslbl.grid(row=3,column=2,sticky="we",padx=10)



update_time() 
update_mph()
save_top_speed()
update_gps_info()

window.mainloop()
