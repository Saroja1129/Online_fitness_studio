import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call

def client_list():
    
    Admin2 = tk.Tk()
    Admin2.title("Admin")
    Admin2.geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user="root", passwd="Arti@123", database="fitnessstudio" )
    connection = my_connect.cursor()
    query = "select client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
        client_email, client_mobile,mem_level from client join membership on client_id=mem_client_id"

    connection.execute(query)

    myresult = connection.fetchall()
        
    # Create title within page
    Label_Client = tk.Label(Admin2, text ="Client List" )
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

    
def create_fitness_seminar():
    call(["python","fitness_seminar.py"])    
    
def training_session():
    call(["python","Adding_training_session.py"])    

Admin_home=tk.Tk()
Admin_home.title("Admin_Home_Page")
Admin_home.geometry("800x600")



submitbtn = tk.Button(Admin_home, text ="client_list",
                      bg ='yellow', command=client_list)
submitbtn.place(x = 150, y = 140, width = 100)

submitbtn = tk.Button(Admin_home, text ="schedule fitness seminar",
                      bg ='yellow', command=create_fitness_seminar)
submitbtn.place(x = 150, y = 180, width = 150)

submitbtn = tk.Button(Admin_home, text ="schedule Training session",
                      bg ='yellow', command=training_session)
submitbtn.place(x = 150, y = 220, width = 150)

Admin_home.mainloop()
