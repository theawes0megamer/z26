from tkinter import *
from datetime import datetime
import time
import serial 
import pynmea2
from geopy.distance import geodesic  # Install using: pip install geopy


serial_port = "/dev/ttyS0"
baud_rate = 115200

prev_position = None
prev_time = time.time()

gps_serial = serial.Serial(serial_port, baudrate=baud_rate, timeout=1)



# create tkinter window
window = Tk()

window.geometry('1024x600')
window.config(bg="black")
window.title("Zero2Sixty Box")


def update_time(): # Update the time in the UI
    time = datetime.now().strftime("%B %d, %Y, %I:%M:%S %p")
    timelbl.config(text=time)
    timelbl.after(1000, update_time)

def update_mph(): 
    global mph  
    global sats
    mph = 0
    mphstr=str(mph) + " MPH"
    
    # GPS INTEGRATION
    gps_data = gps_serial.readline().decode("utf-8") # read data

    if gps_data.startswith('$GPGGA'):
        try:
            gga_sentence = pynmea2.parse(gps_data)
            sats = gga_sentence.num_sats
            latitude = gga_sentence.latitude
            longitude = gga_sentence.longitude
            current_position = (gga_sentence.latitude, gga_sentence.longitude)
            current_time = time.time()
            if prev_position is not None:
                distance = geodesic(prev_position, current_position).miles

                # Calculate speed (distance / time) in MPH
                 elapsed_time = current_time - prev_time
                 speed_mph = distance / elapsed_time * 3600  # Convert to MPH
                 



            # Use latitude and longitude data as needed
        except pynmea2.ParseError as e:
            print(f"Error parsing GPS data: {e}")

    mphlbl.config(text=mphstr)
    timelbl.after(100,update_mph)
    if mph > 0:
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
