import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox

from tkinter import *
from subprocess import call
from PIL import *
import argparse

# pass current user information
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
args = parser.parse_args()
user = args.input
local_DB_password = args.pw
LocalDbPassword="Arti@123"

def getclient():
    con=mysql.connect(host="localhost",user="root",password=LocalDbPassword,db="fitnessstudio")
    cursor=con.cursor()
    movieList = []
    try:
      cursor.execute("select distinct client_id from client")
      results = cursor.fetchall()
      for a in results:
        data =  (a[0])
        movieList.append(data)
            
      selected2.set(movieList[0])
      options=movieList 
      dropdown = OptionMenu(Tran_ses, selected2 ,*options )
      dropdown.place(x = 350, y = 540, width = 200) 
        
    except:
       print("Error: unable to fecth data")  

def getinstructor():
    
    # Update user and password 
    con=mysql.connect(host="localhost",user="root",password=LocalDbPassword,db="fitnessstudio")
    cursor=con.cursor()
    movieList = []
    try:
      cursor.execute("select distinct trainer_id from instructor where semflag = true")
      results = cursor.fetchall()
      for a in results:
        data =  (a[0])
        movieList.append(data)
            
      selected1.set(movieList[0])
      options=movieList 
      dropdown = OptionMenu(Tran_ses, selected1 ,*options )
      dropdown.place(x = 350 ,y = 450, width = 200) 
        
    except:
       print("Error: unable to fecth data")
            

def getadmin():
    
    # Update user and password 
    con=mysql.connect(host="localhost",user="root",password=LocalDbPassword,db="fitnessstudio")
    cursor=con.cursor()
    movieList = []
    try:
      cursor.execute("select distinct admin_id from admin")
      results = cursor.fetchall()
      for a in results:
        data =  (a[0])
        movieList.append(data)
            
      selected.set(movieList[0])
      options=movieList 
      dropdown = OptionMenu(Tran_ses, selected ,*options )
      dropdown.place(x = 350, y = 360, width = 200) 
        
    except:
       print("Error: unable to fecth data") 
       
       
def submitact():
    a=Name.get() #sessio_name
    con=mysql.connect(host="localhost",user="root",password=LocalDbPassword,db="fitnessstudio")
    cursor=con.cursor() 
    cursor.execute("select session_id from training_session order by session_id")
    results = cursor.fetchall()
    l=len(results)
    S = str(results[l-1]) 
    e = int(S[2:8])+1 #session_id
    print(e)
    b=clicked.get() #live/recorded
    c=clicked1.get() #group/individual
    f=selected.get() #admin_id
    h=selected1.get() #inst_id
    d=zoomlink.get()
    g=selected2.get()
 
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
    print(g)
    print(h)
    
    try:
      con=mysql.connect(host="localhost",user="root",password=LocalDbPassword,db="fitnessstudio")
      cursor=con.cursor()
      print("insert into training_session values(%s,%s,%s,%s,%s,%s,%s,%s)",[a,b,c,d,e,f,g,h])
      #cursor.execute("insert into fitness_seminar(FS_zoomlink,FS_sem_id,FS_type,FS_admin_id,FS_Inst_ID) values('a','a','a','A23675','A00001');,[(a),(b),(c),])
      cursor.execute("insert into training_session values(%s,%s,%s,%s,%s,%s,%s,%s)",[a,b,c,d,e,f,g,h])
      con.commit()
      results=cursor.fetchall()
      msgbox.showinfo("Create status","Fitness_seminar creation succesfull")
    except:
      print("Error: unable to create")
      msgbox.showinfo("Create status","Fitness_seminar creation unsuccesfull")



Tran_ses=tk.Tk()
Tran_ses.title("Training_session")
Tran_ses.geometry("800x600")

selected = StringVar(Tran_ses)
selected1 = StringVar(Tran_ses)
selected2 = StringVar(Tran_ses)

Label_Name = tk.Label(Tran_ses, text ="Session Instructor Name", font=('bold',10) )
Label_Name.place(x = 200, y = 20)
Name = tk.Entry(Tran_ses, width = 35)
Name.place(x = 350, y = 20, width = 200)

Label_ST = tk.Label(Tran_ses, text ="Session_Type :", font=('bold',10) )
Label_ST.place(x = 200, y = 80)
clicked=StringVar()
clicked.set("live")
drop = OptionMenu( Tran_ses , clicked, "live","recorded")
drop.place(x = 350, y = 80, width = 200)

Label_ST = tk.Label(Tran_ses, text ="Session(Individual/group)", font=('bold',10) )
Label_ST.place(x = 200, y = 160)
clicked1=StringVar()
clicked1.set("Individual")
drop1 = OptionMenu( Tran_ses , clicked1, "Group","Individual")
drop1.place(x = 350, y = 160, width = 200)

Label_zoom = tk.Label(Tran_ses, text ="Session Zoomlink", font=('bold',10) )
Label_zoom.place(x = 200, y = 240)
zoomlink = tk.Entry(Tran_ses, width = 35)
zoomlink.place(x = 350, y = 240, width = 200)

#can change if we use argparse
Label_admin = tk.Label(Tran_ses, text ="Session admin", font=('bold',10) )
Label_admin.place(x = 200, y = 320)
adminid = tk.Button(Tran_ses, text ="Select Organiser", bg ='white',command =getadmin)
adminid.place(x = 350, y = 320, width = 200)


Label_inst = tk.Label(Tran_ses, text ="Session instructor", font=('bold',10) )
Label_inst.place(x = 200, y = 400)
inst = tk.Button(Tran_ses, text ="Get instructor ", bg ='white',command =getinstructor)
inst.place(x = 350, y = 400, width = 200)

Label_client = tk.Label(Tran_ses, text ="client", font=('bold',10) )
Label_client.place(x = 200, y = 500)
client = tk.Button(Tran_ses, text ="Select client", bg ='white',command =getclient)
client.place(x = 350, y = 500, width = 200)

submitbtn = tk.Button(Tran_ses, text ="CREATE_SEMINAR", bg ='blue',command =submitact)
submitbtn.place(x = 350, y = 600, width = 150)

Tran_ses.mainloop()
