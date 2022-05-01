import tkinter as tk
from tkinter.font import BOLD
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call
import argparse

# pass current user information
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
args = parser.parse_args()
user = args.input
local_DB_password = args.pw
python_alias= "python"


     
def Client_Trainingsessions(client_id):
    # call([python_alias,"Adding_training_session.py","--input", user, "--pw", local_DB_password ])
    # # call(["python","Adding_training_session.py"]) 
    def getclient():
        con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
        cursor=con.cursor()
        movieList = []
        try:
          # cursor.execute("select distinct client_id from client")
          # results = cursor.fetchall()
          # for a in results:
          #  data =  (a[0])
          #  movieList.append(data)
            
          # selected2.set(movieList[0])
          # options=movieList 
          # dropdown = OptionMenu(Tran_ses, selected2 ,*options )
          # dropdown.place(x = 350, y = 540, width = 200) 
            query = "select ID from advisor where email = " +  "'" + str(user) + "'"  +""
            cursor.execute(query)
            userID = connection.fetchall()
            selected2 = userID[0][0]
        
        except:
         print("Error: unable to fecth data")  

    def getinstructor():
    
    # Update user and password 
      con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
      cursor=con.cursor()
      movieList = []
      try:
        query="select distinct trainer_id from instructor where oneflag = true"
        cursor.execute(query)
        results = cursor.fetchall()
        for a in results:
          data =  (a[0])
          movieList.append(data)
            
        selected1.set(movieList[0])
        options=movieList 
        dropdown = OptionMenu(Tran_ses, selected1 ,*options )
        dropdown.place(x = 350 ,y = 410, width = 200) 
        
      except:
        print("Error: unable to fecth data")
            

    def getadmin():
    
    # Update user and password 
      con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
      cursor=con.cursor()
      movieList = []
      try:
        query="select distinct admin_id from admin"
        cursor.execute(query)
        results = cursor.fetchall()
        for a in results:
           data =  (a[0])
           movieList.append(data)
            
        selected.set(movieList[0])
        options=movieList 
        dropdown = OptionMenu(Tran_ses, selected ,*options )
        dropdown.place(x = 350, y = 280, width = 200) 
        
      except:
         print("Error: unable to fecth data") 
         
    # def all():
    #      updatingtable()
    #      submitact()
         
    # def updatingtable(client_id):
            
    #         con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
    #         cursor=con.cursor() 
    #         cursor.execute("select session_id from training_session order by session_id")
    #         results = cursor.fetchall()
    #         l=len(results)
    #         S = str(results[l-1]) 
    #         d = int(S[2:8])+1 #session_id
    #         cursor.execute("insert into training_session_client values(%s,%s)",[d,client_id])
    #         con.commit()
      
         
    def submitact():
 
        con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
        cursor=con.cursor() 
        query="select session_id from training_session order by session_id"
        cursor.execute(query)
        results = cursor.fetchall()
        l=len(results)
        S = str(results[l-1]) 
        d = int(S[2:8])+1 #session_id
     
        
      
        
        a=clicked.get() #live/recorded
        b="individual"#group/individual
        c=zoomlink.get()
        e=selected.get() #admin_id
        f=selected1.get() #inst_id
        g=selected2.get()#client_id
    
        print(a)
        print(b)
        print(c)
        print(d)
        print(e)
        print(f)
        print(g)
    
        try:
            con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
            cursor=con.cursor()
            print("insert into training_session values(%s,%s,%s,%s,%s,%s,%s,%s)",[a,b,c,d,e,f])
            #cursor.execute("insert into fitness_seminar(FS_zoomlink,FS_sem_id,FS_type,FS_admin_id,FS_Inst_ID) values('a','a','a','A23675','A00001');,[(a),(b),(c),])
            cursor.execute("insert into training_session values(%s,%s,%s,%s,%s,%s)",[a,b,c,d,e,f])
            con.commit()
            results=cursor.fetchall()
            
            con1=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
            cursor1=con1.cursor()
            print("insert into training_session_client values(%s,%s)",[d,client_id])
            cursor1.execute("insert into training_session_client values(%s,%s)",[d,client_id])
            con1.commit()
            results1=cursor.fetchall()
            
          
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

    # Label_Name = tk.Label(Tran_ses, text ="Session Instructor Name", font=('bold',10) )
    # Label_Name.place(x = 200, y = 20)
    # Name = tk.Entry(Tran_ses, width = 35)
    # Name.place(x = 350, y = 20, width = 200)

    Label_ST = tk.Label(Tran_ses, text ="Session_Type :", font=('bold',10) )
    Label_ST.place(x = 200, y = 80)
    
    clicked=StringVar()
    clicked.set("live")
    drop = OptionMenu(Tran_ses, clicked, "live","recorded")
    drop.place(x = 350, y = 80, width = 200)

    # Label_ST = tk.Label(Tran_ses, text ="Session(Individual/group)", font=('bold',10) )
    # Label_ST.place(x = 200, y = 160)
    # clicked1=StringVar()
    # clicked1.set("Individual")
    
    # drop1 = OptionMenu( Tran_ses , clicked1, "Group","Individual")
    # drop1.place(x = 350, y = 160, width = 200)

    Label_zoom = tk.Label(Tran_ses, text ="Session Zoomlink", font=('bold',10) )
    Label_zoom.place(x = 200, y = 160)
    zoomlink = tk.Entry(Tran_ses, width = 35)
    zoomlink.place(x = 350, y = 160, width = 200)

    #can change if we use argparse
    Label_admin = tk.Label(Tran_ses, text ="Session admin", font=('bold',10) )
    Label_admin.place(x = 200, y = 240)
    adminid = tk.Button(Tran_ses, text ="Select Organiser", bg ='white',command =getadmin)
    adminid.place(x = 350, y = 240, width = 200)


    Label_inst = tk.Label(Tran_ses, text ="Session instructor", font=('bold',10) )
    Label_inst.place(x = 200, y = 360)
    inst = tk.Button(Tran_ses, text ="Get instructor ", bg ='white',command =getinstructor)
    inst.place(x = 350, y = 360, width = 200)

    # Label_client = tk.Label(Tran_ses, text ="client", font=('bold',10) )
    # Label_client.place(x = 200, y = 500)
    # client = tk.Button(Tran_ses, text ="Select client", bg ='white',command =getclient)
    # client.place(x = 350, y = 500, width = 200)

    submitbtn = tk.Button(Tran_ses, text ="CREATE_SEMINAR", bg ='blue',command =submitact)
    submitbtn.place(x = 350, y = 500, width = 150)

    Tran_ses.mainloop()
    
        
def getSingleClient(i):
    i=i-1
    client_id = myresult[i][0]
    Singleclient = tk.Tk()
    Singleclient.title("Client Plans")
    Singleclient.geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password, database="fitnessstudio" )
    connection = my_connect.cursor()


    # Get single client for current advisor
    query = "select client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
    client_email, client_mobile \
    from client \
    where client_id = " +  "'" + str(client_id) + "'" + ""

    connection.execute(query)
    
    createDietPlanButton = tk.Button(Singleclient, text ="Create Training session",bg ='blue', command=lambda:Client_Trainingsessions(client_id)) 
    createDietPlanButton.place(x = 150, y = 220, width = 200)

    # Show client details
    i = 1
    for client in connection: 
        for j in range(len(client)):
            e = Entry(Singleclient,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
            x1 = 10+j*120
            y1 = 50 +i*20
            e.place(x = x1 , y = y1)
        
     
        i=i+1

    
    # Create Button Create Diet Plan
    # createDietPlanButton = tk.Button(Singleclient, text ="Create Diet Plan",
    #                     bg ='blue', command=lambda:createDietPlan(Singleclient, connection, client_id)) 
    # createDietPlanButton.place(x = 150, y = 220, width = 200)

    Singleclient.mainloop()



        
Client = tk.Tk()
Client.title("Client")
Client.geometry("1300x900") 
my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password , database="fitnessstudio" )
connection = my_connect.cursor()

# Fetch current advisor information (ID):
# query = "select ID from advisor where email = " +  "'" + str(user) + "'"  +""
# connection.execute(query)
# userID = connection.fetchall()
# userID = userID[0][0]

client_id = StringVar()
# Get all clients from current advisor, check if clients fulfill the membership Premium
query = "select client_id, client_name , client_age, client_gender, client_height,client_email, \
          client_mobile,mem_level from client join membership on client_id=mem_client_id"
    
connection.execute(query)

myresult = connection.fetchall()


    
# Create title within page
Label_Client = tk.Label(Client, text ="Client List" )
Label_Client.config(font=("Courier", 15,BOLD))
Label_Client.place(x = 10, y = 10)

Label_1 = tk.Label(Client, text ="client_ID", font=("courier", 12))
Label_2 = tk.Label(Client, text ="Name", font=("courier", 12) )
Label_3 = tk.Label(Client, text ="Age" , font=("courier", 12))
Label_4 = tk.Label(Client, text ="Gender", font=("courier", 12) )
Label_5 = tk.Label(Client, text ="Height", font=("courier", 12))
Label_6 = tk.Label(Client, text ="Email" , font=("courier", 12))
Label_7 = tk.Label(Client, text ="Mobile" , font=("courier", 12))
Label_8 = tk.Label(Client, text ="Mem_level" , font=("courier", 12))

Label_1.place(x = 15, y = 40)
Label_2.place(x= 165, y = 40)
Label_3.place(x = 265, y = 40)
Label_4.place(x = 380, y = 40)
Label_5.place(x = 500,y = 40)
Label_6.place(x = 600, y = 40)
Label_7.place(x = 735, y = 40)
Label_8.place(x = 865, y = 40)

i = 1
for client in myresult: 

    #Create underlying buttons for the name of clients
    createClientButtonN = tk.Button(Client, text =" Get Client ",
                        bg ='white', borderwidth = 0, command=lambda i=i:getSingleClient(i))
    y1 = 50
    y2 = y1+i*20

    createClientButtonN.place(x = 1150, y = y2, width = 80) 

    
    for j in range(len(client)):
        e = Entry(Client,width=40, fg='blue')
        e.grid(row=i, column=j) 
        e.insert(END, client[j])
        x1 = 10+j*120
        y1 = 50 +i*20
        e.place(x = x1 , y = y1)      
    
    i=i+1


Client.mainloop()
