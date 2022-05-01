import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call
import argparse


# pass current user information
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
parser.add_argument("--alias", help = "python alias")
args = parser.parse_args()
user = args.input
local_DB_Password = args.pw
python_alias= args.alias

def changed():
    a=Mem_level.get()
    b=Mem_cost.get() 
    print(a)
    print(b)
    try:
        m = mysql.connect(host="localhost", user="root", passwd=local_DB_Password, database="fitnessstudio" )
        connection = m.cursor()
        connection.execute("update membership set mem_cost=%s where mem_level=%s",[b,a])
        myresult = connection.fetchall()
        m.commit()
        msgbox.showinfo("Error Status","Updation done") 
    except:
        msgbox.showinfo("Error Status","Not done") 
        

a=tk.Tk()
a.geometry("200x300")

Label_1 = tk.Label(a, text ="Membership level", )
Label_1.place(x=10, y=10)

Mem_level = tk.Entry(a, width = 20)
Mem_level.place(x=10, y= 50)

Label_2 = tk.Label(a, text ="Membership cost", )
Label_2.place(x=10, y= 100)

Mem_cost = tk.Entry(a, width = 20)
Mem_cost.place(x=10, y= 150)



submitbtn1 = tk.Button(a, text ="Modify",bg ='silver', command=changed)
submitbtn1.place(x=10,y=200)
a.mainloop()
