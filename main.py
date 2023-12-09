from tkinter import *
from ttkthemes import ThemedTk

# create tkinter window
window = ThemedTk(theme="black")

window.geometry('1024x600')

window.title("Zero2Sixty Box")

lbl = Label(window, text="Hello", font=("Arial Bold", 500))
lbl.config(fg="white")
lbl.grid(column=0, row=0)


window.mainloop()
