import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call


def getinstructor():

    # Update user and password 
    con=mysql.connect(host="localhost",user="root",password="Arti@123",db="fitnessstudio")
    cursor=con.cursor()
    cursor.execute("select name from instructor where semflag = true")
    results=cursor.fetchall()
    print(results)
    options = list(results)
    print(options)    
    clicked2=StringVar()
    drop = OptionMenu( FS , clicked2, options)
    drop.place(x = 450, y = 250, width = 200)
    
def submit_details():
    fs_zoomlink.get()
    fs_sem_id.get()
    con=mysql.connect(host="localhost",user="root",password="Arti@123",db="fitnessstudio")
    cursor=con.cursor()
    cursor.execute("Insert admin VALUES (fs_zoomlink=(%s),fs_sem_id=(%s))",[(fs_zoomlink),(fs_sem_id)])
    results=cursor.fetchall()    

FS=tk.Tk()
FS.title("fitness_seminar_page")
FS.geometry("800x600")


Label1 = tk.Label(FS, text ="Fitness seminar Zoomlink", )
Label1.place(x = 150, y = 50)

fs_zoomlink = tk.Entry(FS, width = 35)
fs_zoomlink.place(x = 300, y = 50, width = 200)

Label2 = tk.Label(FS, text ="Seminar ID", )
Label2.place(x = 150, y = 100)

fs_sem_id= tk.Entry(FS, width = 35)
fs_sem_id.place(x = 300, y = 100, width = 200)

Label3 = tk.Label(FS, text ="Type", )
Label3.place(x = 150, y = 150)


clicked=StringVar()
clicked.set("live")
drop = OptionMenu( FS , clicked, "live","recorded")
drop.place(x = 300, y = 150, width = 200)



submitbtn = tk.Button(FS, text ="Fetch available seminar instructors", bg ='white',command=getinstructor)
submitbtn.place(x = 250, y = 250, width = 150 )

submitbtn = tk.Button(FS, text ="CREATE_SEMINAR", bg ='white',command =submit_details)
submitbtn.place(x = 250, y = 300, width = 150)

FS.mainloop()