# =====importing libraries===========
'''This is the section where you will import libraries'''
import time
from datetime import date
import datetime
from random import randint

# =====define functions===========

# function to register a new user (admin only)

def reg_user(username):
    if username == "admin":
        new_username = input("Please enter a new username: ")
        while new_username in username_and_passwords:
            new_username = input(
                "That username has been taken, please enter a different username: ")

        new_password = input("Please enter a new password: ")
        password_check = input("Please confirm your new password: ")
        while new_password != password_check:
            password_check = input(
                "Passwords do not match, please confirm your new password: ")
        user_details = open('user.txt', 'a')
        user_details.write(f"\n{new_username},{new_password}")
        user_details.close()
        print("Username and password have been added to the system.")
        time.sleep(1)
        menu = menu_selector(username)
        menu_choice(menu)
    else:
        print("ACCESS DENIED! You do not have admin level permissions")
        time.sleep(1)
        menu = menu_selector(username)
        menu_choice(menu)

# function to add new task (any user)

def add_task():
    user_assignment = input("Who is this task for?: ")
    task_title = input("Please give this task a title: ")
    task_description = input(
        "Please provide a brief description of the task: ")
    task_start_date = date.today()
    # task_due_date = input(
    #     "Please enter when this task us due for completion: ")
    date_entry = input('Enter the date the task is due, in YYYY-MM-DD format')
    year, month, day = map(int, date_entry.split('-'))
    date1 = datetime.date(year, month, day)
    task_id = str(randint(1, 10000))
    task_details = open('tasks.txt', 'a')
    task_details.write(
        f"\n{user_assignment},{task_title},{task_description},{task_start_date},{date1},No,{task_id}")
    print("A new task has been added and assigned - Have a good day!")
    task_details.close()
    menu = menu_selector(username)
    menu_choice(menu)

# function to view all tasks in system

def view_all():
    with open('tasks.txt', 'r') as task_details:
        for line in task_details:
            task_list = line.split(",")
            print(f"""
___________________________________________________
ID:{task_list[6]}
Task:                  {task_list[1]}
Assigned to:           {task_list[0]}
Date assigned:         {task_list[3]}
Due date:              {task_list[4]} 
Task Complete?:        {task_list[5]}
Task decription:       
    {task_list[2]}
___________________________________________________ 
""")

# function to mark task as complete

def mark_as_complete(task_id):
        task_details = open('tasks.txt', 'r')
        replaced_content = ""
        for line in task_details:
            task_list = line.strip().split(",")
            if task_id == task_list[6]:
                new_line = line.lower().replace("no","Yes")
                print(f"""
Task {task_id} has been marked as complete.""")

            else:
                new_line = line
            replaced_content = replaced_content + new_line
        task_details.close()

        # code to write altered code back into txt file
        # and send user back to main menu

        write_details = open('tasks.txt','w')
        write_details.write(replaced_content)
        menu = menu_selector(username)
        menu_choice(menu)


def edit_date_or_assigned(task_id):
        time.sleep(1)
        user_or_date_edit = input("""

Press 'A' to change the assigned user.
Press 'D' to change the task due date.

Press '-1' to return to edit options.
        """)

        if user_or_date_edit.lower() == 'a':
            edit_assigned(task_id)


        elif user_or_date_edit.lower() == 'd':
            edit_date(task_id)

        
        elif user_or_date_edit == '-1':
            view_mine()
        else:
            print("Input not recognised")
            edit_date_or_assigned(task_id)


def edit_date(task_id):
    replacement_date = input(""""

    Enter the new due date for this task: """)

    task_details = open('tasks.txt', 'r')
    replaced_content = ""
    for line in task_details:
        task_list = line.strip().split(",")
        if task_id == task_list[6]:
            new_line = line.lower().replace(task_list[4],replacement_date)

            print(f"""
    Task {task_id}'s due date has been changed to {replacement_date}.
            """)

        else:
            new_line = line
        replaced_content = replaced_content + new_line
    task_details.close()
    write_details = open('tasks.txt','w')
    write_details.write(replaced_content)

def edit_assigned(task_id):
    replace_user = input(""""

Enter the name of the person you'd want to assign this task to:""")
    task_details = open('tasks.txt', 'r')
    replaced_content = ""
    for line in task_details:
        task_list = line.strip().split(",")
        if task_id == task_list[6]:
            new_line = line.lower().replace(task_list[0],replace_user)

            print(f"""
Task {task_id} has been assigned to {replace_user}.
            """)

        else:
            new_line = line
        replaced_content = replaced_content + new_line
    task_details.close()
    write_details = open('tasks.txt','w')
    write_details.write(replaced_content)


# function to edit task details of selected task

def edit_task(task_id):
    edit_choice = input("""

Press 'C' to make the task as complete.
Press 'E' to reassign user or change task due date.

Press '-1' to return to view tasks.
    """)
    
    if edit_choice.lower() == 'c':
        mark_as_complete(task_id)

    # code to edit tasks assigned user or due date
    
    elif edit_choice.lower() == 'e':
        edit_date_or_assigned(task_id)

    elif edit_choice.strip() == '-1':
        view_mine()
    else:
        print("""
        
        The input was not recognised - please try again
        
        """)
        time.sleep(2)
        edit_task(task_id)
    menu = menu_selector(username)
    menu_choice(menu)


def task_selector(username,task_id_list):
    #inital input
    task_id = input("""
    Enter the task ID to update a task
    (press '-1' to exit back to menu)
    """)

    if task_id == '-1':
        menu = menu_selector(username)
        menu_choice(menu)

    elif task_id in task_id_list:
        task_status = check_task_complete(task_id)
        if task_status == True:
            edit_task(task_id)
        else:
            print("That task has been completed and can no longer be editied")
            time.sleep(1)
            view_mine()
    else:
        print("Input not recognised please try again")
        time.sleep(1)
        view_mine()

def check_task_complete(task_id):
    task_details = open("tasks.txt", 'r')
    for line in task_details:
        task_list = line.strip().split(",")
        if task_id == task_list[6]:
            print(task_list[5])
            if task_list[5] == "yes":
                return False
            else:
                return True



#function to view user assigned tasks only

def view_mine():
    task_id_list = []
    with open('tasks.txt', 'r') as task_details:
        for line in task_details:
            task_list = line.strip().split(",")
            if username == task_list[0]:
                print(f"{username}, your task to complete:")
                print(f""" 
___________________________________________________
ID:{task_list[6]}
Task:                  {task_list[1]}
Date assigned:         {task_list[3]}
Due date:              {task_list[4]} 
Task Complete?:        {task_list[5]}
Task decription:       
    {task_list[2]}
___________________________________________________""")
                task_id_list.append(task_list[6])

    task_selector(username,task_id_list)

# function to show admin system statistics

def system_statistics():
    task_stats = ""
    user_stats = ""
    # if files exist run this block of code
    try:
        with open("task_overview.txt", "r") as task_overview:
            for line in task_overview:
                task_stats += line
        with open("user_overview.txt", "r") as task_overview:
            for line in task_overview:
                user_stats += line
        print(task_stats + user_stats)

    # if files don't exist then handle error with this block
    except FileNotFoundError:

        # create report files if they don't exist
        generate_report()

        # read newly created files
        with open("task_overview.txt", "r") as task_overview:
            for line in task_overview:
                task_stats += line
        with open("user_overview.txt", "r") as task_overview:
            for line in task_overview:
                user_stats += line

        #print output to console
        print(task_stats + user_stats)

# function to provide admin menu

def admin_menu():
    menu_options = ['r', 'a', 'va', 'vm', 'e', 'ds', 'gr']
    menu = input('''Select one of the following Options below:
    r  - registering a user
    a  - add task
    va - view all tasks
    vm - view my task
    gr - generate reports
    ds - display statistics  
    e  - Exit
    : ''').lower()

    while menu not in menu_options:
        print("You entered an invalid input, please try again!")
        time.sleep(1)

    menu = input('''Select one of the following Options below:
    r  - registering a user
    a  - add task
    va - view all tasks
    vm - view my task
    gr - generate reports
    ds - display statistics  
    e  - Exit
    : ''').lower()

    return menu


# function to provide standard menu (non admin)

def standard_menu():
    menu_options = ['r', 'a', 'va', 'vm', 'e', 's']
    menu = input('''Select one of the following Options below:
    r - Registering a user (admin only)
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()

    while menu not in menu_options:
        print("You entered an invalid input, please try again!")
        time.sleep(1)
        menu = input('''
    Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()
    
    return menu


def menu_selector(username):
    if username == "admin":
        return admin_menu()
    else:
        return standard_menu()



def get_task_details():
# declare counters and empty string
    task_detais_string, task_counter, complete_count, uncomplete_count, overdue_counter = "", 0, 0, 0, 0

# loop through all recorded tasks to create report
# add to counters if conditions are met

    with open('tasks.txt', 'r') as task_details:
        for line in task_details:
            task_counter += 1
            data = line.split(",")
            if data[5].lower() == "yes":
                complete_count += 1
            else:
                uncomplete_count += 1

            due_date = datetime.datetime.strptime(data[4], "%d/%m/%Y").date()
            today = datetime.date.today()
            if (today > due_date) and data[5].lower() == "no":
                overdue_counter += 1
            else:
                continue                
# store full string value which makes sence for user in report

    task_detais_string = f"""The total number of tasks that have been generated is {task_counter}.
The number of completed tasks is {complete_count}.
The number of uncompleted tasks is {uncomplete_count}.
The total number of tasks which havent been compelted and are over due is {overdue_counter}.
The percentage of tasks that are incomplete is {round(((uncomplete_count/task_counter)*100),2)}%.
The percentage of tasks that are overdue is {round(((overdue_counter/task_counter)*100),2)}%.
"""""

# close file and return string value

    task_details.close()
    return task_detais_string


# function to create report about all users

def get_user_details():
# declare counter variables
    users_report = ""
    number_of_users = 0
    task_counter = 0

# code to get count of total users
    with open('tasks.txt', 'r') as task_details:
        for line in task_details:
            task_counter += 1

    with open('user.txt', 'r') as user_details:

        user_details_str = ""
        for line in user_details:
            data = line.split(',')
            number_of_users += 1
            user = data[0]
            task_count = 0
            user_task_complete = 0
            user_tasks_outstanding = 0
            with open('tasks.txt', 'r') as task_details:
                over_due_count = 0
                for line in task_details:
                    tasks = line.split(',')
                    if tasks[0] == user:
                        task_count += 1
                        if tasks[5].lower() == "yes":
                            user_task_complete += 1
                        if tasks[5].lower() == 'no':
                            user_tasks_outstanding += 1

                        due_date = datetime.datetime.strptime(tasks[4], "%d/%m/%Y").date()
                        today = datetime.date.today()
                        if today > due_date:
                            if tasks[5].lower() == 'no':
                                over_due_count += 1
                try:
                    perc_tasks_complete = round(((user_task_complete/task_count)*100),2)
                except ZeroDivisionError:
                    perc_tasks_complete = 0
                    over_due_count = 0

                if task_count == 0:
                    tasks_left = 0
                    over_due_count = 0
                else:
                    tasks_left = round(((user_tasks_outstanding/task_count)*100),2)

                try:
                    over_due_count = round(((over_due_count/task_count)*100),2)

                except ZeroDivisionError:
                    over_due_count = 0

                new_line = f"""\n{user} has been assigned {task_count} tasks, accounting for {round(((task_count/task_counter)*100),2)}% of all tasks.
{user} has completed {perc_tasks_complete}% of tasks assigned to them.
{user} has {tasks_left}% of task assigned to them left to compelte.
{user} has {over_due_count}% of tasks assigned them which are overdue and not complete."""
                user_details_str = user_details_str + new_line
    
    users_report = f"""The total number of registered with Task_Manager is {number_of_users}.
Number of tasks that have been generated and tracked using Task_Manager is {task_counter}.
"""
    task_details.close()
    user_details.close()
    return users_report + user_details_str


# function to generate and write report files

def generate_report():
    # open files to write to

    task_overview = open('task_overview.txt', 'w')
    user_overview = open('user_overview.txt', 'w')
    # call functions and assign to variable

    task_details = get_task_details()
    user_details = get_user_details()

    #write function outputs to file

    task_overview.write(task_details)
    user_overview.write(user_details)

    # close files after writing

    task_overview.close()
    user_overview.close()

# function to create username and password dictionary - login

def get_users_details():
    username_and_passwords = {}
    with open('user.txt', 'r') as user_details:
        for line in user_details:
            data = line.split(",")
            username_and_passwords.update({data[0].strip(): data[1].strip()})
    user_details.close()
    return username_and_passwords

# function to check username and password against dictionary of users
# returns username - login

def enter_details(username_and_passwords):

    # username check
    username = input("Please enter your username: ")
    while username not in username_and_passwords.keys():
        print("User name not recognised")
        username = input("Please enter your username: ")
        continue

    # password check
    password = input("Please enter your password: ")
    while password != username_and_passwords[username]:
        print("The password you've entered is not correct")
        password = input("Please enter your password: ")
        continue
    return username

# function to exit system
def exit_system():
    print('Goodbye!!!')
    exit()

#  function to flow throw option choice from menu
def menu_choice(menu):
    if menu.lower() == 'r':
        reg_user(username)

    # code to allow user to add new tasks

    elif menu == 'a':
        add_task()

    # code to check all tasks in system

    elif menu == 'va':
        view_all()

    # code allows user to check their tasks only

    elif menu == 'vm':
        view_mine()

    #code to show admin system statistics
    elif menu == 'ds':
        system_statistics()
    
    elif menu == 'gr':
        generate_report()

    # exit out of the system
    elif menu == 'e':
        exit_system()

# ====Login Section====

username_and_passwords = get_users_details()

username = enter_details(username_and_passwords)

menu = menu_selector(username)

menu_choice(menu)
