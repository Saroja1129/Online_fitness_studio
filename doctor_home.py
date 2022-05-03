# SJSU CMPE 138 Spring 2022 TEAM5

import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call
import argparse
import logging

from feedbackDietitian import * 

# pass current user information
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
parser.add_argument("--alias", help = "python alias")
args = parser.parse_args()
user = args.input
local_DB_password = args.pw  
python_alias = args.alias




# Create log file
log_file = 'doctor_home.txt'
log_fh = logging.FileHandler(log_file)

log_format = '%(asctime)s %(levelname)s: %(message)s'
# Possible levels: DEBUG, INFO, WARNING, ERROR, CRITICAL    
log_level = 'INFO' 
logging.basicConfig(format=log_format, level=log_level, 
    handlers=[log_fh])


def viewPrescription(client_id):
    
    D = tk.Tk()
    D.geometry("350x250")
    
   
    con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
    cursor=con.cursor() 
    try:
        query="select test_name,test_id from Lab_test where clientID=" +  "'" + str(client_id) + "'" + "" 
        logging.info(query)    
        cursor.execute(query)
      
    except mysql.Error as err:
        logging.error(err)
        logging.error("Query not successful!")	
    
    results = cursor.fetchall()
        
    i=0 
    for client in results: 
        for j in range(len(client)):
            e = Entry(D, width=10, fg='blue') 
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
    i=i+1
    
    D.mainloop()
    

def GiveFeedback(client_id):
    
    con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
    cursor=con.cursor() 
    cursor.execute("select client_feedback from client= " +  "'" + str(client_id) + "'" + "")
    results = cursor.fetchall()
    
    feedbackEntry = tk.Entry(doctor, width = 50) # entry is a text box
    feedbackEntry.insert(END,results)
    feedbackEntry.place(x = 100, y = 100, width = 400)
   
    

def createPrescription(client_id):
   
    def submitact():
        con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
        cursor=con.cursor() 
        cursor.execute("select test_id from Lab_test")
        results = cursor.fetchall()
        a=len(results)
       # print(results[a-1])
        S = str(results[a-1]) 
        a= str(int(S[2:8])+1)
      
        b=Testname.get()
        c=userID
        d=client_id
        
        try:
            con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
            cursor=con.cursor()
            #print("insert into Lab_test values(%s,%s,%s,%s)",[a,b,c,d])
            cursor.execute("insert into Lab_test values(%s,%s,%s,%s)",[(a),(b),(c),(d)])
            con.commit()
            results=cursor.fetchall()
            msgbox.showinfo("Create status","Prescription added succesfully")
        except:
           # print("Error: unable to create")
            msgbox.showinfo("Create status","Prescription added unsuccesfull")
      
    B=tk.Tk()
    B.title("Prescription")
    B.geometry("800x600")

    Label1 = tk.Label(B, text ="Test Name")
    Label1.place(x = 50, y = 300)
    
    Testname = tk.Entry(B, width = 35)
    Testname.place(x = 200, y = 300, width = 200)
    
    submitbtn = tk.Button(B, text ="Submit", bg ='blue',command =submitact)
    submitbtn.place(x = 350, y = 500, width = 150)
    
    B.mainloop()

def getSingleClient(i):

    client_id = myresult[i][0]
    clientPlans = tk.Tk()
    clientPlans.title("Client Plans")
    clientPlans.geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password, database="fitnessstudio" )
    connection = my_connect.cursor()


    # Get single client for current advisor
    query = "select client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
    client_email, client_mobile \
    from client \
    where client_id = " +  "'" + str(client_id) + "'" + " and client_id in(select clientID from advises where advID = " +  "'" + str(userID) + "'" + ")"

    connection.execute(query)

    # Show client details
    i = 0
    for client in connection: 
        for j in range(len(client)):
            e = Entry(clientPlans,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
            x1 = 10+j*120
            y1 = 50 +i*20
            e.place(x = x1 , y = y1)
        
     
        i=i+1

    
  
    createDietPlanButton = tk.Button(clientPlans, text ="Create Prescription",
                        bg ='blue', command=lambda:createPrescription(client_id)) 
    createDietPlanButton.place(x = 150, y = 220, width = 200)

    createDietPlanButton = tk.Button(clientPlans, text ="View Prescription of Client",
                        bg ='blue', command=lambda:viewPrescription(client_id)) 
    createDietPlanButton.place(x = 450, y = 220, width = 200)

  
   # createFeedbackButton = tk.Button(clientPlans, text ="Feedback to Client",
    #                    bg ='blue', command=lambda:GiveFeedback(client_id)) 
    #createFeedbackButton.place(x = 850, y = 200, width = 200)
    
        # Create Button Feeback to Client
    createFeedbackButton = tk.Button(clientPlans, text ="Feedback to Client",
                        bg ='blue', command=lambda:showFeedback(clientPlans,connection, client_id)) 
    createFeedbackButton.place(x = 850, y = 200, width = 200)
    

    
    
    

    clientPlans.mainloop()




# -------------------
# doctor home page

doctor = tk.Tk()
doctor.title("doctor")
doctor.geometry("1300x900") 
my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password , database="fitnessstudio" )
connection = my_connect.cursor()

# Fetch current advisor information (ID):
query = "select ID from advisor where email = " +  "'" + str(user) + "'"  +""
connection.execute(query)
userID = connection.fetchall()
userID = userID[0][0]


# Get all clients from current advisor, check if clients fulfill the membership Premium
query = "select client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
client_email, client_mobile \
from client \
where client_id in(select clientID from advises where advID = " +  "'" + str(userID) + "'" + " and clientID in(select mem_client_id from membership where mem_level = 'Premium'))" 

connection.execute(query)

myresult = connection.fetchall()

    
# Create title within page
Label_Client = tk.Label(doctor, text ="Client List" )
Label_Client.config(font=("Courier", 15))
Label_Client.place(x = 10, y = 20)

i = 0

for client in myresult: 

    #Create underlying buttons for the name of clients
    createClientButtonN = tk.Button(doctor, text =" Get Client ",
                        bg ='white', borderwidth = 0, command=lambda i=i:getSingleClient(i))
    y1 = 50
    y2 = y1+i*20

    createClientButtonN.place(x = 1150, y = y2, width = 80) 

    
    for j in range(len(client)):
        
        e = Entry(doctor,width=20, fg='blue')
        e.grid(row=i, column=j) 
        e.insert(END, client[j])
        x1 = 10+j*120
        y1 = 50 +i*20
        e.place(x = x1 , y = y1)      
    
    i=i+1

doctor.mainloop()
