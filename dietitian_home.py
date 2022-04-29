# import tkinter related libraries
import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *

# Import helper functions
from createMacronutrients import *
from createSupplements import *
from feedbackDietitian import * # import all functions from feedback file: for creating a client feedback

import argparse

# pass current user information
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
args = parser.parse_args()
user = args.input
local_DB_password = args.pw  



# Get single client information and call subroutines for macronutrients, supplements
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

    
    # Create Button Create Diet Plan
    createDietPlanButton = tk.Button(clientPlans, text ="Create Diet Plan",
                        bg ='blue', command=lambda:createDietPlan(clientPlans, connection, client_id)) 
    createDietPlanButton.place(x = 150, y = 220, width = 200)


    # Create Button Create Supplements
    createSuppButton = tk.Button(clientPlans, text ="Create Supplement Plan",
                        bg ='blue', command=lambda:createSupplements(clientPlans, connection, client_id)) 
    createSuppButton.place(x = 150, y = 520, width = 200)

    # Create Button Feeback to Client
    createFeedbackButton = tk.Button(clientPlans, text ="Feedback to Client",
                        bg ='blue', command=lambda:showFeedback(clientPlans,connection, client_id)) 
    createFeedbackButton.place(x = 850, y = 200, width = 200)
    

    clientPlans.mainloop()




# -------------------
# Dietitian home page

dietitian = tk.Tk()
dietitian.title("Dietitian")
dietitian.geometry("1300x900") 
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
where client_id in(select clientID from advises where advID = " +  "'" + str(userID) + "'" +" )" 


connection.execute(query)

myresult = connection.fetchall()

    
# Create title within page
Label_Client = tk.Label(dietitian, text ="Client List" )
Label_Client.config(font=("Courier", 15))
Label_Client.place(x = 10, y = 20)


i = 0
for client in myresult: 

    #Create underlying buttons for the name of clients
    createClientButtonN = tk.Button(dietitian, text =" Get Client ",
                        bg ='white', borderwidth = 0, command=lambda i=i:getSingleClient(i))
    y1 = 50
    y2 = y1+i*20

    createClientButtonN.place(x = 1150, y = y2, width = 80) 

    
    for j in range(len(client)):
        e = Entry(dietitian,width=20, fg='blue')
        e.grid(row=i, column=j) 
        e.insert(END, client[j])
        x1 = 10+j*120
        y1 = 50 +i*20
        e.place(x = x1 , y = y1)      
    
    i=i+1


dietitian.mainloop()