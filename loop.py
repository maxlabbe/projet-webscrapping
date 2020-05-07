from tkinter import *
import time

root = Tk()
frame = Frame(root)
frame.pack()

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )
photo = PhotoImage(file='Figure 2020-05-04 083548.png')
for i in range(10):
    redbutton = Button(frame, text=i, fg="red")
    redbutton.pack( side = LEFT)
    

    greenbutton = Button(frame, image=photo, height=20, width=50)
    greenbutton.pack( side = LEFT )
    
    bluebutton = Button(frame, text="Blue", fg="blue")
    bluebutton.pack( side = LEFT )
    
    blackbutton = Button(bottomframe, text="Black", fg="black")
    blackbutton.pack( side = BOTTOM)
    
    yellowbutton = Button(bottomframe, text='yellow', fg="yellow")
    yellowbutton.pack( side = RIGHT)
    
    root.update()
    time.sleep(0.5)
    
    greenbutton.destroy()
    bluebutton.destroy()
    blackbutton.destroy()
    yellowbutton.destroy()
    redbutton.destroy()

redbutton = Button(frame, text=i, fg="red")
redbutton.pack( side = LEFT)
    

greenbutton = Button(frame, image=photo)
greenbutton.pack( side = LEFT )
    
bluebutton = Button(frame, text="Blue", fg="blue")
bluebutton.pack( side = LEFT )

blackbutton = Button(bottomframe, text="Black", fg="black")
blackbutton.pack( side = BOTTOM)
    
yellowbutton = Button(bottomframe, text='yellow', fg="yellow")
yellowbutton.pack( side = RIGHT)
root.mainloop()