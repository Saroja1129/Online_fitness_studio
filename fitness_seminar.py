import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call

def Sem_id_generator():
     con=mysql.connect(host="localhost",user="root",password="Arti@123",db="fitnessstudio")
     cursor=con.cursor() 
     cursor.execute("select fs_sem_id from fitness_seminar")
     results = cursor.fetchall()
     a=len(results)
     print(results[a-1])
     S = str(results[a-1]) 
     fs_sem_id= S[2:4]+str(int(S[4:8])+1)
     print(fs_sem_id)
     Label3 = tk.Label(FS, text =fs_sem_id)
     Label3.place(x = 500, y = 100)
     
         
def getadmin():
    
    # Update user and password 
    con=mysql.connect(host="localhost",user="root",password="Arti@123",db="fitnessstudio")
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
      dropdown = OptionMenu(FS, selected ,*options )
      dropdown.place(x = 400, y = 300, width = 200) 
        
    except:
       print("Error: unable to fecth data")     
 
def getinstructor():

    # Update user and password 
    con=mysql.connect(host="localhost",user="root",password="Arti@123",db="fitnessstudio")
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
      dropdown = OptionMenu(FS, selected1 ,*options )
      dropdown.place(x = 400, y = 400, width = 200) 
        
    except:
       print("Error: unable to fecth data")
            
def submit_details():
    a=fs_zoomlink.get()
    con=mysql.connect(host="localhost",user="root",password="Arti@123",db="fitnessstudio")
    cursor=con.cursor() 
    cursor.execute("select fs_sem_id from fitness_seminar order by fs_sem_id")
    results = cursor.fetchall()
    l=len(results)
    print(l)
    S = str(results[l-1]) 
    b= S[2:4]+str(int(S[4:8])+1)
    c=clicked.get()
    d=selected.get()
    e=selected1.get()
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    
    try:
      con=mysql.connect(host="localhost",user="root",password="Arti@123",db="fitnessstudio")
      cursor=con.cursor()
      print("insert into fitness_seminar values(%s,%s,%s,%s,%s)",[a,b,c,d,e])
      #cursor.execute("insert into fitness_seminar(FS_zoomlink,FS_sem_id,FS_type,FS_admin_id,FS_Inst_ID) values('a','a','a','A23675','A00001');,[(a),(b),(c),])
      cursor.execute("insert into fitness_seminar values(%s,%s,%s,%s,%s)",[a,b,c,d,e])
      con.commit()
      results=cursor.fetchall()
      msgbox.showinfo("Create status","Fitness_seminar creation succesfull")
    except:
      print("Error: unable to create")
      msgbox.showinfo("Create status","Fitness_seminar creation unsuccesfull")      

FS=tk.Tk()
FS.title("fitness_seminar_page")
FS.geometry("900x800")

selected = StringVar(FS)
selected1 = StringVar(FS)
fs_sem_id =StringVar(FS)
#fs_sem_id="hi"

Label1 = tk.Label(FS, text ="Fitness seminar Zoomlink", )
Label1.place(x = 250, y = 100)

fs_zoomlink = tk.Entry(FS, width = 35)
fs_zoomlink.place(x = 400, y = 100, width = 200)

# Label2 = tk.Label(FS, text ="Seminar ID", )
# Label2.place(x = 150, y = 200)

# fs_sem_id= tk.Entry(FS, width = 35)
# fs_sem_id.place(x = 300, y = 100, width = 200)

# submitbtn = tk.Button(FS, text ="Get_Seminar_ID", bg ='white',command=Sem_id_generator)
# submitbtn.place(x = 300, y = 100, width = 150 )

Label3 = tk.Label(FS, text ="Type", )
Label3.place(x = 250, y = 175)

clicked=StringVar()
clicked.set("live")
drop = OptionMenu( FS , clicked, "live","recorded")
drop.place(x = 400, y = 175, width = 200)

Label4 = tk.Label(FS, text ="Organiser")
Label4.place(x = 250, y = 250)

adminid = tk.Button(FS, text ="Select Organiser", bg ='white',command =getadmin)
adminid.place(x = 400, y = 250, width = 200)

submitbtn = tk.Button(FS, text ="Fetch available seminar instructors", bg ='white',command=getinstructor)
submitbtn.place(x = 400, y = 350, width = 200)

Label5 = tk.Label(FS, text ="Instructor")
Label5.place(x = 250, y = 350)

submitbtn = tk.Button(FS, text ="CREATE_SEMINAR", bg ='blue',command =submit_details)
submitbtn.place(x = 400, y = 450, width = 150)

FS.mainloop()
