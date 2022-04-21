import mysql.connector
import tkinter  as tk 
from tkinter import * 
my_w = tk.Tk()
my_w.geometry("700x250") 
# Update user and password
my_connect = mysql.connector.connect(
  host="localhost",
  user="root", 
  passwd="Arti@123",
  database="fitnessstudio"
)
my_conn = my_connect.cursor()

my_conn.execute("SELECT * FROM client")
i=0 
for client in my_conn: 
    for j in range(len(client)):
        e = Entry(my_w, width=10, fg='blue') 
        e.grid(row=i, column=j) 
        e.insert(END, client[j])
    i=i+1
my_w.mainloop()