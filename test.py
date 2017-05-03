from tkinter import *
import numpy as np
import time

root = Tk()
root.geometry('200x200')
t = Label(root,text='hello')
t.pack()
jobs=-1
temp = 0
temp2=0
def refresh():
    global jobs
    global temp
    global myTime
    global temp2
    startTime = time.time()
    #t.config(text=str(np.random.randint(0,10000,1)[0]))
    time.sleep(0.05)
    #delay = 100 - int((time.time() - startTime)*1000)
    #print(delay)
    #t.pack()

    #if(time.time()-myTime>1):
        #print(jobs)
        #sys.exit(0)
    #else:
        #jobs+=1
    jobs+=1

    if(time.time()-myTime>1):
        print(jobs)
        print(temp2)
        sys.exit(0)

    #temp += time.time()-startTime
    delay = 100.00-((time.time()-startTime)*1000)

    #Caclulate loss by

    temp+=delay-int(delay)
    #if(temp>1):
    #    temp=0
    #    temp2+=1
    #    delay -=1

    root.after(50,refresh)



myTime = time.time()
refresh()
root.mainloop()
