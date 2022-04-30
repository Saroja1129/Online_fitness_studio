import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox

from tkinter import *
from subprocess import call
from PIL import *
import argparse

#pass current user information
 
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
args = parser.parse_args()
user = args.input
python_alias="python"
local_DB_password = args.pw
#local_DB_password = "um41Tact$"



def train_sessions(kind):
    Rec_tra_sessions = tk.Tk()
    Rec_tra_sessions .title(kind+" Training Sessions")
    Rec_tra_sessions .geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password, database="fitnessstudio" )
    connection = my_connect.cursor()
    query = "select session_instructor_name,session_invididual_group,session_id,\
    session_zoom_link from training_session where session_type=" + "'" + str(kind) +"'" 
                                                               
    connection.execute(query)

    myresult = connection.fetchall()
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

def fitness_seminars(kind):
    Rec_fitness_seminars = tk.Tk()
    Rec_fitness_seminars .title(kind+" Fitness Seminars")
    Rec_fitness_seminars .geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password, database="fitnessstudio" )
    connection = my_connect.cursor()
    query = "select FS_sem_id,FS_Inst_ID, FS_zoomlink\
    from Fitness_seminar where FS_type =" + "'" + str(kind) +"'" 

    connection.execute(query)

    myresult = connection.fetchall()
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
    cursor.execute("select client_id from client where client_email = %s", [(user)] )
    results=cursor.fetchall()
    #print(results)
    l=len(results)
    S = str(results[l-1]) 
    e = int(S[2:8]) 
    #print(e)
    a=Adv_type.get()
    con=mysql.connect(host="localhost",user="root",password=local_DB_password, db="fitnessstudio") 
    cursor=con.cursor()
    cursor.execute("select max(id) from advisor where jobType = %s", [(a)] )
    results1=cursor.fetchall()
    #print(results1)
    l=len(results1)
    S = str(results1[l-1]) 
    f = int(S[2:8]) 
    #print(f)
    con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio") 
    cursor=con.cursor()
    cursor.execute("insert into advises (clientID,advID) values(%s,%s)",
                   [(e),(f)])
    con.commit()
    msgbox.showinfo("Login status","lOGIN SUCCESSFULL")
    Client.destroy()
    #call(["python","Premium.py"])
    #call([python_alias,"test.py","--input", user, "--pw", local_DB_password,"--Job",a])
    call([python_alias,"Client_advisor_display.py","--input", user, "--pw", local_DB_password,"--Job",a])
    
def premium():
    Client.destroy()
    #call the buy premium page
    call(["python","Premium.py"])
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
print(l)
S = str(results[l-1]) 
b= S[2]
print(b)

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
    submitbtn1 = tk.Button(Client, text =kind+" Traning sessions",bg ='silver', command=lambda:train_sessions(kind='recorded'))
    submitbtn1.place(x = 50, y = 90, width = 200)
    
    #access to recorded fitness seminars page
    #kind='recorded'
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
    submitbtn1 = tk.Button(Client, text =kind+" Traning sessions",bg ='silver', command=lambda:train_sessions(kind='recorded'))
    submitbtn1.place(x = 50, y = 90, width = 200)
    
    #access to recorded fitness seminars page
    num2 = tk.Label(Client, text ="2.", font=('bold',20) )
    num2.place(x = 30, y = 120)
    submitbtn2 = tk.Button(Client, text =kind+" Fitness Seminars",bg ='silver', command=lambda:fitness_seminars(kind='recorded'))
    submitbtn2.place(x = 50, y = 120, width = 200)
    
    #access to live training sessions page
    kind='live'
    num3 = tk.Label(Client, text ="3.", font=('bold',20) )
    num3.place(x = 30, y = 150)
    submitbtn3 = tk.Button(Client, text ="Enroll to "+kind+" Traning sessions",bg ='silver', command=lambda:train_sessions(kind='live'))
    submitbtn3.place(x = 50, y = 150, width = 200)
    
    #access to recorded fitness seminars page
    num4 = tk.Label(Client, text ="4.", font=('bold',20) )
    num4.place(x = 30, y = 180)
    submitbtn4 = tk.Button(Client, text ="Enroll to "+kind+"  Fitness Seminars",bg ='silver', command=lambda:fitness_seminars(kind='live'))
    submitbtn4.place(x = 50, y = 180, width = 200)
    
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
    submitbtn1 = tk.Button(Client, text =kind+" Traning sessions",bg ='silver', command=lambda:train_sessions(kind='recorded'))
    submitbtn1.place(x = 50, y = 90, width = 200)
    
    #access to recorded fitness seminars page
    num2 = tk.Label(Client, text ="2.", font=('bold',20) )
    num2.place(x = 30, y = 120)
    submitbtn2 = tk.Button(Client, text =kind+" Fitness Seminars",bg ='silver', command=lambda:fitness_seminars(kind='recorded'))
    submitbtn2.place(x = 50, y = 120, width = 200)
    
    #access to live training sessions page
    kind='live'
    num3 = tk.Label(Client, text ="3.", font=('bold',20) )
    num3.place(x = 30, y = 150)
    submitbtn3 = tk.Button(Client, text ="Enroll to "+kind+" Traning sessions",bg ='silver', command=lambda:train_sessions(kind='live'))
    submitbtn3.place(x = 50, y = 150, width = 200)
    
    #access to recorded fitness seminars page
    num4 = tk.Label(Client, text ="4.", font=('bold',20) )
    num4.place(x = 30, y = 180)
    submitbtn4 = tk.Button(Client, text ="Enroll to "+kind+"  Fitness Seminars",bg ='silver', command=lambda:fitness_seminars(kind='live'))
    submitbtn4.place(x = 50, y = 180, width = 200)
    
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

Client.mainloop()
