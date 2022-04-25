import tkinter.messagebox as tkmb
import tkinter as tk
import mysql.connector as mysql
from tkinter import *

def print_answers():
    value = value_inside.get()
    #print("        ", value)
    value = value.lstrip("(")
    value = value.rstrip(",)")

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
cursor.execute("select * from training_session")
results=cursor.fetchall()

option_item_list = list()
result_list = list()

for item in results:
    items = list()
    items.append(item[0:3])
    option_item_list.append(items)
    result_list.append(item[0:4])

value_inside = tk.StringVar(root)
value_inside.set("Select an Option")

question_menu = tk.OptionMenu(root, value_inside, *option_item_list)
question_menu.pack()

submit_button = tk.Button(root, text='Submit', command=print_answers)
submit_button.pack()

root.mainloop()
