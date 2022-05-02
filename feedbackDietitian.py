# SJSU CMPE 138 Spring 2022 TEAM5

import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import *
import logging

# Create log file
log_file = 'dietitianLog.txt'
log_fh = logging.FileHandler(log_file)

log_format = '%(asctime)s %(levelname)s: %(message)s'
# Possible levels: DEBUG, INFO, WARNING, ERROR, CRITICAL    
log_level = 'INFO' 
logging.basicConfig(format=log_format, level=log_level, 
    handlers=[log_fh])



def saveFeedback(connection, client_id, feedbackEntry):

    feedback = feedbackEntry.get()

    # Check for complete user input
    if(feedback==""):
        msgbox.showinfo("Insert status","all fields are required")
    else:

        try:        
            query = "select client_feedback from client where client_id = " +  "'" + str(client_id) + "'" 
            logging.info(query) # save operation in log file
            connection.execute(query)
            logging.info("Query was successful!")

        except mysql.connector.Error as err:
            logging.error(err)
            logging.error("Query not successful!")

        
        result = connection.fetchall()


        try:        
            query = "update client set client_feedback =  " + "'"+str(feedback) +"'" +   " where client_id = " +  "'" + str(client_id) + "'" 
            logging.info(query) # save operation in log file
            connection.execute(query)
            logging.info("Query was successful!")

        except mysql.connector.Error as err:
            logging.error(err)
            logging.error("Query not successful!")

        

def createFeedback(connection, clientPlans,client_id, feedbackEntry):

    # Create Button to log diet plan values with pressing OK
    createOKButton = tk.Button(clientPlans, text ="Ok",
                        bg ='grey', command=lambda:saveFeedback(connection, client_id, feedbackEntry)) # pass result to check for empty
    createOKButton.place(x = 850, y = 290, width = 50)

   

def showFeedback(clientPlans,connection, client_id):

    try:        
        query = "select client_feedback from client where client_id = " +  "'" + str(client_id) + "'" 
        logging.info(query) # save operation in log file
        connection.execute(query)
        logging.info("Query was successful!")

    except mysql.connector.Error as err:
        logging.error(err)
        logging.error("Query not successful!")


    myFeedback = connection.fetchall()

    insert = myFeedback[0][0]

    feedbackEntry = tk.Entry(clientPlans, width = 50) # entry is a text box
    feedbackEntry.insert(END,insert)
    feedbackEntry.place(x = 850, y = 260, width = 400)


    createFeedback(connection, clientPlans,client_id, feedbackEntry)
