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
parser.add_argument("--Job", help="Job Type of Advisor")
parser.add_argument("--alias", help = "python alias")
args = parser.parse_args()
user = args.input
local_DB_password = args.pw
jobType=args.Job
python_alias=args.alias



def GetComment(client):
    
    if(jobType=="Mental_Coach"):
        C=tk.Tk()
        C.title("Prescription")   
        print(client) 
        
        con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
        cursor=con.cursor()
        Label_1 = tk.Label(C, text ="Comment" )
        Label_1.grid(row = 1, column = 0)
        query="select m_c_comment from mental_coaching_plan where clientID = " +  "'" + str(client) + "'"
        cursor.execute(query)
        result2=cursor.fetchall()
        
        print(result2)
        
        i=2
        for client in result2: 
            for j in range(len(client)):
                e = Entry(C, width=10, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, client[j])
        i=i+1

        C.mainloop()
        
    

def GetPrescription(client):
    
    if(jobType=="Doctor"):
        A=tk.Tk()
        A.title("Prescription")    
        
        con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
        cursor=con.cursor()
        # cursor.execute("select client_feedback from client where client_email = " +  "'" + str(user) + "'"  )
        # cursor.execute("select client_id from client where client_email ='name1.last@gmail.com'"  )
        # results=cursor.fetchall()
        # client = results[0][0]
        
        Label_1 = tk.Label(A, text ="Test name" )
        Label_1.grid(row = 1, column = 0)
        query="select test_name from lab_test where clientID = " +  "'" + str(client) + "'"
        cursor.execute(query)
        result1=cursor.fetchall()
        
        i=1
        for client in result1: 
            for j in range(len(client)):
                e = Entry(A, width=10, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, client[j])
        i=i+1

        
        A.mainloop()

    
def showFeedback():
    
    con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
    cursor=con.cursor()
    cursor.execute("select client_id from client where client_email = " +  "'" + str(user) + "'"  )
    # cursor.execute("select client_feedback from client where client_email ='name1.last@gmail.com'"  )
    results=cursor.fetchall()

    myFeedback = results[0][0]

    feedbackEntry = tk.Entry(AC, width = 50) # entry is a text box
    feedbackEntry.insert(END,myFeedback)
    feedbackEntry.place(x = 550, y = 550, width = 400)

def GetMacronutrients(client):  
    if(jobType=="Dietian"):

        B=tk.Tk()
        B.title("Dietplan")    
        
        con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
        cursor=con.cursor()
        # cursor.execute("select client_feedback from client where client_email = " +  "'" + str(user) + "'"  )
        # cursor.execute("select client_id from client where client_email ='name1.last@gmail.com'"  )
        # results=cursor.fetchall()
        # client = results[0][0]
        
        Label_1 = tk.Label(B, text ="Protein" )
        Label_2 = tk.Label(B, text ="carb" )
        Label_3 = tk.Label(B, text ="fat" )
        Label_4 = tk.Label(B, text ="vitaminD3" )
        Label_5 = tk.Label(B, text ="vitaminC" )
        Label_6 = tk.Label(B, text ="magnesium" )
        Label_7 = tk.Label(B, text ="omega3" )
        
        Label_1.grid(row = 1, column = 0)
        Label_2.grid(row = 1, column=  1)
        Label_3.grid(row = 1, column = 2)
        Label_4.grid(row = 1, column = 3)
        Label_5.grid(row = 1, column = 4)
        Label_6.grid(row = 1, column = 5)
        Label_7.grid(row = 1, column = 6)
        
    
        
        query="select protein,carbs,fat,vitaminD3,vitaminC,magnesium,omega3 \
                    from Dietary_Plan join plan_macronutrients on diet_plan_ID = diet_plan_ID_macro\
                    join plan_supplements on diet_plan_ID_macro=diet_plan_ID_suppl\
                    where clientID = " +  "'" + str(client) + "'"
        cursor.execute(query)
        result1=cursor.fetchall()
        
        i=2
        for client in result1: 
            for j in range(len(client)):
                e = Entry(B, width=10, fg='blue') 
                e.grid(row=i, column=j) 
                e.insert(END, client[j])
        i=i+1

        B.mainloop()


  

AC=tk.Tk()
AC.title("Advisor_prescription")
AC.geometry("900x900")

con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
cursor=con.cursor()
cursor.execute("select client_id from client where client_email =" +  "'" + str(user) + "'"  )
results=cursor.fetchall()
client = results[0][0]

print(client)
Label_IH = tk.Label(AC, text ="Feedback from Advisor" )
Label_IH.config(font=("Courier", 12))
Label_IH.place(x = 500, y = 500)

Feedback= tk.Entry(AC, width = 35)
Feedback.place(x = 550, y = 550, width = 200)

submitbtn1 = tk.Button(AC, text ="Show Feedback",
                      bg ='silver', command=showFeedback)
submitbtn1.place(x = 725, y = 500, width = 100)

submitbtn2 = tk.Button(AC, text ="Get Dietplan",
                      bg ='silver', command=lambda:GetMacronutrients(client))
submitbtn2.place(x = 100, y = 100, width = 200)

submitbtn3 = tk.Button(AC, text ="Get Mental_Coach_Plan",
                      bg ='silver', command=lambda:GetComment(client))
submitbtn3.place(x = 100, y = 200, width = 200)

submitbtn4 = tk.Button(AC, text ="Get Doctor Prescription",
                      bg ='silver', command=lambda:GetPrescription(client))
submitbtn4.place(x = 100, y = 300, width = 200)

AC.mainloop()

