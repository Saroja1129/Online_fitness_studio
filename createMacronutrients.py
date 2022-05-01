import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import *
import logging

# Create log file
log_file = 'dietitianLog.txt'
log_fh = logging.FileHandler(log_file)

log_format = '%(asctime)s %(levelname)s: %(message)s'
# Possible levels: DEBUG, INFO, WARNING, ERROR, CRITICAL    
log_level = 'INFO' 
logging.basicConfig(format=log_format, level=log_level, 
    handlers=[log_fh])

# The script needs to be read from the bottom to the top. The main dietitian home page is initiated after all functions needed are defined.
# 1.) Get single client by pushing button GetClient
# 2.) Create Diet Plan Option and/or Create Supplement Option are implemented as buttons
# 3.) Create Diet Plan calls showDietPlan, which shows the current diet plan: 
    # it pulls the data from an existing dietary plan from the database and if not existent it fills the output with 0's
# 4.) showDietPlan calls inputDietPlan that saves input data from the white entry options into the database by pushing the button OK
# 5.) The button ok calls insert_or_update function
# 6.) insert_or_update: checks if current plan values are available, if not creates a new dietary plan by inserting values in diatray_plan and plan_macronutrients
#      values rae provided as input by the advisor user. If a plan exists, the an update query performs the database updates



def insert_or_update(connection, dietitian, result, client_id, proteinEntry, carbsEntry, fatEntry):

    protein = proteinEntry.get()
    carbs = carbsEntry.get()
    fat = fatEntry.get()

    # Check for complete user input
    if(protein=="" or carbs=="" or fat==""):
        msgbox.showinfo("Insert status","all fields are required")

    # Check if current die plan does not exist
    if result ==[]:

        # if plan supplements is not existent, but already a diet plan ID was created for specific client, fetch client id, otherwise create new plan ID
        
        try:              
            query = "select diet_plan_ID from dietary_plan where clientID = " + "'"+str(client_id)+"'" +""
            logging.info(query) # save operation in log file
            connection.execute(query)
            logging.info("Query was successful!")

        except mysql.connector.Error as err:
            logging.error(err)
            logging.error("Query not successful!")
        

        planID = connection.fetchall()

        if planID !=[]: # if plan ID already exist for specific client use it to create the supplement plan
            newPlanID = planID[0][0]
        else:
            # Get current maximum plan value
            try:              
                query = "select max(diet_plan_ID) from dietary_plan"
                logging.info(query) # save operation in log file
                connection.execute(query)
                logging.info("Query was successful!")

            except mysql.connector.Error as err:
                logging.error(err)
                logging.error("Query not successful!")

        
            maxPlanID = connection.fetchall()
            maxPlanID = maxPlanID[0][0]

            # Set new plan ID by incrementing plan ID +1
            newPlanID = int(maxPlanID) +1

            # Create a new dietary plan for particluar client
            try:              
                query = "insert into dietary_plan values ("+ "'"+str(newPlanID)+"'" +"," "'"+str(userID)+"'," + "'"+str(client_id)+"'" +")"
                logging.info(query) # save operation in log file
                connection.execute(query)
                logging.info("Query was successful!")

            except mysql.connector.Error as err:
                logging.error(err)
                logging.error("Query not successful!")


        # Insert macronutrients
        try:              
            query = "insert into plan_macronutrients values ("+ "'"+str(newPlanID)+"'" +"," + protein +" , "+ carbs +","+ fat +")" 
            logging.info(query) # save operation in log file
            connection.execute(query)
            logging.info("Query was successful!")

        except mysql.connector.Error as err:
            logging.error(err)
            logging.error("Query not successful!")
        
       
    else:
        # Update an existing dietary plan
        try:              
            query = "update plan_macronutrients \
                set protein = "  + protein +" , carbs = "+ carbs +", fat = "+ fat +" \
                where diet_plan_ID_macro in (select diet_plan_ID from dietary_plan where clientID = " +  "'" + str(client_id) + "'"  +")"
            logging.info(query) # save operation in log file
            connection.execute(query)
            logging.info("Query was successful!")

        except mysql.connector.Error as err:
            logging.error(err)
            logging.error("Query not successful!")


    
    # Show diet plan
    showDietPlan(connection, dietitian, client_id, proteinEntry, carbsEntry, fatEntry)



# Buttons and inputs created for diet plan
def inputDietPlan(connection, dietitian, result, client_id, proteinEntry, carbsEntry, fatEntry):


    # Create Button to log diet plan values with pressing OK
    createOKButton = tk.Button(dietitian, text ="Ok",
                        bg ='grey', command=lambda:insert_or_update(connection, dietitian ,result, client_id, proteinEntry, carbsEntry, fatEntry)) # pass result to check for empty
    createOKButton.place(x = 150, y = 350, width = 50)

    


# Show diet plan if already existing
def showDietPlan(connection, dietitian, client_id, proteinEntry, carbsEntry, fatEntry):

    # Get current plan
    try:              
        query = "select protein, carbs, fat \
            from dietary_plan, plan_macronutrients \
            where diet_plan_ID_macro = diet_plan_ID and clientID = " +  "'" + str(client_id) + "'" 
        logging.info(query) # save operation in log file
        connection.execute(query)
        logging.info("Query was successful!")

    except mysql.connector.Error as err:
        logging.error(err)
        logging.error("Query not successful!")
   
   
   
    # Fetch results
    result = connection.fetchall()

    # Check if client already has a plan: if not set default values to zero
    if result == []:
        insert0 = 0
        insert1 = 0
        insert2 = 0

    else:
        insert0 = result[0][0] 
        insert1 = result[0][1] 
        insert2 = result[0][2] 


    Protein = tk.Label(dietitian, text ="Protein ", )
    Protein.place(x = 450, y = 260)

    e = Entry(dietitian,width=20, fg='blue')
    e.insert(END,insert0)
    e.place(x = 550 , y = 260)

    Carbs = tk.Label(dietitian, text ="Carbohydrates ", )
    Carbs.place(x = 450, y = 285)

    f = Entry(dietitian,width=20, fg='blue')
    f.insert(END,insert1)
    f.place(x = 550 , y = 285)


    Fat = tk.Label(dietitian, text ="Fat ", )
    Fat.place(x = 450, y = 310)

    g = Entry(dietitian,width=20, fg='blue')
    g.insert(END,insert2)
    g.place(x = 550 , y = 310)

    inputDietPlan(connection, dietitian, result, client_id, proteinEntry, carbsEntry, fatEntry)




# Buttons and inputs created for diet plan
def createDietPlan(dietitian, connection, client_id):

    name = tk.Label(dietitian, text ="Protein ", )
    name.place(x = 50, y = 260)

    proteinEntry = tk.Entry(dietitian, width = 35) # entry is a text box
    proteinEntry.place(x = 150, y = 260, width = 200)


    name = tk.Label(dietitian, text ="Carbohydrates ", )
    name.place(x = 50, y = 285)

    carbsEntry = tk.Entry(dietitian, width = 35) # entry is a text box
    carbsEntry.place(x = 150, y = 285, width = 200)


    name = tk.Label(dietitian, text ="Fat ", )
    name.place(x = 50, y = 310)

    fatEntry = tk.Entry(dietitian, width = 35) # entry is a text box
    fatEntry.place(x = 150, y = 310, width = 200)


    # Show available diet plan: if not available fill with zeros
    showDietPlan(connection, dietitian, client_id, proteinEntry, carbsEntry, fatEntry)