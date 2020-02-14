from tkinter import *
from random import *

#def jump():
#    button1.place(relx=random(), rely=random())

#master = Tk()

#button1 = Button(master, text="Hello World", command=jump)
#button1.place(relx=0.5, rely=0.5, anchor=CENTER)

#mainloop()

##root = Tk()
##
##c = Canvas(root, width=80, height=40)
##c.pack()
##c.create_line(0, 20, 80, 20)
##
##root.mainloop()

root = Tk()
def userStay():
    print("You have chosen to stay.")

def userHit():
    print("You have chosen to hit.")

buttonStay = Button(root, text="Stay",command=userStay)
buttonStay.place(relx=0.25,rely=0.75,anchor=CENTER)
buttonHit = Button(root, text="Hit",command=userHit)
buttonHit.place(relx=0.75,rely=0.75,anchor=CENTER)

root.mainloop()
