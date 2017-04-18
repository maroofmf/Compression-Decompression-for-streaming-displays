import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk

'''
# Display a tkinter window
top = tkinter.Tk()
top.mainloop()

# Display a button:
top = tkinter.Tk()
top.geometry("500x500")

def callBak(a):
    msg = messagebox.showinfo("hello","My name is maroof"+str(a))

B = tkinter.Button(top,text='Hello',command= lambda: callBak(100))
B.place(x=0,y=0)
top.mainloop()


#Display image:
window = tkinter.Tk()
window.title('Show')
window.geometry('500x500')
window.configure(background='grey')
path = 'b.jpg'
img = ImageTk.PhotoImage(Image.open(path))
panel = tkinter.Label(window,image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
window.mainloop()
'''

import tkinter as tk
import time
images = ['a.jpg','b.jpg']


window=tk.Tk()
window.geometry('500x500')
window.title('Show Images')
window.configure(background='grey')
img = ImageTk.PhotoImage(Image.open(images[0]))
panel = tkinter.Label(window,image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
window.mainloop()
