# SJSU CMPE 138 Spring 2022 TEAM5
import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox

from tkinter import *
from subprocess import call
from PIL import *
import argparse
import logging

# Create log file
log_file = 'clientLog.txt'
log_fh = logging.FileHandler(log_file)

log_format = '%(asctime)s %(levelname)s: %(message)s'
# Possible levels: DEBUG, INFO, WARNING, ERROR, CRITICAL    
log_level = 'INFO' 
logging.basicConfig(format=log_format, level=log_level,handlers=[log_fh])


#pass current user informations
 
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
parser.add_argument("--alias", help = "python alias")
args = parser.parse_args()
user = args.input
#user="name1.last@gmail.com"
python_alias=args.alias
#python_alias='python'
local_DB_password = args.pw
#local_DB_password = "um41Tact$"



def train_sessions(kind):
    Rec_tra_sessions = tk.Tk()
    Rec_tra_sessions .title(kind+" Training Sessions")
    Rec_tra_sessions .geometry("1300x900") 
    
    my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password, database="fitnessstudio" )
    connection = my_connect.cursor()
    try:
        #displays training sessions
        query = ("select session_instructor_name,session_invididual_group,session_id,\
        session_zoom_link from training_session where session_type=" + "'" + str(kind) +"'" )
        logging.info(query) # save operation in log file
        connection.execute(query)
        myresult = connection.fetchall()
        logging.info("Query was successful!")  
        
    except mysql.Error as err:
        logging.error(err)
        logging.error("Query not successful!")

    #print(myresult)
    # Create title within page
    Label_Client = tk.Label(Rec_tra_sessions, text =kind+" Training Sessions" )
    Label_Client.config(font=("Courier", 15))
    Label_Client.place(x = 10, y = 20)
    i = 0
    for value in myresult: 
        
        #Create underlying buttons for the name of clients
        #createClientButtonN = tk.Button(Admin2, text =" Get Client ",
        #bg ='white', borderwidth = 0, command=lambda:getSingleClient(myresult,client))
        y1 = 50
        y2 = y1+i*20
    
        # createClientButtonN.place(x = 1150, y = y2, width = 80) 
    
        for j in range(len(value)):
            e = Entry(Rec_tra_sessions,width=40, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, value[j])
            x1 = 10+j*120
            y1 = 50 +i*20
            e.place(x = x1 , y = y1) 
            
        i=i+1
    Rec_tra_sessions.mainloop()
    
def training_sessions1():
    Client.destroy()
    #call([python_alias,"test.py","--input", user, "--pw", local_DB_password,"--Job",a])
    call([python_alias,"training_session.py","--input", user, "--pw",local_DB_password, "--alias", python_alias])
    #print("training")

def fitness_seminars(kind):
    Rec_fitness_seminars = tk.Tk()
    Rec_fitness_seminars .title(kind+" Fitness Seminars")
    Rec_fitness_seminars .geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password, database="fitnessstudio" )
    connection = my_connect.cursor()
    try:
        #displays fitness seminars
        query = "select FS_sem_id,FS_Inst_ID, FS_zoomlink\
        from Fitness_seminar where FS_type =" + "'" + str(kind) +"'" 
        logging.info(query) # save operation in log file
        connection.execute(query)
        myresult = connection.fetchall()
        logging.info("Query was successful!")
        
    except mysql.Error as err:
        logging.error(err)
        logging.error("Query not successful!")
    
    #print(myresult)
    # Create title within page
    Label_Client = tk.Label(Rec_fitness_seminars, text =kind+" Fitness Seminars" )
    Label_Client.config(font=("Courier", 15))
    Label_Client.place(x = 10, y = 20)
    i = 0
    for value in myresult: 
        
        #Create underlying buttons for the name of clients
        #createClientButtonN = tk.Button(Admin2, text =" Get Client ",
        #bg ='white', borderwidth = 0, command=lambda:getSingleClient(myresult,client))
        y1 = 50
        y2 = y1+i*20
    
        # createClientButtonN.place(x = 1150, y = y2, width = 80) 
    
        for j in range(len(value)):
            e = Entry(Rec_fitness_seminars,width=40, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, value[j])
            x1 = 10+j*120
            y1 = 50 +i*20
            e.place(x = x1 , y = y1) 
            
        i=i+1
    Rec_fitness_seminars.mainloop()
    
def Advisor_Request():
    #comment the next statement when uploading
    #user="name1.last@gmail.com"
    con=mysql.connect(host="localhost",user="root",password=local_DB_password, db="fitnessstudio") 
    cursor=con.cursor()
    try:
        #retreive client id for the corressponding client email
        query="select client_id from client where client_email = %s"
        logging.info(query) # save operation in log file
        cursor.execute(query, [(user)])
        results = cursor.fetchall()
        logging.info("Query was successful!")
        
    except mysql.Error as err:
        logging.error(err)
        logging.error("Query not successful!")
        
    #print(results)
    l=len(results)
    S = str(results[l-1]) 
    e = int(S[2:8]) 
    #print(e)
    a=Adv_type.get()
    #print(a)
    con=mysql.connect(host="localhost",user="root",password=local_DB_password, db="fitnessstudio") 
    cursor=con.cursor()
    try:
        #selecting advisor for a particular jobtype
        query="select max(id) from advisor where jobType = %s"
        logging.info(query)
        cursor.execute(query, [(a)])
        results1 = cursor.fetchall()
        logging.info("Query was successful!")
        
    except mysql.Error as err:
        logging.error(err)
        logging.error("Query not successful!")
        
    #print(results1)
    l=len(results1)
    S = str(results1[l-1]) 
    f = int(S[2:8]) 
    #print(f)
    con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio") 
    cursor=con.cursor()
    try:
        #inerting into advises table
        query="insert into advises (clientID,advID) values(%s,%s)"
        logging.info(query)
        cursor.execute(query,[(e),(f)])
        con.commit()
        logging.info("Query was successful!")
        msgbox.showinfo("Login status","ADVISOR REQUESTED SUCCESSFULLY")
        
    except mysql.Error as err:
        logging.error(err)
        logging.error("Query not successful!")
        
        
    #cursor.execute("insert into advises (clientID,advID) values(%s,%s)",
    #              [(e),(f)])
    #con.commit()
    #msgbox.showinfo("Login status","ADVISOR REQUESTED SUCCESSFULLY")
    #Client.destroy()
    #call([python_alias,"test.py","--input", user, "--pw", local_DB_password,"--Job",a])
    #call([python_alias,"Client_advisor_display.py","--input", user, "--pw",local_DB_password, "--alias", python_alias])
    
def Advisor_access():
    a=Adv_type.get()
    #print(a)
    Client.destroy()
    call([python_alias,"Client_advisor_display.py","--input", user, "--pw",local_DB_password,"--alias", python_alias,"--Job",a,])
   
    
    
def premium():
    Client.destroy()
    #call the buy premium page
    call([python_alias,"Premium.py","--input", user, "--pw",local_DB_password, "--alias", python_alias])
    return True


Client=tk.Tk()
Client.title("Client Home")
Client.geometry("800x600")
#print(user)

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

#Type="Premium"

if(Type=="Free"):
    
    Free_User = tk.Label(Client, text =Type+" USER:", font=('bold',30) )
    Free_User .place(x = 30, y = 20)
    
    Output_free = tk.Label(Client, text ="As a "+ Type+" user you have access to all these:", font=('bold',20) )
    Output_free.place(x = 30, y = 60)
    
    #access to recorded training sessions page
    kind='recorded'
    num1 = tk.Label(Client, text ="1.", font=('bold',20) )
    num1.place(x = 30, y = 90)
    #submitbtn1 = tk.Button(Client, text =kind+" Traning sessions",bg ='silver', command=lambda:train_sessions(kind='recorded'))
    submitbtn1 = tk.Button(Client, text =" Traning sessions",bg ='silver', command=training_sessions1)
    submitbtn1.place(x = 50, y = 90, width = 200)
    
    #access to recorded fitness seminars page
    kind='recorded'
    num2 = tk.Label(Client, text ="2.", font=('bold',20) )
    num2.place(x = 30, y = 120)
    submitbtn2 = tk.Button(Client, text =kind+" Fitness Seminars",bg ='silver', command=lambda:fitness_seminars(kind='recorded'))
    submitbtn2.place(x = 50, y = 120, width = 200)
    
    #more stuff
    Output_more_stuff = tk.Label(Client, text ="If you want to access more exciting features such as:", font=('bold',20) )
    Output_more_stuff.place(x = 30, y = 200)
    Output_more_stuff2 = tk.Label(Client, text ="*Live Training Sessions*\n*Live Fitness Seminars*\n*One-on-One Sessions*\n*dietary plan and much more*", font=('bold',20) )
    Output_more_stuff2.place(x = 30, y = 230)
    
    submitbtn3 = tk.Button(Client, text ="Buy Premium",font=('bold',30),bg ='silver', command=premium)
    submitbtn3.place(x = 50, y = 350, width = 200)
    
    
elif(Type=="Basic"):
    
    Free_User = tk.Label(Client, text =Type+" USER:", font=('bold',30) )
    Free_User .place(x = 30, y = 20)
    
    Output_free = tk.Label(Client, text ="As a "+ Type+" User you have access to all these:", font=('bold',20) )
    Output_free.place(x = 30, y = 60)
    
    #access to recorded training sessions page
    kind='recorded'
    num1 = tk.Label(Client, text ="1.", font=('bold',20) )
    num1.place(x = 30, y = 90)
    #submitbtn1 = tk.Button(Client, text =kind+" Traning sessions",bg ='silver', command=lambda:train_sessions(kind='recorded'))
    submitbtn1 = tk.Button(Client, text =" Traning sessions",bg ='silver', command=training_sessions1)
    submitbtn1.place(x = 50, y = 90, width = 200)
    
    #access to recorded fitness seminars page
    kind='recorded'
    num2 = tk.Label(Client, text ="2.", font=('bold',20) )
    num2.place(x = 30, y = 120)
    submitbtn2 = tk.Button(Client, text =kind+" Fitness Seminars",bg ='silver', command=lambda:fitness_seminars(kind='recorded'))
    submitbtn2.place(x = 50, y = 120, width = 200)
    
    #access to live training sessions page
    #kind='live'
    #num3 = tk.Label(Client, text ="3.", font=('bold',20) )
    #num3.place(x = 30, y = 150)
    #submitbtn3 = tk.Button(Client, text ="Enroll to "+kind+" Traning sessions",bg ='silver', command=lambda:train_sessions(kind='live'))
    #submitbtn3 = tk.Button(Client, text =kind+" Traning sessions",bg ='silver', command=training_sessions1)
    #submitbtn3.place(x = 50, y = 150, width = 200)
    
    #access to recorded fitness seminars page
    num4 = tk.Label(Client, text ="3.", font=('bold',20) )
    num4.place(x = 30, y = 150)
    submitbtn4 = tk.Button(Client, text ="Enroll to "+kind+"  Fitness Seminars",bg ='silver', command=lambda:fitness_seminars(kind='live'))
    submitbtn4.place(x = 50, y = 150, width = 200)
    
    #more stuff
    Output_more_stuff = tk.Label(Client, text ="If you want to access more exciting features such as:", font=('bold',20) )
    Output_more_stuff.place(x = 30, y = 250)
    Output_more_stuff2 = tk.Label(Client, text ="*One-on-One Sessions*\n*dietary plan and much more*", font=('bold',20) )
    Output_more_stuff2.place(x = 30, y = 280)
    
    submitbtn5 = tk.Button(Client, text ="Buy Premium",font=('bold',30),bg ='silver', command=premium)
    submitbtn5.place(x = 50, y = 400, width = 200)


elif(Type=="Premium"):
    Free_User = tk.Label(Client, text =Type+" USER:", font=('bold',30) )
    Free_User .place(x = 30, y = 20)
    
    Output_free = tk.Label(Client, text ="As a "+ Type+" User you have access to all these:", font=('bold',20) )
    Output_free.place(x = 30, y = 60)
    
    #access to recorded training sessions page
    kind='recorded'
    num1 = tk.Label(Client, text ="1.", font=('bold',20) )
    num1.place(x = 30, y = 90)
    #submitbtn1 = tk.Button(Client, text =kind+" Traning sessions",bg ='silver', command=lambda:train_sessions(kind='recorded'))
    submitbtn1 = tk.Button(Client, text =" Traning sessions",bg ='silver', command=training_sessions1)
    submitbtn1.place(x = 50, y = 90, width = 200)
    
    #access to recorded fitness seminars page
    num2 = tk.Label(Client, text ="2.", font=('bold',20) )
    num2.place(x = 30, y = 120)
    submitbtn2 = tk.Button(Client, text =kind+" Fitness Seminars",bg ='silver', command=lambda:fitness_seminars(kind='recorded'))
    submitbtn2.place(x = 50, y = 120, width = 200)
    
    #access to live training sessions page
    #kind='live'
    #num3 = tk.Label(Client, text ="3.", font=('bold',20) )
    #num3.place(x = 30, y = 150)
    #submitbtn3 = tk.Button(Client, text ="Enroll to "+kind+" Traning sessions",bg ='silver', command=lambda:train_sessions(kind='live'))
    #submitbtn3 = tk.Button(Client, text =kind+" Traning sessions",bg ='silver', command=training_sessions1)
    #submitbtn3.place(x = 50, y = 150, width = 200)
    
    #access to recorded fitness seminars page
    num4 = tk.Label(Client, text ="3.", font=('bold',20) )
    num4.place(x = 30, y = 150)
    submitbtn4 = tk.Button(Client, text ="Enroll to "+kind+"  Fitness Seminars",bg ='silver', command=lambda:fitness_seminars(kind='live'))
    submitbtn4.place(x = 50, y = 150, width = 200)
    
    Output_more_stuff = tk.Label(Client, text ="As a Premium user you can request for an Advisor:", font=('bold',20) )
    Output_more_stuff.place(x = 30, y = 250)
    Advisor_type = tk.Label(Client, text =" Advisor Type:", font=('bold',20) )
    Advisor_type.place(x = 30, y = 280)
    Adv_type = StringVar()
    Adv_type.set("Dietitian")
    drop = OptionMenu( Client, Adv_type, "Dietitian","Mental_Coach","Doctor",)
    drop.place(x = 170, y = 280, width = 200)
    regibutton1 = tk.Button(Client, text ="Request", font=('bold',30),
                          bg ='silver', command=Advisor_Request)
    regibutton1.place(x = 180, y = 310, width = 150, height = 50)
    regibutton2 = tk.Button(Client, text ="Access Advisor", font=('bold',30),
                          bg ='silver', command=Advisor_access)
    regibutton2.place(x = 180, y = 400, width = 250, height = 50)

Client.mainloop()
