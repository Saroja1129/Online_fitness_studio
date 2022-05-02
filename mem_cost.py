# SJSU CMPE 138 Spring 2022 TEAM5

import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call
import argparse
import logging


# pass current user information
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
parser.add_argument("--alias", help = "python alias")
args = parser.parse_args()
user = args.input
local_DB_Password = args.pw
python_alias= args.alias

# Create log file
log_file = 'adminLog.txt'
log_fh = logging.FileHandler(log_file)

log_format = '%(asctime)s %(levelname)s: %(message)s'
# Possible levels: DEBUG, INFO, WARNING, ERROR, CRITICAL    
log_level = 'INFO' 
logging.basicConfig(format=log_format, level=log_level, 
    handlers=[log_fh])



def changed():
    a=Mem_level.get()
    b=Mem_cost.get() 
   # print(a)
    #print(b)
    try:
        m = mysql.connect(host="localhost", user="root", passwd=local_DB_Password, database="fitnessstudio" )
        connection = m.cursor()
        try:
            query="update membership set mem_cost=%s where mem_level=%s"
            logging.info(query) # save operation in log file
            connection.execute(query,[b,a])
            myresult = connection.fetchall()
            m.commit()
            logging.info("Query was successful!")

        except mysql.Error as err:
            logging.error(err)
            logging.error("Query not successful!")
            
  
        msgbox.showinfo("Error Status","Updation done") 
    except:
        msgbox.showinfo("Error Status","Not done") 
        

a=tk.Tk()
a.geometry("200x300")

Label_1 = tk.Label(a, text ="Membership level", )
Label_1.place(x=10, y=10)

Mem_level = tk.Entry(a, width = 20)
Mem_level.place(x=10, y= 50)

Label_2 = tk.Label(a, text ="Membership cost", )
Label_2.place(x=10, y= 100)

Mem_cost = tk.Entry(a, width = 20)
Mem_cost.place(x=10, y= 150)



submitbtn1 = tk.Button(a, text ="Modify",bg ='silver', command=changed)
submitbtn1.place(x=10,y=200)
a.mainloop()
