from tkinter import *
import numpy as np
import time

root = Tk()
root.geometry('200x200')
t = Label(root,text='hello')
t.pack()

def refresh():
    global root
    t.config(text=str(np.random.randint(0,4,1)[0]))
    time.sleep(0.2)
    t.pack()
    root.after(11,refresh)


root.after(100,refresh)
root.mainloop()
