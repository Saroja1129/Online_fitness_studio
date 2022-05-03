import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call
import argparse

# pass current user information
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for dB engine")
parser.add_argument("--alias", help = "python alias")
args = parser.parse_args()
user = args.input
local_dB_password = args.pw
python_alias= args.alias


from feedbackDietitian import *


def viewcomment(client_id):
    
    Comment= tk.Tk()
    Comment.geometry("350x250")
    
    con=mysql.connect(host="localhost",user="root",password=local_dB_password,db="fitnessstudio")
    cursor=con.cursor() 
    cursor.execute("select M_C_plan_id, M_C_comment from mental_coaching_plan where clientid=" +  "'" + str(client_id) + "'" + "")
    results = cursor.fetchall()
    
    i=0 
    for client in results: 
        for j in range(len(client)):
            e = Entry(Comment, width=10, fg='Magenta') 
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
    i=i+1
    
    Comment.mainloop()
    

def GiveFeedback(client_id):
    
    con=mysql.connect(host="localhost",user="root",password=local_dB_password,db="fitnessstudio")
    cursor=con.cursor() 
    cursor.execute("select client_feedback from clientid= " +  "'" + str(client_id) + "'" + "")
    results = cursor.fetchall()
    
    feedbackEntry = tk.Entry(mental_coach, width = 50) # entry is a text box
    feedbackEntry.insert(END,results)
    feedbackEntry.place(x = 100, y = 100, width = 400)
   
    

def GiveComment(client_id):
   
    def submitact():
        con=mysql.connect(host="localhost",user="root",password=local_dB_password,db="fitnessstudio")
        cursor=con.cursor() 
        cursor.execute("select M_C_plan_id from mental_coaching_plan")
        results = cursor.fetchall()
        a=len(results)
        print(results[a-1])
        S = str(results[a-1]) 
        a= str(int(S[2:6])+1)
      
        d=Testname.get()
        b=userId
        c=client_id
        
        try:
            con=mysql.connect(host="localhost",user="root",password=local_dB_password,db="fitnessstudio")
            cursor=con.cursor()
            print("insert into mental_coaching_plan values(%s,%s,%s,%s)",[a,b,c,d])
            cursor.execute("insert into mental_coaching_plan values(%s,%s,%s,%s)",[(a),(b),(c),(d)])
            con.commit()
            results=cursor.fetchall()
            msgbox.showinfo("Create status","Comment added Succesfully")
        except:
            print("Error: unable to create")
            msgbox.showinfo("Create status","Comment added Unsuccesfull")
      
    B=tk.Tk()
    B.title("Mental_Coach")
    B.geometry("800x600")

    Label1 = tk.Label(B, text ="AddComment")
    Label1.place(x = 50, y = 300)
    
    Testname = tk.Entry(B, width = 35)
    Testname.place(x = 200, y = 300, width = 200)
    
    submitbtn = tk.Button(B, text ="Submit", bg ='Magenta',command =submitact)
    submitbtn.place(x = 350, y = 500, width = 150)
    
    B.mainloop()

def getClientInfo(i):

    client_id = myresult[i][0]
    clientPlans = tk.Tk()
    clientPlans.title("Client Plans")
    clientPlans.geometry("1300x900") 
    my_connect = mysql.connect(host="localhost", user="root", passwd=local_dB_password, database="fitnessstudio" )
    connection = my_connect.cursor()


    # Get single client for current advisor
    query = "select client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
    client_email, client_mobile \
    from client \
    where client_id = " +  "'" + str(client_id) + "'" + " and client_id in(select clientId from advises where advId = " +  "'" + str(userId) + "'" + ")"

    connection.execute(query)

    # Show client details
    i = 0
    for client in connection: 
        for j in range(len(client)):
            e = Entry(clientPlans,width=20, fg='Magenta')
            e.grid(row=i, column=j) 
            e.insert(END, client[j])
            x1 = 10+j*120
            y1 = 50 +i*20
            e.place(x = x1 , y = y1)
        
     
        i=i+1

    
  
    createcommentButton = tk.Button(clientPlans, text ="Give comment on mental health",
                        bg ='Magenta', command=lambda:GiveComment(client_id)) 
    createcommentButton.place(x = 150, y = 220, width = 200)

    viewPrescriptionPlanButton = tk.Button(clientPlans, text ="View comment of Client",
                        bg ='Magenta', command=lambda:viewcomment(client_id)) 
    viewPrescriptionPlanButton.place(x = 300, y = 220, width = 200)

  
    createFeedbackButton = tk.Button(clientPlans, text ="Feedback to Client",
                        bg ='blue', command=lambda:showFeedback(clientPlans,connection, client_id)) 
    createFeedbackButton.place(x = 850, y = 200, width = 200)
    
    
    

    clientPlans.mainloop()




# -------------------
# Mental_coach home page 

mental_coach = tk.Tk()
mental_coach.title("doctor")
mental_coach.geometry("1300x900") 
my_connect = mysql.connect(host="localhost", user="root", passwd=local_dB_password , database="fitnessstudio" )
connection = my_connect.cursor()

# Fetch the advisor information(Id):
query = "select Id from advisor where email = " +  "'" + str(user) + "'"  +""
connection.execute(query)
userId = connection.fetchall()
userId = userId[0][0]


# Get the clients with premium membership and the advisor related to the client Id
query = "select client_id, client_name , client_age, client_gender, client_height, client_weight, client_bmi, \
client_email, client_mobile \
from client \
where client_id in(select clientId from advises where advId = " +  "'" + str(userId) + "'" + " and clientId in(select mem_client_id from membership where mem_level = 'Premium'))" 

connection.execute(query)

myresult = connection.fetchall()

    
# Create title within page
Label_Client = tk.Label(mental_coach, text ="Client List" )
Label_Client.config(font=("Courier", 15))
Label_Client.place(x = 10, y = 20)

i = 0

for client in myresult: 

    #Create underlying buttons for the name of clients
    createClientButtonN = tk.Button(mental_coach, text =" Get Client ",
                        bg ='white', borderwidth = 0, command=lambda i=i:getClientInfo(i))
    y1 = 50
    y2 = y1+i*20

    createClientButtonN.place(x = 1150, y = y2, width = 80) 

    
    for j in range(len(client)):
        
        e = Entry(mental_coach,width=20, fg='Magenta')
        e.grid(row=i, column=j) 
        e.insert(END, client[j])
        x1 = 10+j*120
        y1 = 50 +i*20
        e.place(x = x1 , y = y1)      
    
    i=i+1

mental_coach.mainloop()

