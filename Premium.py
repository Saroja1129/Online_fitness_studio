import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox

from tkinter import *
from subprocess import call
from PIL import *
import argparse

#pass current user informations
 
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
parser.add_argument("--alias", help = "python alias")
args = parser.parse_args()
user = args.input
#user="name3.last@gmail.com"
python_alias=args.alias
local_DB_password = args.pw
#local_DB_password = "um41Tact$"

def BuyBasic():
    #print("We are in Buy Basic")
    con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio") 
    cursor=con.cursor()
    cursor.execute("update membership set mem_level='Basic',mem_cost=350 where \
           mem_client_id in (select client_id from client where client_email='" + str(user) +"')") 
    con.commit()
    msgbox.showinfo("Login status","YOU HAVE BEEN SUCCESSFULLY UPGRADED TO BASIC")
    Premium.destroy()
    call([python_alias,"client_home.py","--input", user, "--pw", local_DB_password, "--alias", python_alias ])
    return True
    
def BuyPremium():
    #print("We are in Buy Premium")
    con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio") 
    cursor=con.cursor()
    cursor.execute("update membership set mem_level='Premium',mem_cost=500 where \
           mem_client_id in (select client_id from client where client_email='" + str(user) +"')") 
    con.commit()
    msgbox.showinfo("Login status","YOU HAVE BEEN UPGRADED SUCCESSFULLY TO PREMIUM")
    Premium.destroy()
    call([python_alias,"client_home.py","--input", user, "--pw", local_DB_password, "--alias", python_alias ])
    return True

Premium=tk.Tk()
Premium.title("Buy Subscription")
Premium.geometry("800x600")


con=mysql.connect(host="localhost",user="root",password=local_DB_password, db="fitnessstudio") 
cursor=con.cursor()
cursor.execute("select mem_level from membership join client on\
              mem_client_id=client_id where client_email =" + "'" + str(user) +"'")
results=cursor.fetchall()
l=len(results)
#print(l)
S = str(results[l-1]) 
b= S[2]
#print(b)
if(b=='F'):
    Type="Free"
elif(b=='B'):
    Type="Basic"
elif(b=='P'):
    Type="Premium"
    
#Type="Basic"

if(Type=="Free"):
    
    Basic = tk.Label(Premium, text ="BASIC", font=('bold',30) )
    Basic.place(x = 100, y = 20)
    Prem= tk.Label(Premium, text ="PREMIUM", font=('bold',30) )
    Prem.place(x = 500, y = 20)
    
    Label1= tk.Label(Premium, text ="1.Live Training Sessions",font=('bold',20) )
    Label1.place(x = 40, y = 60)
    Label2= tk.Label(Premium, text ="2.Live Fitness Seminars",font=('bold',20) )
    Label2.place(x = 40, y = 100)
    Label3= tk.Label(Premium, text ="1.One-on-One Sessions",font=('bold',20) )
    Label3.place(x = 450, y = 60)
    Label4= tk.Label(Premium, text ="2.Live Training Sessions",font=('bold',20) )
    Label4.place(x = 450, y = 100)
    Label5= tk.Label(Premium, text ="3.Feedback From advises",font=('bold',20) )
    Label5.place(x = 450, y = 140)
    
    Prembutton1 = tk.Button(Premium, text ="Buy Basic", font=('bold',30),
                          bg ='silver', command=BuyBasic)
    Prembutton1.place(x = 80, y = 200, width = 150, height = 50)
    
    Prembutton2 = tk.Button(Premium, text ="Buy Premium", font=('bold',30),
                          bg ='silver', command=BuyPremium)
    Prembutton2.place(x = 480, y = 200, width = 200, height = 50)
    
elif(Type=="Basic"):
    
    #Basic = tk.Label(Premium, text ="BASIC", font=('bold',30) )
    #Basic.place(x = 100, y = 20)
    Prem= tk.Label(Premium, text ="PREMIUM", font=('bold',30) )
    Prem.place(x = 300, y = 20)
    
    #Label1= tk.Label(Premium, text ="1.Live Training Sessions",font=('bold',20) )
    #Label1.place(x = 40, y = 60)
    #Label2= tk.Label(Premium, text ="2.Live Fitness Seminars",font=('bold',20) )
    #Label2.place(x = 40, y = 100)
    Label3= tk.Label(Premium, text ="1.One-on-One Sessions",font=('bold',20) )
    Label3.place(x = 250, y = 60)
    Label4= tk.Label(Premium, text ="2.Live Training Sessions",font=('bold',20) )
    Label4.place(x = 250, y = 100)
    Label5= tk.Label(Premium, text ="3.Feedback From advises",font=('bold',20) )
    Label5.place(x = 250, y = 140)
    
    #Prembutton1 = tk.Button(Premium, text ="Buy Basic", font=('bold',30),
    #                     bg ='silver', command=BuyBasic)
    #Prembutton1.place(x = 80, y = 200, width = 150, height = 50)
    #
    Prembutton2 = tk.Button(Premium, text ="Buy Premium", font=('bold',30),
                         bg ='silver', command=BuyPremium)
    Prembutton2.place(x = 250, y = 200, width = 200, height = 50)

Premium.mainloop()
