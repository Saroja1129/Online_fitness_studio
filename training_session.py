import tkinter.messagebox as tkmb
import tkinter as tk
import mysql.connector as mysql
from tkinter import *

def print_answers():
    value = value_inside.get()
    #print("        ", value)
    value = value.lstrip("(")
    value = value.rstrip(",)")
    
    #print("============")
    #print(value)
    if "live" in value:
        if "individual" in value:
            tkmb.showinfo("title", "Please upgrade your membership first!")
    else:
        for result in result_list:
            #print("====", value, type(value))
            #print("----", result[0:3], type(result[0:3]))
            result_str = str(result[0:3])
            #print("++++++", result_str)
 
            if value in result_str:
                tkmb.showinfo("This is the zoom link to access the session: \n", str(result[3]))

root = tk.Tk()
root.title("Welcome to Training Session Page")
root.geometry('700x500')

con=mysql.connect(host="localhost",user="root",password="password",db="fitnessstudio")
cursor=con.cursor()
cursor.execute("select instructor.name, session_type, session_individual_group, session_zoom_link, training_session.session_id, session_instructor_id, client_id \
from training_session join training_session_client join instructor \
where training_session.session_id = training_session_client.session_id \
and training_session.session_instructor_id = instructor.ID")

results=cursor.fetchall()

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
