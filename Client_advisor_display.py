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
args = parser.parse_args()
user = args.input
local_DB_password = args.pw
jobType=args.Job





def showFeedback():
    
    con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
    cursor=con.cursor()
    # cursor.execute("select client_feedback from client where client_email = " +  "'" + str(user) + "'"  )
    cursor.execute("select client_feedback from client where client_email ='name1.last@gmail.com'"  )
    results=cursor.fetchall()
    
    myFeedback = results[0][0]
    
    feedbackEntry = tk.Entry(AC, width = 50) # entry is a text box
    feedbackEntry.insert(END,myFeedback)
    feedbackEntry.place(x = 550, y = 550, width = 400)

def GetMacronutrients(client):
    try:    
       if(jobType=="Dietian"):

            B=tk.Tk()
            B.title("Dietplan")    
            
            con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
            cursor=con.cursor()
            cursor.execute("select client_feedback from client where client_email = " +  "'" + str(user) + "'"  )
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
            
            try:
            
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

            except:  
                msgbox.showinfo("Error Status","You dont have dietplan/You have not subscribed to Dietitian ")  
            B.mainloop()
    except:
                msgbox.showinfo("Error Status","You dont have dietplan/You have not subscribed to Dietitian ")
  
  

AC=tk.Tk()
AC.title("Advisor_prescription")
AC.geometry("900x900")

con=mysql.connect(host="localhost",user="root",password = local_DB_password,db="fitnessstudio") 
cursor=con.cursor()
# cursor.execute("select client_feedback from client where client_email = " +  "'" + str(user) + "'"  )
cursor.execute("select client_id from client where client_email ='name2.last@gmail.com'"  )
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
                      bg ='silver', command=lambda:GetMacronutrients(client))
submitbtn3.place(x = 100, y = 200, width = 200)

submitbtn4 = tk.Button(AC, text ="Get Doctor Prescription",
                      bg ='silver', command=lambda:GetMacronutrients(client))
submitbtn4.place(x = 100, y = 300, width = 200)

AC.mainloop()

