import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox


from tkinter import *
from subprocess import call
from hashlib import pbkdf2_hmac # for hash function
from PIL import *

#Change here for your local DB password
local_DB_Password = "password"


def Register():
            Admin.destroy()
            #call client Registration page instead of admin
            call(["python","adminHome.py"])
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
        # Update user and password
        con=mysql.connect(host="localhost",user="root",password=local_DB_Password, db="fitnessstudio") 
        cursor=con.cursor()
        cursor.execute("select * from admin where admin_email = %s and admin_pwd=%s", [(user),(passw)] )
        results=cursor.fetchall()
        if results:
            msgbox.showinfo("Login status","lOGIN SUCCESSFULL")
            Admin.destroy()
            call(["python","adminHome.py"])
            return True
        else:
            msgbox.showinfo("Login status","lOGIN UNSUCCESSFULL")
            return False
        
    elif(a=='Client'):
            # Update user and password
        con=mysql.connect(host="localhost",user="root",password = local_DB_Password,db="fitnessstudio") 
        cursor=con.cursor()
        cursor.execute("select * from client where client_email = %s and client_pwd =%s", [(user),(passw)] )
        results=cursor.fetchall()
        if results:
            msgbox.showinfo("Login status","lOGIN SUCCESSFULL")
            Admin.destroy()
            #call client home_page instead of admin
            call(["python","adminHome.py"])
            return True
        else:
            msgbox.showinfo("Login status","lOGIN UNSUCCESSFULL")
            return False
    
    elif(a=='Advisor'):
            # Update user and password
        con=mysql.connect(host="localhost",user="root",password = local_DB_Password,db="fitnessstudio") 
        cursor=con.cursor()
        cursor.execute("select * from advisor where email = %s and password =%s", [(user),(passw)] )
        results=cursor.fetchall()
        if results:
            msgbox.showinfo("Login status","lOGIN SUCCESSFULL")
            Admin.destroy()
            #call client home_page instead of admin
            call(["python","adminHome.py"])
            return True
        else:
            msgbox.showinfo("Login status","lOGIN UNSUCCESSFULL")
            return False
    
    elif(a=='Instructor'):
             # Update user and password
         con=mysql.connect(host="localhost",user="root",password = local_DB_Password,db="fitnessstudio") 
         cursor=con.cursor()
         cursor.execute("select * from Instructor where email = %s and Password =%s", [(user),(passw)] )
         results=cursor.fetchall()
         if results:
             msgbox.showinfo("Login status","lOGIN SUCCESSFULL")
             Admin.destroy()
             
             call(["python","adminHome.py"]) # TODO call client home_page instead of admin
             return True
         else:
             msgbox.showinfo("Login status","lOGIN UNSUCCESSFULL")
             return False    
                
           
            
Admin=tk.Tk()
Admin.title("Fitness_Studio")
Admin.geometry("800x600")

Label_Domain = tk.Label(Admin, text ="Domain ", font=('bold',10) )
Label_Domain.place(x = 50, y = 20)

clicked=StringVar()
clicked.set("Admin")
drop = OptionMenu( Admin , clicked, "Admin","Instructor","Client","Advisor")
drop.place(x = 150, y = 20, width = 200)

# Domain = tk.Entry(Admin, width = 35)
# Domain.place(x = 150, y = 20, width = 200)

Label_User_name = tk.Label(Admin, text ="UserName ", )
Label_User_name.place(x = 50, y = 60)

Username = tk.Entry(Admin, width = 35)
Username.place(x = 150, y = 60, width = 200)

Label_Password = tk.Label(Admin, text ="Password ", )
Label_Password.place(x = 50, y = 100)

Password= tk.Entry(Admin, width = 35)
Password.place(x = 150, y = 100, width = 200)
Password.config(show="*")


submitbtn = tk.Button(Admin, text ="Login",
                      bg ='blue', command=submitact)
submitbtn.place(x = 200, y = 140, width = 55)

Label4 = tk.Label(Admin, text ="If you are new client", )
Label4.place(x = 150, y = 200)

submitbtn1 = tk.Button(Admin, text ="Register Here",
                      bg ='silver', command=Register)
submitbtn1.place(x = 280, y = 200, width = 100)

Admin.mainloop()

