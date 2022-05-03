# SJSU CMPE 138 Spring 2022 TEAM5

from json.tool import main
import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call
from PIL import *
import argparse
import logging



python_alias = "python3"

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
parser.add_argument("--alias", help="python alias")
args = parser.parse_args()
inst_email = args.input
pwd = args.pw
usr="root"

log_file = 'instructor.txt'
log_fh = logging.FileHandler(log_file)

log_format = '%(asctime)s %(levelname)s: %(message)s'
# Possible levels: DEBUG, INFO, WARNING, ERROR, CRITICAL    
log_level = 'INFO' 
logging.basicConfig(format=log_format, level=log_level, 
    handlers=[log_fh])







# Get single client information
def singleClientWP(client_id):

    #Fetch single client information
    clientWP = tk.Tk()
    clientWP.title("Client Overview")
    clientWP.geometry("1200x900") 
  
    conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    cursor = conn.cursor()
    try:        
        # Get single client for current instructor
        query = "select distinct client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
    client_email, client_mobile from client where client_id = " +  "'" + str(client_id) + "'"
        logging.info(query) # save operation in log file
        cursor.execute(query)
        clientinfo = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Query was successful!")

    except mysql.Error as err:
        conn.rollback()
        logging.error(err)
        logging.error("Query not successful!")
        
    
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

        for j in range(2,7):

            e = Entry(clientWP,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
            x1 = 10+(j-2)*150
            y1 = 50 +i*20
            e.place(x = x1 , y = y1)
         
        i=i+1
    
    conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    cursor = conn.cursor()
    try:        
        # Get Workout for client
        query = "select * from Workout where Client_ID = " + "'" +str(client_id) + "' and Preparer_ID = '" +str(inst_id) + "'" 
        logging.info(query) # save operation in log file
        cursor.execute(query)
        workouts = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Query was successful!")

    except mysql.Error as err:
        conn.rollback()
        logging.error(err)
        logging.error("Query not successful!")


    #inst_id =Workout[0][3]
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
            e.insert(END, Workout[2-j])
            x1 = 10+j*120
            y1 = 100 +i*30
            e.place(x = x1 , y = y1)    
     
        i=i+1
    

    # Create Button Create Workout
    addWorkoutButton = tk.Button(clientWP, text ="Add Workout",
                        bg ='gray', command=lambda:addworkout(client_id,inst_id ,clientWP))
    addWorkoutButton.place(x = 150, y = 420, width = 200)


    # Create Button Contact Client
    contactClientB = tk.Button(clientWP, text ="Contact Client",
                        bg ='gray', command=lambda:contactClient(client_id, client_name,client_email,client_mobile)) 
    contactClientB.place(x = 550, y = 420, width = 200)

    clientWP.mainloop()


def contactNew():

    #Fetch single client information
    newclientEval = tk.Tk()
    newclientEval.title("Clients with no workout plan:")
    newclientEval.geometry("1200x900") 

    # Create title within page
    Label_New_Clients = tk.Label(newclientEval, text ="Clients with no workout plans:" )
    Label_New_Clients.config(font=("Courier", 12))
    Label_New_Clients.place(x = 10, y = 20)

    conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    cursor = conn.cursor()
    try:        
        # Get all clients that don't have Workout
        query = "select distinct client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
    client_email, client_mobile from client  where client_id not in (select Client_ID from Workout)" 
        # where client_id not in (select client_id from Workout) <--- NEEDS TO BE PUT IN WHEN 
        logging.info(query) # save operation in log file
        cursor.execute(query)
        clients = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Query was successful!")

    except mysql.Error as err:
        conn.rollback()
        logging.error(err)
        logging.error("Query not successful!")
    

    i=0
    
    for client in clients: 
        
        #Create underlying buttons for the name of clients
        createClientButtonN = tk.Button(newclientEval, text =" Client ",bg ='white', 
        borderwidth = 0, command=lambda i=i :contactClient(clients[i][3], clients[i][1],clients[i][7], clients[i][8]))
        y1 = 50
        y2 = y1+i*30
        createClientButtonN.place(x = 1000, y = y2, width = 100) 

        for j in range(len(client)-3):
            e = Entry(newclientEval,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
            x1 = 10+j*140
            y1 = 50 +i*30
            e.place(x = x1 , y = y1)      
     
        i=i+1

    newclientEval.mainloop()


def contactClient(client_id, client_name, client_email, client_mobile):

    # Pop out contaxt box with information
    contact = tk.Tk()
    contact.title("Contact Information")
    contact.geometry("480x360") 
    Label_Client = tk.Label(contact, text ="Contact Info for "+ str(client_name) )
    Label_Client.config(font=("Courier", 12))
    Label_Client.place(x = 10, y = 20)
    e = Entry(contact,width=24, fg='blue')
    e.insert(END, "ID #: " + str(client_id))
    e.place(x = 60 , y = 60)
    e = Entry(contact,width=24, fg='blue')
    e.insert(END, "Email: " + str(client_email))
    e.place(x = 60 , y = 120)
    e = Entry(contact,width=24, fg='blue')
    e.insert(END, "Number: " + str(client_mobile))
    e.place(x = 60 , y = 180)


    contact.mainloop()




def deleteworkout(client_id, Workout, i, clientWP):
    #Delete workout from Database
    conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    cursor = conn.cursor()
    try:        
        # Delete workout
        query = "delete from Workout where Workout.Client_ID\
         = " + "'" +str(client_id) + "'" + "and Workout.Workout_name =" + "'"+ str(Workout[i][2]) +"'" +" and\
        Workout.Preparer_ID = " +"'"+ str(inst_id) +"'"
        logging.info(query) # save operation in log file
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Query was successful!")

    except mysql.Error as err:
        conn.rollback()
        logging.error(err)
        logging.error("Query not successful!")

    msgbox.showinfo(message="Workout deleted",parent=clientWP)

    # Refresh UI   
    clientWP.destroy()
    singleClientWP(client_id)


def addworkout(client_id,inst_id ,clientWP):
  
    # Place text label for workout name
    workoutName = tk.Label(clientWP, text ="Workout Name: ", )
    workoutName.place(x = 50, y = 480)

    # Place input for workout name
    newWorkoutName = tk.Entry(clientWP, width = 360) # entry is a text box
    newWorkoutName.place(x = 250, y = 480, width = 360)

    #Place button to execute addition
    addWorkoutButtonN = tk.Button(clientWP, text =" Add ",
                          bg ='gray', borderwidth = 0, command=lambda :addtodb(clientWP, client_id,inst_id,newWorkoutName.get()))
    
    addWorkoutButtonN.place(x = 250, y = 520, width = 100)
    

def addtodb(clientWP, client_id,inst_id,inp):

    #Check that the input is not empty
    if (inp==""):
        msgbox.showerror(message="Please enter a workout name",title="Error",parent=clientWP)
        return
    
    conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    cursor = conn.cursor()
    try:        
        # Add workout to DB
        query =  "Insert into Workout values ('"+ str(client_id)+"',"+"'"+str(inst_id)+"','"+str(inp)+"');"
        logging.info(query) # save operation in log file
        cursor.execute(query)
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Query was successful!")

    except mysql.Error as err:
        conn.rollback()
        logging.error(err)
        logging.error("Query not successful!")

    msgbox.showinfo(title="Error",message="Workout Added",parent=clientWP)
    
    #Refresh UI
    clientWP.destroy()
    singleClientWP(client_id)


# Get complete client list on Instructor home page
def client_list():

    #Set up frame
    clientList = tk.Tk()
    clientList.title("clientList")
    clientList.geometry("1200x900") 

    # Create title within page
    LabelclientList = tk.Label(clientList, text ="Client List" )
    LabelclientList.config(font=("Courier", 12))
    LabelclientList.place(x = 10, y = 20)

    conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    cursor = conn.cursor()
    try:        
        # Get all clients for current instructor
        query ="select distinct I.Name ,I.ID,C.client_name,B.Client_ID from Instructor as I join Workout \
            as B on I.ID = B.Preparer_ID join client as C on C.client_id = B.Client_ID  where I.ID ="+ "'"+str(inst_id)+"'"   
        logging.info(query) # save operation in log file
        cursor.execute(query)
        clients = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Query was successful!")

    except mysql.Error as err:
        conn.rollback()
        logging.error(err)
        logging.error("Query not successful!")

    i = 0
    #client_id = clients[i][3]
    for client in clients: 
        
        #Create underlying buttons for the name of clients
        createClientButtonN = tk.Button(clientList, text =" Details ",
                          bg ='white', borderwidth = 0, command=lambda i=i :singleClientWP(clients[i][3]))
        y1 = 50
        y2 = y1+i*30
        createClientButtonN.place(x = 1000, y = y2, width = 100) 

        for j in range(len(client)):
            e = Entry(clientList,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
            x1 = 10+j*140
            y1 = 50 +i*30
            e.place(x = x1 , y = y1)      
     
        i=i+1
        
    clientList.mainloop()

#def sess_list():
#    call([python_alias,"training_instructor.py","--input", usr, "--pw",pwd])


def sess_list():

    Sessions = tk.Tk()
    Sessions.title("Sessions")
    Sessions.geometry("1200x900") 
        
    # Create title within page
    Label_Sessions = tk.Label(Sessions, text ="Training Sessions" )
    Label_Sessions.config(font=("Courier", 12))
    Label_Sessions.place(x = 10, y = 20)

    # Connect and query

    conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    cursor = conn.cursor()
    try:        
        # Get all sessions for current instructor
        query = "select * from training_session where session_instructor_id ='" + str(inst_id)+"'"
        logging.info(query) # save operation in log file
        cursor.execute(query)
        sessionsList = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Query was successful!")

    except mysql.Error as err:
        conn.rollback()
        logging.error(err)
        logging.error("Query not successful!")
    
    i = 0
    for session in sessionsList: 
        
        #Create underlying buttons for the name of clients
        createSessionButtonN = tk.Button(Sessions, text =" Session Info ",
                          bg ='white', borderwidth = 0, command=lambda i=i :sessionInfo(sessionsList[i]))
        y1 = 50
        y2 = y1+i*30

        createSessionButtonN.place(x = 1000, y = y2, width = 150) 

        for j in range(3):
            e = Entry(Sessions,width=20, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, session[3-j])
            x1 = 10+j*120
            y1 = 50 +i*30
            e.place(x = x1 , y = y1)      
     
        i=i+1
    Sessions.mainloop()
 


def sessionInfo(session):
    sess_ID = session[5]
    sess_Link = session[2]
    sess_Live = session[0]
    sess_Ind = session[1]

    # Pop out contaxt box with information
    sessZInfo = tk.Tk()
    sessZInfo.title("Session Information")
    sessZInfo.geometry("480x360") 
    Label_Session = tk.Label(sessZInfo, text ="Info for session "+ str(sess_ID) )
    Label_Session.config(font=("Courier", 12))
    Label_Session.place(x = 10, y = 20)
    e = Entry(sessZInfo,width=24, fg='blue')
    e.insert(END,  str(sess_Link))
    e.place(x = 60 , y = 60)
    e = Entry(sessZInfo,width=24, fg='blue')
    e.insert(END, "Live/Recorded:" + str(sess_Live))
    e.place(x = 60 , y = 120)
    e = Entry(sessZInfo,width=24, fg='blue')
    e.insert(END, "Ind/Group: " + str(sess_Ind))
    e.place(x = 60 , y = 180)
    sessZInfo.mainloop()




def sem_list():

    Seminars = tk.Tk()
    Seminars.title("Seminars")
    Seminars.geometry("1200x900") 
        
    # Create title within page
    Label_Seminars = tk.Label(Seminars, text ="Fitness Seminars" )
    Label_Seminars.config(font=("Courier", 12))
    Label_Seminars.place(x = 10, y = 20)

    
    # Query seminars

    conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    cursor = conn.cursor()
    try:        
        # Get all seminars for current instructor
        query = "select * from Fitness_seminar where FS_Inst_ID ='" + str(inst_id)+"'"
        logging.info(query) # save operation in log file
        cursor.execute(query)
        seminars = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Query was successful!")

    except mysql.Error as err:
        conn.rollback()
        logging.error(err)
        logging.error("Query not successful!")
    
  
    i = 0
    for seminar in seminars: 
        
        #Create underlying buttons for the name of clients
        seminarInfoButton = tk.Button(Seminars, text ="Info ",
                          bg ='white', borderwidth = 0, command=lambda i=i :Semzoom(seminars[i]))
        y1 = 50
        y2 = y1+i*30

        seminarInfoButton.place(x = 1060, y = y2, width = 150) 

        for j in range(1,len(seminar)-1):
            e = Entry(Seminars,width=30, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, seminar[j])
            x1 = 10+(j-1)*120
            y1 = 50 +i*30
            e.place(x = x1 , y = y1)      
     
        i=i+1
    Seminars.mainloop()

def Semzoom(semline):
    Semzoomlink = semline[0]

    # Pop out contaxt box with information
    semZoomInfo = tk.Tk()
    semZoomInfo.title("Zoom Information")
    semZoomInfo.geometry("480x360") 
    Label_Client = tk.Label(semZoomInfo, text ="Zoom info for seminar #"+ str(semline[1]) )
    Label_Client.config(font=("Courier", 12))
    Label_Client.place(x = 10, y = 20)
    e = Entry(semZoomInfo,width=24, fg='blue')
    e.insert(END,  str(Semzoomlink))
    e.place(x = 60 , y = 60)
    semZoomInfo.mainloop()




def training():

    Training = tk.Tk()
    Training.title("Trainees")
    Training.geometry("1200x900") 
        
    # Create title within page
    Label_Client = tk.Label(Training, text ="Trainees" )
    Label_Client.config(font=("Courier", 12))
    Label_Client.place(x = 10, y = 20)

    # Query trainees
    conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    cursor = conn.cursor()
    try:        
        # Get all trainees for current instructor
        query = "select * from Instructor where Trainer_id ='" + str(inst_id)+"'"
        logging.info(query) # save operation in log file
        cursor.execute(query)
        trainees = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Query was successful!")

    except mysql.Error as err:
        conn.rollback()
        logging.error(err)
        logging.error("Query not successful!")

  
    i = 0
    for trainee in trainees: 
        #Create underlying buttons for the name of clients
        traineeContact = tk.Button(Training, text =" Contact ",
                          bg ='white', borderwidth = 0, command=lambda i=i :contactTrainee(trainees[i]))
        y1 = 50
        y2 = y1+i*30

        traineeContact.place(x = 1000, y = y2, width = 150) 

        for j in range(1,2):
            e = Entry(Training,width=30, fg='blue')
            e.grid(row=i, column=j) 
            e.insert(END, trainee[j])
            x1 = 10+(j-1)*120
            y1 = 50 +i*30
            e.place(x = x1 , y = y1)      
     
        i=i+1
    Training.mainloop()


def contactTrainee(Trainee):
    Tee_id = Trainee[0]
    Tee_name = Trainee[1]
    Tee_email = Trainee[3]

    # Pop out contaxt box with information
    contact = tk.Tk()
    contact.title("Contact Information")
    contact.geometry("480x360") 
    labelContactTrainee = tk.Label(contact, text ="Contact Info for "+ str(Tee_name) )
    labelContactTrainee.config(font=("Courier", 12))
    labelContactTrainee.place(x = 10, y = 20)
    e = Entry(contact,width=24, fg='blue')
    e.insert(END, "ID #: " + str(Tee_id))
    e.place(x = 60 , y = 60)
    e = Entry(contact,width=24, fg='blue')
    e.insert(END, "Email: " + str(Tee_email))
    e.place(x = 60 , y = 120)
    contact.mainloop()





# Instantiate instructor_home class
# Find info on current instructor
conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
cursor = conn.cursor()
try:       

    # Get all trainees for current instructor
    query = "select Name,ID from Instructor where Email = '" + str(inst_email)+"'"
    logging.info(query) # save operation in log file
    cursor.execute(query)
    instinfo = cursor.fetchall()
    inst_name = instinfo[0][0]
    inst_id = instinfo[0][1]

    # Check if there is a trainer for the current instructor
    queryTrainer = "select Trainer_id from Instructor where ID = '" + str(inst_id)+"'"
    logging.info(query) # save operation in log file
    cursor.execute(queryTrainer)
    tr_id = cursor.fetchall()[0][0]
    cursor.close()
    conn.commit()
    conn.close()
    logging.info("Query was successful!")

except mysql.Error as err:
    conn.rollback()
    logging.error(err)
    logging.error("Query not successful!")
inst_name = instinfo[0][0]
inst_id = instinfo[0][1]


# Instructor home window 
Instructor_home=tk.Tk()
Instructor_home.title("Instructor_Home_Page")
Instructor_home.geometry("900x900")
Label_IH = tk.Label(Instructor_home, text ="Instructor Home for "+str(inst_name) )
Label_IH.config(font=("Courier", 12))
Label_IH.place(x = 10, y = 20)


# Create Button Show My Clients
showClients = tk.Button(Instructor_home, text ="Show My Clients",
                      bg ='gray', command=client_list)
showClients.place(x = 150, y = 140, width = 220)

# Create Button Show Sessions
showSessions = tk.Button(Instructor_home, text ="Show My Sessions",
                      bg ='gray', command=sess_list)
showSessions.place(x = 150, y = 240, width = 220)

# Create Button Show Seminars
showSeminars = tk.Button(Instructor_home, text ="Show My Seminars",
                      bg ='gray', command=sem_list)
showSeminars.place(x = 150, y = 340, width = 220)       


# Create Button Show Trainees
showSeminars = tk.Button(Instructor_home, text ="Show My Trainees",
                      bg ='gray', command=training)
showSeminars.place(x = 150, y = 440, width = 220)

# Create Button Show Trainees
showSeminars = tk.Button(Instructor_home, text ="Contact New Client",
                      bg ='gray', command=contactNew)
showSeminars.place(x = 150, y = 540, width = 220)

if (str(tr_id) != "None"):
    # Query for Trainer email 
    conn = mysql.connect(host="localhost", user=usr, passwd=pwd, database="fitnessstudio" )
    cursor = conn.cursor()

    try:        
        # Get trainer info for instructor
        query = "select Email,Name from Instructor where ID = '" + str(tr_id)+"'"
        logging.info(query) # save operation in log file
        cursor.execute(query)
        trainerInfo = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        logging.info("Query was successful!")

    except mysql.Error as err:
        conn.rollback()
        logging.error(err)
        logging.error("Query not successful!")
     
    tr_email= trainerInfo[0][0]
    tr_name = trainerInfo[0][1]

    # Create label for training instructor
    Label_IH = tk.Label(Instructor_home, text ="Training supervisor: " +str(tr_name)+", email: " +str(tr_email) )
    Label_IH.config(font=("Courier", 12))
    Label_IH.place(x = 10, y = 70)

#If no supervisor => lead Trainer
if (str(tr_id) == "None"):
    Label_IH = tk.Label(Instructor_home, text ="Lead Trainer" )
    Label_IH.config(font=("Courier", 12))
    Label_IH.place(x = 10, y = 70)

# Run main loop
Instructor_home.mainloop()