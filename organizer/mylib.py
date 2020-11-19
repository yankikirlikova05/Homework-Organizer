from tkinter import Label, Tk, Button, Entry, messagebox, mainloop, Frame, Toplevel
import csv
import datetime

class Homework:
    def __init__(self,name,due_date,subject,addition):
        self.name = name
        self.due_date = due_date
        self.subject = subject
        self.addition = addition

def refresh(self):
    self.destroy()
    self.__init__()

#returns true/false
def is_date_able(entry):
    try:
        day = int(entry[0] + entry[1])
        month = int(entry[3] + entry[4])
        year = int(entry[6:10])
    
    except ValueError:
        return False

    now = datetime.datetime.now()
    today = now.strftime("%d")
    this_month = now.strftime("%m")
    this_year = now.strftime("%Y")

    if month == int(this_month) and year == int(this_year) and day < int(today):
        return False

    elif year == now.year and month < now.month:
        return False

    elif year < now.year:
        return False

    elif entry[2] != "/" or entry[5] != "/" or day > 31 or month > 12:
        return False

    else:
        return True

#uyarı penceresi için
def warning(text, desc):
    messagebox.showerror(text, desc)

#writes data to the csv file 
def add_csv(root, liste):
    with open('homeworks.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        for hw in liste:
            writer.writerow([hw.name, hw.due_date,hw.subject])

#datayı listeden silmek için DELETE TE SIKINTI VAR
def delete(nesne, liste,show,frame, root):
    
    if nesne in liste:
        option = messagebox.askyesno("Delete", "Are You Sure You Want To Delete This Homework?")
        if option == True:
            print(nesne.name)
            liste.remove(nesne)
            for i in liste:
                print(i.name)


    refresh(frame)
    show(frame, delete,root, get_csv, liste)

def delete_homework(liste,show,frame, root):
    def delete_search(name):
        names = []
        for i in liste:
            names.append(i.name)

            if i.name == name.get():
                liste.remove(i)
                lines = list()
                with open('homeworks.csv', 'r') as readFile:
                    reader = csv.reader(readFile)
                    for row in reader:
                        lines.append(row)
                        for field in row:
                            if field == i.name:
                                lines.remove(row)

                with open('homeworks.csv', 'w') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(lines)
                    
                refresh(frame)
                show(frame, delete,root, get_csv, liste)
                delete.destroy()
                return 0
        if name.get() not in names:
            warning("Error", "Homework Not Found! Try another homework name.")


    delete = Toplevel()
    name = Entry(delete, width = 50, borderwidth = 2)
    submit = Button(delete,text="Delete", command=lambda:delete_search(name))
    
    delete.title("Delete Homework")
    name.grid(row=0,column=0)
    submit.grid(row=1,column=0)

#gets data from the csv file
def get_csv(liste, file):
    with open(file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
            hw = Homework(row[0],row[1],row[2],addition = 0)
            liste.append(hw)

#datayı tarihe göre sıralamak
def sorting(liste):
    def func(hw):
        return hw.addition

    for hw in liste:
        month =  100*int(hw.due_date[3] + hw.due_date[4])
        year =  10000*int(hw.due_date[6:10])
        day = int(hw.due_date[0] + hw.due_date[1])
        hw.addition = day  + month + year

    liste.sort(key = func, reverse = False)

#data yı göstermek
def show(frame, delete,root, get_csv, liste):
    sorting(liste)
    no_hw = Label(frame, text="",padx=5,pady=20)
    if len(liste) == 0:
        no_hw["text"] = "You don't have any homework!"

    else:
        no_hw.grid_forget()
        #Label(frame, text="Homeworks:").grid(row=0, column=0)
        delete = Button(frame, text="Delete Homework",command=lambda:delete_homework(liste, show,frame, root),state="active").grid(row=0, column=4)

        no_hw["text"] = "Homeworks:"

    no_hw.grid(row=0, column=0)
    #Will be editted (csv files)
    root.geometry('580x400')
    for i in range(len(liste)):
        name = Label(frame, text=liste[i].name)
        due = Label(frame, text=liste[i].due_date,padx=10)
        subject = Label(frame, text=liste[i].subject)
        #delete_forall = Button(frame, text= f"delete {liste[i].name}",command=lambda: delete(liste[i],liste,show,frame, root))
        name.grid(row=i+1,column=0)
        due.grid(row=i+1,column=1)
        subject.grid(row=i+1,column=2)
        #delete_forall.grid(row=i+1,column=4)

    add_button = Button(frame, text="+",command = lambda: add(frame, liste,show,root,no_hw,delete)).grid(row=0,column=3,padx=10)
    #delete_button = Button(frame, text="Delete Homework",command=delete_homework).grid(row=0, column=4)
    quit_button= Button(frame, text="Quit",fg='red',command=lambda: exit_app(root,liste)).grid(row=0,column=5)

    frame.grid()

def add(frame,liste,show,root,label,delete_button):
    if len(liste) >20:
        messagebox.showerror("Too Many Homeworks", "You may not have more than fifteen homeworks. This is too much work :)")
    def get_all():
        label.destroy()
        newHw = Homework(entry.get(), due.get(), subject.get(), addition = 0)
    
        if len(newHw.name) == 0 or len(newHw.subject) == 0 or is_date_able(newHw.due_date) == False or len(newHw.due_date) != 10:
            warning("Inappropriate Homework Entry", "You must provide a subject, a name, a due date. Due date must not be passed. Also, the due date format must be like that format: \"**/**/****\" (day/month/year).")
            top.destroy()
            show(frame, delete_button,root, get_csv, liste)
            return 1


        liste.append(newHw)
        add_csv(root, liste)
        show(frame, delete_button,root, get_csv, liste)
        top.destroy()

    top = Toplevel()
    top.title('New Homework')
    entry = Entry(top, width = 50, borderwidth = 2)
    due = Entry(top, width = 50, borderwidth = 2)
    subject = Entry(top, width = 50, borderwidth = 2)
    exit_button = Button(top, text="Add Homework",fg="green", command=get_all, state="normal")
    cancel = Button(top, text="Cancel", fg="red", command=top.destroy)

    #input kontrol eklenecek
    Label(top, text="Name: ").grid(row=0, column=0)
    entry.grid(row=0, column=1, columnspan=4)
    Label(top, text="Due Date: ").grid(row=1, column=0)
    due.grid(row=1, column=1, columnspan=4)
    Label(top, text="Subject: ").grid(row=2, column=0)
    subject.grid(row=2, column=1, columnspan=4)
    
    
    exit_button.grid(row=3, column=4)
    cancel.grid(row=3, column=0)

def exit_app(root,liste):
    add_csv("homeworks.csv", liste)
    root.quit()