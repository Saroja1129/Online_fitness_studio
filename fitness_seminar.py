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
local_DB_password = args.pw
python_alias= args.alias

# local_DB_password="Arti@123"



def Sem_id_generator():
     con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
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
     
# def getname(selected1):
#       con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
#       cursor=con.cursor()
#       print(selected1)
#       cursor.execute("select name from instructor where id =" +  "'" + str(selected1) + "'"  )
#       # cursor.execute("select name from instructor where id ='A00001'"  )
      
#       results=cursor.fetchall() 
#       print(results)   
#       myFeedback = str(results)        
#       l=len(results)
#       S = str(results[l-1]) 
#       e = int(S[2:8])
#       feedbackEntry = tk.Entry(FS, width = 60) # entry is a text box
#       feedbackEntry.insert(END,e)
#       feedbackEntry.place(x = 800, y = 400, width = 100)
         
def getadmin():
    
    # Update user and password 
    con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
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
    con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
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
      
      # submitbtn = tk.Button(FS, text ="Inst_name", bg ='white',command=lambda:getname(selected1))
      # submitbtn.place(x = 650, y = 400, width = 100)
      
      
      
            
    except:
       print("Error: unable to fecth data")
            
def submit_details():
    a=fs_zoomlink.get()
    con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
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
    f=fs_name.get()
    g=date.get()
    h=time.get()
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    
    try:
      con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
      cursor=con.cursor()
      print("insert into fitness_seminar values(%s,%s,%s,%s,%s)",[a,b,c,d,e])
      #cursor.execute("insert into fitness_seminar(FS_zoomlink,FS_sem_id,FS_type,FS_admin_id,FS_Inst_ID) values('a','a','a','A23675','A00001');,[(a),(b),(c),])
      cursor.execute("insert into fitness_seminar values(%s,%s,%s,%s,%s,%s,%s,%s)",[a,b,c,d,e,f,g,h])
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

Label0 = tk.Label(FS, text ="Fitness seminar Title", )
Label0.place(x = 250, y = 50)

fs_name = tk.Entry(FS, width = 35)
fs_name.place(x = 400, y = 50, width = 200)

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

# EntryFSInst = tk.Entry(FS, width = 35)
# EntryFSInst.place(x = 400, y = 550, width = 200)

# con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
# cursor=con.cursor()
# cursor.execute("select name from instructor where id='A00001'"  )
# cursor.execute("select name from instructor where id ="+ "'"+str(selected1)+"'" +""  )
# results=cursor.fetchall()
    
# myFeedback = results[0][0]
    
# feedbackEntry = tk.Entry(FS, width = 50) # entry is a text box
# feedbackEntry.insert(END,myFeedback)
# feedbackEntry.place(x = 400, y = 550, width = 400)

Label5 = tk.Label(FS, text ="Instructor")
Label5.place(x = 250, y = 350)

Label5 = tk.Label(FS, text ="Fitness seminar date", )
Label5.place(x = 250, y = 450)

date = tk.Entry(FS, width = 35)
date.place(x = 400, y = 450, width = 200)

lbl_time = tk.Label(FS, text ="Fitness seminar Time", )
lbl_time.place(x = 250, y = 500)

time = tk.Entry(FS, width = 35)
time.place(x = 400, y = 500, width = 200)

submitbtn = tk.Button(FS, text ="CREATE_SEMINAR", bg ='blue',command =submit_details)
submitbtn.place(x = 400, y = 600, width = 150)

FS.mainloop()


