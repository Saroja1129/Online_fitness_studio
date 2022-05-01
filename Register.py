import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox

from hashlib import pbkdf2_hmac
from tkinter import *
from subprocess import call
from PIL import *
import argparse

#pass current user informations
#add your local DB password here
parser = argparse.ArgumentParser()
#parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
parser.add_argument("--alias", help = "python alias")
args = parser.parse_args()
#user = args.input
#user="name1.last@gmail.com"

python_alias=args.alias
local_DB_password = args.pw
#local_DB_password = "um41Tact$"



def hashPassword(passw):

    iter = 500_000 

    #Convert password (string) into byte
    passw_b = str.encode(passw)
    hash = pbkdf2_hmac('sha256', passw_b, b'salt'*2, iter)

    return str(hash.hex())

def Registeration():
    user = Name.get()
    email = Email.get()
    password= pwd.get()
    password1= password
    password=hashPassword(password)  
    rpassword= repwd.get()
    mobile = mob.get()
    age = Age.get()
    sex = Sex.get()
    weight = Weight.get()
    height = Height.get()
    bmi=int(weight)/int(height)*int(height)
    adminid = "A23795"
 
    
    if(user=="" or email=="" or password=="" or rpassword=="" or mobile=="" or
       age=="" or sex=="" or weight=="" or height==""):
        msgbox.showinfo("Insert status","all fields are required")
    elif(password1 != rpassword):
        msgbox.showinfo("Insert status","Passwords Dont match")
        
    else:
        my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password, database="fitnessstudio" )
        connection = my_connect.cursor()
        query ="select max(client_id) from client"
        connection.execute(query)
        results = connection.fetchall()
        
        #print(results)
        l=len(results)
        S = str(results[l-1]) 
        e = int(S[2:8])+1 #session_id
        #print(e)
        con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio") 
        cursor=con.cursor()
        cursor.execute("insert into client (client_admin_id,client_id,client_bmi,\
                       client_email,client_pwd,client_name,client_mobile,\
                           client_weight,client_height,client_age,client_gender) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                       [(adminid),(e),(bmi),(email),(password),(user),(mobile),(weight),(height),(age),(sex)])
        con.commit()
        membership_level="Free"
        membership_cost=0
        con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio") 
        cursor=con.cursor()
        cursor.execute("insert into membership (mem_client_id,mem_level,mem_cost,mem_admin_id) values(%s,%s,%s,%s)",[(e),(membership_level),(membership_cost),(adminid)])
        con.commit()
        #cursor.execute("select * from admin where admin_email = %s and admin_pwd=%s", [(user),(passw)] )
        results=cursor.fetchall()
        msgbox.showinfo("Insert status","Registeration Successful")
        
        Regi.destroy()
        call([python_alias,"admin_login.py",email,membership_level])
        return True
        
   



Regi=tk.Tk()
Regi.title("Client Registeration")
Regi.geometry("800x600")

Label_Name = tk.Label(Regi, text ="Name :", font=('bold',20) )
Label_Name.place(x = 50, y = 20)
Name = tk.Entry(Regi, width = 35)
Name.place(x = 120, y = 20, width = 200)

Label_Email = tk.Label(Regi, text ="Email :", font=('bold',20) )
Label_Email.place(x = 50, y = 60)
Email = tk.Entry(Regi, width = 35)
Email.place(x = 120, y = 60, width = 200)

Label_pwd = tk.Label(Regi, text ="Password :", font=('bold',20) )
Label_pwd.place(x = 400, y = 20)
pwd = tk.Entry(Regi, width = 35)
pwd.place(x = 520, y = 20, width = 200)
pwd.config(show="*")

Label_repwd = tk.Label(Regi, text ="Reenter Password :", font=('bold',20) )
Label_repwd.place(x = 325, y = 60)
repwd = tk.Entry(Regi, width = 35)
repwd.place(x = 520, y = 60, width = 200)
repwd.config(show="*")

Label_mob = tk.Label(Regi, text ="Mobile :", font=('bold',20) )
Label_mob.place(x = 50, y = 100)
mob = tk.Entry(Regi, width = 35)
mob.place(x = 120, y = 100, width = 200)

#Body Metrics
Label_Metrics= tk.Label(Regi, text ="Body Metrics", font=('bold',30))
Label_Metrics.place(x = 480, y = 120)

Label_Age = tk.Label(Regi, text ="Age:", font=('bold',20) )
Label_Age.place(x = 400, y = 170)
Age = tk.Entry(Regi, width = 35)
Age.place(x = 470, y = 170, width = 200)

Sex = StringVar()
Sex.set("Male")
drop = OptionMenu( Regi, Sex, "Male","Female","Others",)
drop.place(x = 470, y = 210, width = 200)

Label_Sex = tk.Label(Regi, text ="Sex :", font=('bold',20) )
Label_Sex.place(x = 400, y = 210)


Label_Weight = tk.Label(Regi, text ="Weight(lbs) :", font=('bold',20) )
Label_Weight.place(x = 350, y = 250)
Weight = tk.Entry(Regi, width = 35)
Weight.place(x = 470, y = 250, width = 200)

Label_Height = tk.Label(Regi, text ="Height(inches) :", font=('bold',20) )
Label_Height.place(x = 320, y = 290)
Height = tk.Entry(Regi, width = 35)
Height.place(x = 470, y = 290, width = 200)

#Register Button
regibutton1 = tk.Button(Regi, text ="Register", font=('bold',30),
                      bg ='silver', command=Registeration)
regibutton1.place(x = 370, y = 500, width = 150, height = 50)






Regi.mainloop()
