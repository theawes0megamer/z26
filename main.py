from tkinter import *
from datetime import datetime
import time
# create tkinter window
window = Tk()

window.geometry('1024x600')
window.config(bg="black")
window.title("Zero2Sixty Box")


def update_time(): # Update the time in the UI
    time = datetime.now().strftime("%B %d, %Y, %I:%M:%S %p")
    timelbl.config(text=time)
    timelbl.after(1000, update_time)

def update_mph(): # Function to simulate 0-60
    global mph  
    mph = mph+1
    mphstr=str(mph) + " MPH"
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


mph=0
start_time = None

z26lbl = Label(window, text="  Zero2Sixty Box", font=("Lato",20), fg="white",bg="black") # Zero2Sixty Box Label
z26lbl.grid(column=1,row=1,padx=20,pady=20) 

timelbl = Label(window, text="", font=("Lato",20), fg="white",bg="black",width=60) # Time Label
timelbl.columnconfigure(0,weight=1)
timelbl.rowconfigure(0,weight=1)
timelbl.grid(row=1, column=2, sticky="w",padx=20, pady=20)

mphlbl = Label(window, text="",font=("Lato",60), fg="white",bg="black") # MPH Label
mphlbl.grid(row=2,column=1,padx=20,pady=20)

timerlbl = Label(window, text="", font=("Lato",60), fg="white",bg="black")
timerlbl.grid(row=2,column=2,padx=20,pady=20)


update_time() # Call the funtion to update time
update_mph()

window.mainloop()
