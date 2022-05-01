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
parser.add_argument("--alias", help = "python alias")
args = parser.parse_args()
user = args.input
local_DB_password = args.pw
python_alias= args.alias
   


def Fetch_Training_session():
    Admin2 = tk.Tk()
    Admin2.title("Admin")
    Admin2.geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password, database="fitnessstudio" )
    connection = my_connect.cursor()
    query = "select * from training_session"

    connection.execute(query)

    myresult = connection.fetchall()
        
    # Create title within page
    Label_Client = tk.Label(Admin2, text ="Seminar List" )
    Label_Client.config(font=("Courier", 15))
    Label_Client.place(x = 10, y = 20)

  
    i = 0
    for client in myresult: 

        
        #Create underlying buttons for the name of clients
        # createClientButtonN = tk.Button(Admin2, text =" Get Client ",
        #                   bg ='white', borderwidth = 0, command=lambda:getSingleClient(myresult,client))
        y1 = 50
        y2 = y1+i*20

        # createClientButtonN.place(x = 1150, y = y2, width = 80) 

        for j in range(len(client)):
            e = Entry(Admin2,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
            x1 = 10+j*120
            y1 = 50 +i*20
            e.place(x = x1 , y = y1)      
     
        i=i+1


    Admin2.mainloop()


def create_training_session():
    call([python_alias,"Adding_training_session.py","--input", user, "--pw", local_DB_password, "--alias", python_alias]) 
    
def client_list():
    call([python_alias,"Admin_client_list.py","--input", user, "--pw", local_DB_password, "--alias", python_alias])   
    
  
def membership():
    call([python_alias,"mem_cost.py","--input", user, "--pw", local_DB_password, "--alias", python_alias])
    
def create_fitness_seminar():
    call([python_alias,"fitness_seminar.py","--input", user, "--pw", local_DB_password,"--alias", python_alias])    
    

    


Admin_home=tk.Tk()
Admin_home.title("Admin_Home_Page")
Admin_home.geometry("800x600")

my_connect = mysql.connect(host="localhost", user="root", passwd=local_DB_password, database="fitnessstudio" )
connection = my_connect.cursor()
query = "select admin_name from admin where admin_Email = " +  "'" + str(user) + "'"
connection.execute(query)
results=connection.fetchall()
a=results[0][0]



Label_IH = tk.Label(Admin_home, text ="Current Admin User-----")
Label_IH.config(font=("Courier", 12))
Label_IH.place(x = 10, y = 20)

Label_IH1 = tk.Label(Admin_home, text =a )
Label_IH1.config(font=("Courier", 12))
Label_IH1.place(x = 150, y = 20)

submitbtn = tk.Button(Admin_home, text ="Current Clients",
                      bg ='gray', command=client_list)
submitbtn.place(x = 150, y = 140, width = 300)

submitbtn = tk.Button(Admin_home, text ="schedule fitness seminar",
                      bg ='gray', command=create_fitness_seminar)
submitbtn.place(x = 150, y = 240, width = 300)

submitbtn = tk.Button(Admin_home, text ="Current Scheduled Training sessions",
                      bg ='gray', command=Fetch_Training_session)
submitbtn.place(x = 150, y = 340, width = 300)

submitbtn = tk.Button(Admin_home, text ="Create group training session",
                      bg ='gray', command=create_training_session)
submitbtn.place(x = 150, y = 440, width = 300)

submitbtn = tk.Button(Admin_home, text ="Change Membership cost",
                      bg ='gray', command=membership)
submitbtn.place(x = 150, y = 540, width = 300)


Admin_home.mainloop()
