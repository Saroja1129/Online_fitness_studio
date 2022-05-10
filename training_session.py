# SJSU CMPE 138 Spring 2022 TEAM5
import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as tkmb 
from tkinter import *
from subprocess import call
from PIL import *
import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Current user ")
parser.add_argument("--pw", help="Local password for DB engine")
parser.add_argument("--alias", help = "python alias")
args = parser.parse_args()
user = args.input
python_alias= args.alias
#python_alias="python3"
local_DB_password = args.pw
#local_DB_password = "password"

log_file = "training_session.txt"
log_fh = logging.FileHandler(log_file)

log_format = '%(asctime)s %(levelname)s: %(message)s'
# Possible levels: DEBUG, INFO, WARNING, ERROR, CRITICAL    
log_level = 'INFO' 
logging.basicConfig(format=log_format, level=log_level, handlers=[log_fh])

def print_answers():
    value = value_inside.get()
    #print("        ", value)
    value = value.lstrip("(")
    value = value.rstrip(",)")
    
    #print("============")
    #print(value)
    #print("__", type(user))
    try:
        con=mysql.connect(host="localhost",user="root",password=local_DB_password, db="fitnessstudio")
        cursor=con.cursor()
        query = "select mem_level from membership join client on mem_client_id = client_id where client_email =" + "'" + str(user) +"'"
        cursor.execute(query)
        obversations = cursor.fetchall() 
        logging.info(query)
        logging.info("Query was successfully!")
    except mysql.Error as err:
        logging.error(err)
        logging.error("Query not successful!")

    b = str(obversations[len(obversations)-1])[2]

    if(b =='F'):
       Type="Free"
    elif(b=='B'):
        Type="Basic"
    elif(b=='P'):
        Type="Premium"

    if ("recorded" in value) and (Type == "Free" or Type == "Basic" or Type == "Premium"):
        for result in result_list:
            result_str = str(result[0:3])
            if value in result_str:
                tkmb.showinfo("This is the zoom link to access the session: \n", str(result[3]))
    elif ("live" in value) and (Type == "Basic" or Type == "Premium"):
        for result in result_list:
            result_str = str(result[0:3])
            if value in result_str:
                tkmb.showinfo("This is the zoom link to access the session: \n", str(result[3]))
    else: 
        tkmb.showinfo("title", "Please upgrade your membership first!")
        #wait(10)
        root.destroy()
        call([python_alias,"Premium.py","--input", user, "--pw",local_DB_password, "--alias", python_alias])
        #call([python_alias,"admin_login.py","--input", user, "--pw",local_DB_password])

root = tk.Tk()
root.title("Training Session Page for Clients")
root.geometry('700x500')
try:
    con=mysql.connect(host="localhost",user="root",password=local_DB_password,db="fitnessstudio")
    cursor=con.cursor()
    query = "select Instructor.name, session_type, session_individual_group, session_zoom_link, training_session.session_id, session_instructor_id, client_id \
from training_session join training_session_client join Instructor \
where training_session.session_id = training_session_client.session_id \
and training_session.session_instructor_id = Instructor.ID"
    cursor.execute(query)
    results=cursor.fetchall()
    logging.info(query)
    logging.info("Query was successful!")
except mysql.Error as err:
    logging.error(err)
    logging.error("Query not successful!")


option_item_list = list()
result_list = list()

for item in results:
    #print("============", item)
    #print(item
    #items = list()
    #items.append(item[0:3])
    #option_item_list.append(items)
    option_item_list.append(item[0:3])
    result_list.append(item[0:4])

value_inside = tk.StringVar(root)
value_inside.set("Select an Option")

question_menu = tk.OptionMenu(root, value_inside, *option_item_list)
question_menu.pack()

submit_button = tk.Button(root, text='Submit', command=print_answers)
submit_button.pack()

root.mainloop()
