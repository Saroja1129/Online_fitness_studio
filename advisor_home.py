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
args = parser.parse_args()
user = args.input
local_DB_password = args.pw

python_alias = "python3"


def addNewClient():

    Advisor_home.destroy()
    #call client home_page instead of admin
    call([python_alias,"addNewClient.py","--input", user, "--pw", local_DB_password])

    


# Get complete client list on dietitian home page
def dietClientList():

    Advisor_home.destroy()
    #call client home_page instead of admin
    call([python_alias,"dietitian_home.py","--input", user, "--pw", local_DB_password])



# Instantiate advisor_home class
Advisor_home=tk.Tk()
Advisor_home.title("Advisor_Home_Page")
Advisor_home.geometry("900x900")


# Create Button Show My Clients
showClients = tk.Button(Advisor_home, text ="Show My Clients",
                      bg ='blue', command=dietClientList)
showClients.place(x = 150, y = 140, width = 200)


# Create Button Add New Client
showClients = tk.Button(Advisor_home, text ="Add New Client",
                      bg ='blue', command=addNewClient)
showClients.place(x = 400, y = 140, width = 200)

# Run main loop
Advisor_home.mainloop()

