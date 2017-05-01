from tkinter import *

def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

root = Tk()
root.bind('<Motion>', motion)
root.mainloop()
