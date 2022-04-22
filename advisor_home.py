import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call


# Buttons and inputs created for supplements
def createSupplements(dietitian):

    Label_User_name = tk.Label(dietitian, text ="VitaminD3 ", )
    Label_User_name.place(x = 450, y = 260)

    Username = tk.Entry(dietitian, width = 35) # entry is a text box
    Username.place(x = 550, y = 260, width = 200)


    Label_User_name = tk.Label(dietitian, text ="Vitamin C ", )
    Label_User_name.place(x = 450, y = 285)

    Username = tk.Entry(dietitian, width = 35) # entry is a text box
    Username.place(x = 550, y = 285, width = 200)


    Label_User_name = tk.Label(dietitian, text ="Magnesium", )
    Label_User_name.place(x = 450, y = 310)

    Username = tk.Entry(dietitian, width = 35) # entry is a text box
    Username.place(x = 550, y = 310, width = 200)


    Label_User_name = tk.Label(dietitian, text ="Omega 3", )
    Label_User_name.place(x = 450, y = 335)

    Username = tk.Entry(dietitian, width = 35) # entry is a text box
    Username.place(x = 550, y = 335, width = 200)


# Buttons and inputs created for diet plan
def createDietPlan(dietitian):

    Label_User_name = tk.Label(dietitian, text ="Protein ", )
    Label_User_name.place(x = 50, y = 260)

    Username = tk.Entry(dietitian, width = 35) # entry is a text box
    Username.place(x = 150, y = 260, width = 200)


    Label_User_name = tk.Label(dietitian, text ="Carbohydrates ", )
    Label_User_name.place(x = 50, y = 285)

    Username = tk.Entry(dietitian, width = 35) # entry is a text box
    Username.place(x = 150, y = 285, width = 200)


    Label_User_name = tk.Label(dietitian, text ="Fat ", )
    Label_User_name.place(x = 50, y = 310)

    Username = tk.Entry(dietitian, width = 35) # entry is a text box
    Username.place(x = 150, y = 310, width = 200)


# Get single client information
def getSingleClient(myresult,i):

    print("i: ", i)
    client_id = myresult[0][0]
    #fetch single client
    clientPlans = tk.Tk()
    clientPlans.title("Client Plans")
    clientPlans.geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user="root", passwd="password", database="fitnessstudio" )
    connection = my_connect.cursor()


  
    query = "select client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
    client_email, client_mobile from client where client_id = " +  "'" + str(client_id) + "'" + " and client_id in(select adv_clientID from advisor ) "

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
                        bg ='blue', command=lambda:createDietPlan(clientPlans)) 
    createDietPlanButton.place(x = 150, y = 220, width = 200)


    # Create Button Create Supplements
    createSuppButton = tk.Button(clientPlans, text ="Create Supplement Plan",
                        bg ='blue', command=lambda:createSupplements(clientPlans)) 
    createSuppButton.place(x = 550, y = 220, width = 200)

    clientPlans.mainloop()




# Get complete client list on dietitian home page
def client_list():

    dietitian = tk.Tk()
    dietitian.title("Dietitian")
    dietitian.geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user="root", passwd="password", database="fitnessstudio" )
    connection = my_connect.cursor()
    query = "select client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
        client_email, client_mobile from client where client_id in(select adv_clientID from advisor ) "

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
                          bg ='white', borderwidth = 0, command=lambda:getSingleClient(myresult,i))
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


# Instantiate advisor_home class
Advisor_home=tk.Tk()
Advisor_home.title("Advisor_Home_Page")
Advisor_home.geometry("900x900")


# Create Button Show My Clients
showClients = tk.Button(Advisor_home, text ="Show My Clients",
                      bg ='blue', command=client_list)
showClients.place(x = 150, y = 140, width = 200)

# Run main loop
Advisor_home.mainloop()

