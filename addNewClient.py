import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
import argparse

# pass current user information
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
args = parser.parse_args()
user = args.input
local_DB_password = args.pw


def assign(connection):

    clientIDEntry = tk.Entry(addClient, width = 50) # entry is a text box
    clientIDEntry.place(x = 850, y = 260, width = 200)

    # Create Button to log diet plan values with pressing OK
    createOKButton = tk.Button(addClient, text ="Ok",
                       bg ='grey', command=lambda:input(addClient , connection, clientIDEntry)) # pass result to check for empty
    createOKButton.place(x = 850, y = 290, width = 50)



def input(addClient,connection, clientIDEntry):
    print("yes")
    client_id = clientIDEntry.get()

    my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password , database="fitnessstudio" )
    connection = my_connect.cursor()

    # Check if client has premium membership and return all current advisors
    query = "select clientID, advID, jobType \
    from advises join advisor \
    on advisor.ID = advID \
    where clientID = "+  "'" + str(client_id) + "'" +" and clientID in(select mem_client_id from  membership where mem_level = 'Premium')"

    print (query)
    connection.execute(query)

    print("pos exe")

    result = connection.fetchall()

    for x in result:
        print(x)
        

    # Check if all job types are different and max of 3 advisors
    for i in range(0,(len(result)-1)):
        if (len(result) <= 3 and result[i][2] != result[i+1][2] ):
            
            # A new advisor can only be assigned if not already 3 advisors are assigned to one client
            query = "insert into advises values ("+ "'" + str(client_id) + "'"+", "+"'" + str(userID) + "'"+")"
        else:
            print("Requirements not satisfied! ")



# Add client home page
addClient = tk.Tk()
addClient.title("Add Client to Advisor")
addClient.geometry("1300x900") 
my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password , database="fitnessstudio" )
connection = my_connect.cursor()

# Fetch current advisor information (ID):
query = "select ID from advisor where email = " +  "'" + str(user) + "'"  +""
connection.execute(query)
userID = connection.fetchall()
userID = userID[0][0]


# Create Button Show My Clients
showClients = tk.Button(addClient, text ="Add Client",
                      bg ='blue', command=lambda:assign(connection))
showClients.place(x = 150, y = 140, width = 200)


# Run main loop
addClient.mainloop()


