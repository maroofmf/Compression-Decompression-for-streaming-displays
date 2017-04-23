from tkinter import *
from PIL import Image,ImageTk


class display:

    def __init__(self):
        self.fileName = 'b.jpg'
        self.root = Tk()
        self.frame = Frame(self.root)
        self.frame.pack()
        self.panel = Label(self.frame)
        self.test()
        self.root.after(2000,self.shift)
        self.root.mainloop()

    def test(self):
        self.img = ImageTk.PhotoImage(Image.open(self.fileName))
        self.panel = Label(self.frame, image = self.img)
        #panel.pack(side = "bottom", fill = "both", expand = "no")
        self.panel.pack()

    def shift(self):
        self.img = ImageTk.PhotoImage(Image.open('a.jpg'))
        self.panel.config(image = self.img)
        self.panel.pack()


a = display()
