import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as tkmb
from tkinter import *
from subprocess import call
from PIL import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
parser.add_argument("--alias", help="python alias")
args = parser.parse_args()
#inst_email = args.input
#local_DB_password = args.pw
usr="root"
local_DB_password = "password"
#python_alias= args.alias
python_alias="python3"


def question():
    tkmb.showinfo("", "Any questions, please contact our office!")
    training_instructor.destroy()
    call([python_alias,"Instructor.py","--input", usr, "--pw",local_DB_password])

def sessionsContent():
    sessions = tk.Tk()
    sessions.title("My Training Sessions List")
    sessions.geometry("1000x600") 
        
    label = tk.Label(sessions, text ="Training Sessions" )
    label.config(font=("Courier", 20))
    label.place(x = 10, y = 20)

    sessionsList = results 
    print(sessionsList)
  
    i = 0
    for session in sessionsList: 
        j = 0
        #print("____", session)
       	for j in range(len(sessionsList)):
            j = 0
            for j in range(len(session)):
                e = Entry(sessions,width=20, fg='blue')
                e.grid(row=i, column=j) 
                e.insert(END, session[j])
                x1 = 50+j*100
                y1 = 70 +i*30
                e.place(x = x1 , y = y1)      
        
        i=i+1

        questionButton = tk.Button(sessions, text ="Questions?", bg ='gray', command=question)
        questionButton.place(x = 430, y = 500, width = 100)

    sessions.mainloop()


#inst_email = "Isflwr@555.net"
inst_email = "kyra.forester@gmail.com"

con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
cursor=con.cursor()

cursor.execute("select Name,ID from Instructor where Email = '" + str(inst_email)+"'")
results=cursor.fetchall()
#print(results)
instructor_name = results[0][0]
instructor_id = results[0][1]

cursor.execute("select * from training_session where session_instructor_id = '" + str(instructor_id)+"'")
results=cursor.fetchall()
print(results)

training_instructor=tk.Tk()
training_instructor.title("Training Session Page for Instructors")
training_instructor.geometry("800x500")
l = tk.Label(training_instructor, text ="Your scheduled Training Sessions, Instructor "+str(instructor_name) + "!")

l.config(font=("Courier", 20))
l.place(x = 40, y = 100)

loadButton = tk.Button(training_instructor, text ="Load My Sessions", bg ='gray', command=sessionsContent)
loadButton.place(x = 200, y = 240, width = 200)

training_instructor.mainloop()
