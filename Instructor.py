import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call
usr=
pwd=

# Get single client information
def singleClientWP(client_id):

    #fetch single client information
    clientWP = tk.Tk()
    clientWP.title("Client Overview")
    clientWP.geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    connection = my_connect.cursor()
    query = "select distinct client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
    client_email, client_mobile from client where client_id = " +  "'" + str(client_id) + "'"
    connection.execute(query)
    clientinfo = connection.fetchall()
    client_name= clientinfo[0][1]
    client_email = clientinfo[0][7]
    client_mobile = clientinfo[0][8]
    
    # Create title within page
    Label_Client = tk.Label(clientWP, text ="Client " + str(client_name) )
    Label_Client.config(font=("Courier", 12))
    Label_Client.place(x = 10, y = 20)
    
    # Show client details
    i = 0
    for client in clientinfo: 

        for j in range(2,6):

            e = Entry(clientWP,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
            x1 = 10+(j-2)*150
            y1 = 50 +i*20
            e.place(x = x1 , y = y1)
         
        i=i+1

    # Get workout information for that client
    query2 = "select Workout,Name,B.Plan_num,ID,C.client_name,B.Client_ID from Instructor as I join Personalized_workout_plan as \
     B on I.ID=B.Preparer_ID join client as C on C.client_id = B.Client_ID join Workouts on Workouts.Client_ID=B.Client_ID where B.Client_ID\
         = " + "'" +str(client_id) + "'"

    connection.execute(query2)
    workouts = connection.fetchall()
    inst_id =workouts[0][3]
    plan_num = workouts[0][2]
    i = 0

    #Show workout details
    for Workout in workouts:

        workoutbutton = tk.Button(clientWP, text =" Delete Workout ",
                          bg ='white', borderwidth = 0, command=lambda i=i :deleteworkout(client_id,workouts,i,clientWP))
        y1 = 100
        y2 = y1+i*30

        workoutbutton.place(x = 720, y = y2, width = 176)

        for j in range(1):
            e = Entry(clientWP,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, Workout[j])
            x1 = 10+j*120
            y1 = 100 +i*30
            e.place(x = x1 , y = y1)    
     
        i=i+1
    

    # Create Button Create Workout
    addWorkoutButton = tk.Button(clientWP, text ="Add Workout",
                        bg ='gray', command=lambda:addworkout(client_id,inst_id, plan_num ,clientWP))
    addWorkoutButton.place(x = 150, y = 250, width = 200)


    # Create Button Contact Client
    contactClientB = tk.Button(clientWP, text ="Contact Client",
                        bg ='gray', command=lambda:contactClient(client_name,client_email,client_mobile, clientWP)) 
    contactClientB.place(x = 550, y = 250, width = 200)

    clientWP.mainloop()



def contactClient(client_name, client_email, client_mobile, clientWP):

    # Pop out contaxt box with information
    contact = tk.Tk()
    contact.title("Contact Information")
    contact.geometry("480x360") 
    Label_Client = tk.Label(contact, text ="Contact Info for "+ str(client_name) )
    Label_Client.config(font=("Courier", 12))
    Label_Client.place(x = 10, y = 20)
    e = Entry(contact,width=24, fg='blue')
    e.insert(END, "Name: " + str(client_name))
    e.place(x = 60 , y = 60)
    e = Entry(contact,width=24, fg='blue')
    e.insert(END, "Email: " + str(client_email))
    e.place(x = 60 , y = 120)
    e = Entry(contact,width=24, fg='blue')
    e.insert(END, "Number: " + str(client_mobile))
    e.place(x = 60 , y = 180)


    contact.mainloop()




def deleteworkout(client_id, workouts, i, clientWP):

    #Connect to DB
    my_connect = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    
    #Delete query
    querydel = "delete from Workouts where Workouts.Client_ID\
         = " + "'" +str(client_id) + "'" + "and Workouts.Workout =" + "'"+ str(workouts[i][0]) +"'"
    
    connection = my_connect.cursor()
    connection.execute(querydel)
    my_connect.commit()
    my_connect.close
    print(connection)
    msgbox.showinfo(message="Workout deleted",parent=clientWP)

    # Refresh UI   
    clientWP.destroy()
    singleClientWP(client_id)


def addworkout(client_id,inst_id, plan_num ,clientWP):
  
    # Place text label for workout name
    workoutName = tk.Label(clientWP, text ="Workout Name: ", )
    workoutName.place(x = 50, y = 350)

    # Place input for workout name
    newWorkoutName = tk.Entry(clientWP, width = 360) # entry is a text box
    newWorkoutName.place(x = 250, y = 350, width = 360)

    #Place button to execute addition
    addWorkoutButtonN = tk.Button(clientWP, text =" Add ",
                          bg ='gray', borderwidth = 0, command=lambda :addtodb(clientWP, client_id,inst_id,plan_num,newWorkoutName.get()))
    
    addWorkoutButtonN.place(x = 250, y = 400, width = 100)
    

def addtodb(clientWP, client_id,inst_id,plan_num,inp):
    
    #Check that the input is not empty
    if (inp==""):
        msgbox.showerror(message="Please enter a workout name",title="Error",parent=clientWP)
        return
    
    #Connect to DB
    my_connect2 = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    connection2 = my_connect2.cursor()
    
    #Add workout
    queryadd = "Insert into Workouts values ('"+ str(client_id)+"',"+"'"+str(inst_id)+"',"+str(plan_num)+",'"+str(inp)+"');"
    print(queryadd)
    connection2.execute(queryadd)
    my_connect2.commit()
    my_connect2.close()
    msgbox.showinfo(title="Error",message="Workout Added",parent=clientWP)
    
    #Refresh UI
    clientWP.destroy()
    singleClientWP(client_id)


# Get complete client list on Instructor home page
def client_list():

    #Set up frame
    Instructor = tk.Tk()
    Instructor.title("Instructor")
    Instructor.geometry("1900x900") 

    # Create title within page
    Label_Client = tk.Label(Instructor, text ="Client List" )
    Label_Client.config(font=("Courier", 12))
    Label_Client.place(x = 10, y = 20)

    #Connect and query
    my_connect = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    connection = my_connect.cursor()
    query = "select distinct Name,ID,C.client_name,B.Client_ID, Plan_num from Instructor as I \
    join Personalized_workout_plan as B on I.ID=B.Preparer_ID join client as C on C.client_id = B.Client_ID;"
    connection.execute(query)
    myresult = connection.fetchall()

    i = 0
    #client_id = myresult[i][3]
    for client in myresult: 
        
        #Create underlying buttons for the name of clients
        createClientButtonN = tk.Button(Instructor, text =" Client ",
                          bg ='white', borderwidth = 0, command=lambda i=i :singleClientWP(myresult[i][3]))
        y1 = 50
        y2 = y1+i*30
        createClientButtonN.place(x = 1150, y = y2, width = 100) 

        for j in range(len(client)):
            e = Entry(Instructor,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
            x1 = 10+j*140
            y1 = 50 +i*30
            e.place(x = x1 , y = y1)      
     
        i=i+1
        
    Instructor.mainloop()



    
def sess_list():

    Sessions = tk.Tk()
    Sessions.title("Sessions")
    Sessions.geometry("1900x900") 
        
    # Create title within page
    Label_Sessions = tk.Label(Sessions, text ="Training Sessions" )
    Label_Sessions.config(font=("Courier", 12))
    Label_Sessions.place(x = 10, y = 20)

    # Connect and query
    my_connect = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )    
    query = "select * from training_session;"
    connectionSess = my_connect.cursor()
    connectionSess.execute(query)
    sessionsList = connectionSess.fetchall()
  
    i = 0
    for session in sessionsList: 
        
        #Create underlying buttons for the name of clients
        createSessionButtonN = tk.Button(Sessions, text =" Session Info ",
                          bg ='white', borderwidth = 0, command=lambda i=i :print(sessionsList[i]))
        y1 = 50
        y2 = y1+i*30

        createSessionButtonN.place(x = 1450, y = y2, width = 150) 

        for j in range(len(session)):
            e = Entry(Sessions,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, session[j])
            x1 = 10+j*120
            y1 = 50 +i*30
            e.place(x = x1 , y = y1)      
     
        i=i+1
    Sessions.mainloop()
    



def sem_list():

    Seminars = tk.Tk()
    Seminars.title("Seminars")
    Seminars.geometry("1900x900") 
        
    # Create title within page
    Label_Client = tk.Label(Seminars, text ="Fitness Seminars" )
    Label_Client.config(font=("Courier", 12))
    Label_Client.place(x = 10, y = 20)

    my_connect = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )  
    querySem = "select * from Fitness_seminar;"
    connectionSem = my_connect.cursor()
    connectionSem.execute(querySem)
    seminars = connectionSem.fetchall()
  
    i = 0
    for seminar in seminars: 
        
        #Create underlying buttons for the name of clients
        seminarInfoButton = tk.Button(Seminars, text =" Seminar Info ",
                          bg ='white', borderwidth = 0, command=lambda i=i :print(seminars[i]))
        y1 = 50
        y2 = y1+i*30

        seminarInfoButton.place(x = 1450, y = y2, width = 150) 

        for j in range(len(seminar)):
            e = Entry(Seminars,width=30, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, seminar[j])
            x1 = 10+j*120
            y1 = 50 +i*30
            e.place(x = x1 , y = y1)      
     
        i=i+1
    Seminars.mainloop()




# Instantiate instructor_home class
Instructor_home=tk.Tk()
Instructor_home.title("Instructor_Home_Page")
Instructor_home.geometry("900x900")
Label_IH = tk.Label(Instructor_home, text ="Instructor Home for _______" )
Label_IH.config(font=("Courier", 12))
Label_IH.place(x = 10, y = 20)

# Create Button Show My Clients
showClients = tk.Button(Instructor_home, text ="Show My Clients",
                      bg ='gray', command=client_list)
showClients.place(x = 150, y = 140, width = 200)

# Create Button Show Sessions
showSessions = tk.Button(Instructor_home, text ="Show My Sessions",
                      bg ='gray', command=sess_list)
showSessions.place(x = 150, y = 240, width = 200)

# Create Button Show Seminars
showSeminars = tk.Button(Instructor_home, text ="Show My Seminars",
                      bg ='gray', command=sem_list)
showSeminars.place(x = 150, y = 340, width = 200)

# Run main loop
Instructor_home.mainloop()