import tkinter as tk
import mysql.connector as mysql
import tkinter.messagebox as msgbox
from tkinter import *
from subprocess import call

def client_list():
    call(["python","clientgrid.py"])
    
def create_fitness_seminar():
    call(["python","fitness_seminar.py"])    

Admin_home=tk.Tk()
Admin_home.title("Admin_Home_Page")
Admin_home.geometry("800x600")



submitbtn = tk.Button(Admin_home, text ="client_list",
                      bg ='yellow', command=client_list)
submitbtn.place(x = 150, y = 140, width = 100)

submitbtn = tk.Button(Admin_home, text ="schedule fitness seminar",
                      bg ='yellow', command=create_fitness_seminar)
submitbtn.place(x = 150, y = 180, width = 150)

Admin_home.mainloop()
