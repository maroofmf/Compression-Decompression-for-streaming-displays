import tkinter as Tkinter
root = Tkinter.Tk(  )
for r in range(3):
        for c in range(4):
                    Tkinter.Label(root, text='R%s/C%s'%(r,c),
                                        borderwidth=1 ).grid(row=r,column=c)
                    root.mainloop(  )
