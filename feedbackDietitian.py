import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import *


def saveFeedback(connection, dietitian , client_id, feedbackEntry):

    feedback = feedbackEntry.get()

    # Check for complete user input
    if(feedback==""):
        msgbox.showinfo("Insert status","all fields are required")
    else:
        query = "select client_feedback from client where client_id = " +  "'" + str(client_id) + "'" 
        connection.execute(query)
        result = connection.fetchall()

        query = "update client set client_feedback =  " + "'"+str(feedback) +"'" +   " where client_id = " +  "'" + str(client_id) + "'" 
        connection.execute(query)

        


def createFeedback(clientPlans,client_id, feedbackEntry):

    # Create Button to log diet plan values with pressing OK
    createOKButton = tk.Button(clientPlans, text ="Ok",
                        bg ='grey', command=lambda:saveFeedback(connection, dietitian , client_id, feedbackEntry)) # pass result to check for empty
    createOKButton.place(x = 850, y = 290, width = 50)

   




def showFeedback(clientPlans,connection, client_id):


    query = "select client_feedback from client where client_id = " +  "'" + str(client_id) + "'" 
    connection.execute(query)

    myFeedback = connection.fetchall()

    # If feedback is not empty show it
   # if myFeedback is "None":
   #     insert = " hi "
   # elif myFeedback == []:
    #    insert = " hi "
    #else:

    insert = myFeedback[0][0]

    feedbackEntry = tk.Entry(clientPlans, width = 50) # entry is a text box
    feedbackEntry.insert(END,insert)
    feedbackEntry.place(x = 850, y = 260, width = 400)


    createFeedback(clientPlans,client_id, feedbackEntry)