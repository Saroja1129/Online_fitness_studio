import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import *


def insert_or_updateSuppl(connection, dietitian ,result, client_id, VD3Entry, VCEntry, magEntry, omEntry):

    vitD = VD3Entry.get()
    vitC = VCEntry.get()
    mag = magEntry.get()
    omega = omEntry.get()

    # Check for complete user input
    if(vitD=="" or vitC=="" or mag=="" or omega==""):
        msgbox.showinfo("Insert status","all fields are required")

    # Check if current die plan does not exist
    if result ==[]:

        # if plan supplements is not existent, but already a diet plan ID was created for specific client, fetch client id, otherwise create new plan ID
        query = "select diet_plan_ID from dietary_plan where clientID = " + "'"+str(client_id)+"'" +""
        connection.execute(query)

        planID = connection.fetchall()

        if planID !=[]: # if plan ID already exist for specific client use it to create the supplement plan
            newPlanID = planID[0][0]
        else:

            # Get current maximum plan value
            query = "select max(diet_plan_ID) from dietary_plan"
            connection.execute(query)
            maxPlanID = connection.fetchall()
            maxPlanID = maxPlanID[0][0]

            # Set new plan ID by incrementing plan ID +1
            newPlanID = int(maxPlanID) +1

            # Create a new dietary plan for particluar client
            query0 = "insert into dietary_plan values ("+ "'"+str(newPlanID)+"'" +"," "'"+str(userID)+"'," + "'"+str(client_id)+"'" +")"
            connection.execute(query0)


        # Insert macronutrients
        query1 = "insert into plan_supplements values ("+ "'"+str(newPlanID)+"'" +"," + vitD +" , "+ vitC +","+ mag + ","+ omega+")" 
        connection.execute(query1)
    else:
        # Update an existing dietary plan
        query = "update plan_supplements \
                set vitaminD3 = "  + vitD +" , vitaminC= "+ vitC +", magnesium = "+ mag+", omega3 = "+omega+" \
                where diet_plan_ID_suppl in (select diet_plan_ID from dietary_plan where clientID = " +  "'" + str(client_id) + "'"  +")"
        connection.execute(query)
    
    # Show diet plan
    showSupplPlan(connection, dietitian, client_id, VD3Entry, VCEntry, magEntry, omEntry)



# Buttons and inputs created for diet plan

def inputSupplPlan(connection, dietitian, result, client_id, VD3Entry, VCEntry, magEntry, omEntry):


    # Create Button to log diet plan values with pressing OK
    createOKButton = tk.Button(dietitian, text ="Ok",
                        bg ='grey', command=lambda:insert_or_updateSuppl(connection, dietitian ,result, client_id, VD3Entry, VCEntry, magEntry, omEntry)) # pass result to check for empty
    createOKButton.place(x = 150, y = 670, width = 50)

    


# Show diet plan if alraedy existing
def showSupplPlan(connection, dietitian, client_id, VD3Entry, VCEntry, magEntry, omEntry):

    # Get current plan
    query = "select vitaminD3, vitaminC, magnesium, omega3 \
            from dietary_plan, plan_supplements \
            where diet_plan_ID_suppl = diet_plan_ID and clientID = " +  "'" + str(client_id) + "'" 
     
    connection.execute(query)

    
    # Fetch results
    result = connection.fetchall()

    # Check if client already has a plan: if not set default values to zero
    if result == []:
        insert0 = 0
        insert1 = 0
        insert2 = 0
        insert3 = 0

    else:
        insert0 = result[0][0] 
        insert1 = result[0][1] 
        insert2 = result[0][2] 
        insert3 = result[0][3] 


    vD3 = tk.Label(dietitian, text ="Vitamin D3 ", )
    vD3.place(x = 450, y = 560)

    e = Entry(dietitian,width=20, fg='blue')
    e.insert(END,insert0)
    e.place(x = 550 , y = 560)

    vC = tk.Label(dietitian, text ="Vitamin C", )
    vC.place(x = 450, y = 585)

    f = Entry(dietitian,width=20, fg='blue')
    f.insert(END,insert1)
    f.place(x = 550 , y = 585)


    mag = tk.Label(dietitian, text ="Magnesium", )
    mag.place(x = 450, y = 610)

    g = Entry(dietitian,width=20, fg='blue')
    g.insert(END,insert2)
    g.place(x = 550 , y = 610)

    om = tk.Label(dietitian, text ="Omega3", )
    om.place(x = 450, y = 635)

    g = Entry(dietitian,width=20, fg='blue')
    g.insert(END,insert3)
    g.place(x = 550 , y = 635)

    inputSupplPlan(connection, dietitian, result, client_id, VD3Entry, VCEntry, magEntry, omEntry)

    


# Buttons and inputs created for diet plan
def createSupplements(dietitian, connection, client_id):

    name = tk.Label(dietitian, text ="Vitamin D3 ", )
    name.place(x = 50, y = 560)

    VD3Entry = tk.Entry(dietitian, width = 35) # entry is a text box
    VD3Entry.place(x = 150, y = 560, width = 200)


    name = tk.Label(dietitian, text ="Vitamin C ", )
    name.place(x = 50, y = 585)

    VCEntry = tk.Entry(dietitian, width = 35) # entry is a text box
    VCEntry.place(x = 150, y = 585, width = 200)


    name = tk.Label(dietitian, text ="Magnesium ", )
    name.place(x = 50, y = 610)

    magEntry = tk.Entry(dietitian, width = 35) # entry is a text box
    magEntry.place(x = 150, y = 610, width = 200)


    name = tk.Label(dietitian, text ="Omega3 ", )
    name.place(x = 50, y = 635)

    omEntry = tk.Entry(dietitian, width = 35) # entry is a text box
    omEntry.place(x = 150, y = 635, width = 200)


    # Show available diet plan: if not available fill with zeros
    showSupplPlan(connection, dietitian, client_id, VD3Entry, VCEntry, magEntry, omEntry)