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


import tkinter as tk
import time

class play():

    def __init__(self):
        self.images = ['a.jpg','b.jpg']
        self.window=tk.Tk()
        self.index = 0
        self.window.geometry('500x500')
        self.window.title('Show Images')
        self.window.configure(background='grey')
        img = ImageTk.PhotoImage(Image.open(self.images[0]))
        self.panel = tkinter.Label(self.window,image = img)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        self.window.after(0,self.refresh)
        self.window.mainloop()

    def refresh(self):
        img = ImageTk.PhotoImage(Image.open(self.images[0]))
        self.index +=1
        self.panel.config(image = img)

        #panel = tkinter.Label(self.window,image = img)
        #panel.pack(side = "bottom", fill = "both", expand = "yes")
        self.window.after(500,self.refresh)

a = play()

import tkinter as tk
import time

root = tk.Tk()

topFrame = tk.Frame(root)
topFrame.pack()

bottomFrame = tk.Frame(root)
bottomFrame.pack(side = tk.BOTTOM)

button1 = tk.Button(topFrame,text = 'Button 1', fg ='red')
button2 = tk.Button(topFrame,text = 'Button 2', fg ='blue')
button3 = tk.Button(topFrame,text = 'Button 3', fg ='green')
button4 = tk.Button(bottomFrame,text = 'Button 4', fg ='purple')

button1.pack(side = tk.LEFT)
button2.pack(side = tk.LEFT)
button3.pack(side = tk.LEFT)
button4.pack(side = tk.BOTTOM)

root.mainloop()
'''




