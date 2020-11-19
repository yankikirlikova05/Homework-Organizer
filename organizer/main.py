from tkinter import Label, Tk, Button, Entry, messagebox, mainloop, Frame, Toplevel
from mylib import *
import os

root = Tk()
root.title("Homeworks")
root.geometry('490x400')

homeworks = []
frame = Frame(root)

#write data to the list 
try:
    get_csv(homeworks, file="homeworks.csv")
    for i in homeworks:
        print(i.name)

except FileNotFoundError:
    os.system("touch homeworks.csv")


no_hw = Label(frame, text="You don't have any homework!",padx=5,pady=20)
delete_button = Button(frame, text="Delete Homework",command=lambda:delete_homework(homeworks, show,frame, root),state="disabled").grid(row=0, column=4)
if len(homeworks) < 1:
    no_hw.grid(row=0, column=0)

else:
    sorting(homeworks)
    refresh(frame)
    show(frame, delete_button,root, get_csv, homeworks)


frame.grid()
root.mainloop()