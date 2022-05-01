import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox


from tkinter import *
from subprocess import call
from hashlib import pbkdf2_hmac # for hash function
from PIL import *

#Change here for your local DB password
local_DB_password = "Arti@123"
python_alias = "python"


def Register():
            Admin.destroy()
            #call client Registration page instead of admin
            call(["python","Register.py"])
            return True

# Hash incoming passwords 
def hashPassword(passw):

    iter = 500_000 

    #Convert password (string) into byte
    passw_b = str.encode(passw)
    hash = pbkdf2_hmac('sha256', passw_b, b'salt'*2, iter)

    return str(hash.hex())


def submitact():
      
    user = Username.get()
    passw = Password.get()
    passw = hashPassword(passw)      
    a=clicked.get()
    

    if(user=="" or passw==""):
        msgbox.showinfo("Insert status","all fields are required")
    elif(a=='Admin'):
     
        con=mysql.connect(host="localhost",user="root",password=local_DB_password, db="fitnessstudio") 
        cursor=con.cursor()
        cursor.execute("select * from admin where admin_email = %s and admin_pwd=%s", [(user),(passw)] )
        results=cursor.fetchall()
        if results:
            msgbox.showinfo("Login status","lOGIN SUCCESSFULL")
            Admin.destroy()
            call([python_alias,"adminHome.py","--input", user, "--pw", local_DB_password ])
            return True
        else:
            msgbox.showinfo("Login status","lOGIN UNSUCCESSFULL")
            return False
        
    elif(a=='Client'):
            # Update user and password
        con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
        cursor=con.cursor()
        cursor.execute("select * from client where client_email = %s and client_pwd =%s", [(user),(passw)] )
        results=cursor.fetchall()
        if results:
            msgbox.showinfo("Login status","lOGIN SUCCESSFULL")
            Admin.destroy()
            #call client home_page instead of admin
            call([python_alias,"client_home.py","--input", user, "--pw", local_DB_password ])
            return True
        else:
            msgbox.showinfo("Login status","lOGIN UNSUCCESSFULL")
            return False
    
    elif(a=='Advisor'):
            # Update user and password
        con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
        cursor=con.cursor()
        cursor.execute("select * from advisor where email = %s and password =%s", [(user),(passw)] )
        results=cursor.fetchall()
        if results:
            msgbox.showinfo("Login status","lOGIN SUCCESSFULL")
            Admin.destroy()
            #call client home_page instead of admin
            call([python_alias,"advisor_home.py","--input", user, "--pw", local_DB_password ])
            return True
        else:
            msgbox.showinfo("Login status","lOGIN UNSUCCESSFULL")
            return False
    
    elif(a=='Instructor'):
             # Update user and password
         con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
         cursor=con.cursor()
         cursor.execute("select * from Instructor where email = %s and Password =%s", [(user),(passw)] )
         results=cursor.fetchall()
         if results:
             msgbox.showinfo("Login status","lOGIN SUCCESSFULL")
             Admin.destroy()
             
             call([python_alias,"Instructor.py","--input", user, "--pw", local_DB_password ]) # TODO call client home_page instead of admin
             return True
         else:
             msgbox.showinfo("Login status","lOGIN UNSUCCESSFULL")
             return False    
                
           
            
Admin=tk.Tk()
Admin.title("Fitness_Studio")
Admin.geometry("900x900")

Label_IH = tk.Label(Admin, text ="Welcome To Online Fitness Studio" )
Label_IH.config(font=("Courier", 30))
Label_IH.place(x = 30, y = 20)

Label_Domain = tk.Label(Admin, text ="Domain ", font=('bold',10) )
Label_Domain.place(x = 200, y = 210)

clicked=StringVar()
clicked.set("Admin")
drop = OptionMenu( Admin , clicked, "Admin","Instructor","Client","Advisor")
drop.place(x = 300, y = 210, width = 200)



Label_User_name = tk.Label(Admin, text ="UserName ", )
Label_User_name.place(x = 200, y = 280)

Username = tk.Entry(Admin, width = 35)
Username.place(x = 300, y = 280, width = 200)

Label_Password = tk.Label(Admin, text ="Password ", )
Label_Password.place(x = 200, y = 350)

Password= tk.Entry(Admin, width = 35)
Password.place(x = 300, y = 350, width = 200)
# Password.config(show="*")


submitbtn = tk.Button(Admin, text ="Login",
                      bg ='blue', command=submitact)
submitbtn.place(x = 350, y = 420, width = 55)

Label4 = tk.Label(Admin, text ="If you are new client", )
Label4.place(x = 270, y = 500)

submitbtn1 = tk.Button(Admin, text ="Register Here",
                      bg ='silver', command=Register)
submitbtn1.place(x = 400, y = 500, width = 100)

Admin.mainloop()



