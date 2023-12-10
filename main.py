from tkinter import *
from datetime import datetime
import time
# create tkinter window
window = Tk()

window.geometry('1024x600')
window.config(bg="black")
window.title("Zero2Sixty Box")


def update_time(): # Update the time in the UI
    time = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    timelbl.config(text=time)
    timelbl.after(1000, update_time)

def update_mph():
    
    
    global mph  
    mph = mph+1
    mphstr=str(mph) + " MPH"
    mphlbl.config(text=mphstr)
    timelbl.after(500,update_mph)

mph=0

z26lbl = Label(window, text="  Zero2Sixty Box", font=("Lato",20), fg="white",bg="black") # Zero2Sixty Box Label
z26lbl.grid(column=1,row=1) 

timelbl = Label(window, text="", font=("Lato",20), fg="white",bg="black") # Time Label
timelbl.columnconfigure(0,weight=1)
timelbl.rowconfigure(0,weight=1)
timelbl.grid(row=1, column=2, sticky="nsew",padx=20, pady=20)

mphlbl = Label(window, text="",font=("Lato",60), fg="white",bg="black")
mphlbl.grid(row=2,column=1,padx=10,pady=10)



update_time() # Call the funtion to update time
update_mph()

window.mainloop()
