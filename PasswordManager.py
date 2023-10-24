import sys
import sqlite3
import secrets
import string

def start_program():
    print("***************Paswordmanager V2.0***************")
    conn2 = sqlite3.connect('start_password.db')
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT mainpassword FROM start_table")
    password = cursor2.fetchone()

    if password is not None:
        mainpassword = password[0]
        startpassword = input("Please enter password: ")
        if startpassword == mainpassword:
            print("Acess graunted!")
            selection()
        else:
            print("Acess denied!")
    else:
        mainpassword = None
        if mainpassword is None:
            mainpassword = input("Please create a password for the password manager: ")
            print("Password created your login password is: " + mainpassword)
            cursor2.execute("INSERT INTO start_table (mainpassword) VALUES (?)", (mainpassword,))
            conn2.commit()
            
    conn2.commit()
    conn2.close()
            
def selection():
    while True:
        userselection = input("Do you want to \n 1) Add username and password \n 2) Delete application \n 3) Find username and password \n 4) Display all usernames and passwords \n 5) Exit program \n: ")
        match userselection:
            case '1':
                add()
            case '3':
                find()
            case '2':
                tablename = 'passwords_table'
                delete(tablename)
            case '4':
                displayall()
            case'5':
                sys.exit()

def add():
    application = input("what is the application or website: ")
    username = input("what is the username: ")
    randorno = input("Would you like to create a random password: Y/N \n").upper()
    match randorno:
        case 'Y':
            password = ""
            characters = string.ascii_letters + string.digits + string.punctuation
            for i in range(11):
                 password += secrets.choice(characters) 
            print("this is your password: " + password)
        case 'N':
            password = input("what is the password: ")
        case _:
            print("Error invalid choice.")
            selection()
    conn = sqlite3.connect('spassword_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords_table (application, username, password) VALUES (?, ?, ?)", (application, username, password))
    conn.commit()
    cursor.close()
    conn.close()
    print("Username and password sucessfully added.")
   

def delete(table_name):
    application_to_remove = input("What application or website would you like to remove: ")
    conn = sqlite3.connect('spassword_database.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE application=?", (application_to_remove,))
    if cursor.rowcount > 0:
        print(f"Removed '{application_to_remove}' from '{table_name}'")
        conn.commit()
    else:
        print(f"Application '{application_to_remove}' not found in '{table_name}'")
    conn.close()
   

def find():
    application_name = input("what application or website are you looking for: ")
    conn = sqlite3.connect('spassword_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords_table WHERE application=?",(application_name,))
    data = cursor.fetchall()
    if data:
        for row in data:
            print("Application:", row[1])
            print("Username:", row[2])
            print("Password:", row[3])
    else:
        print("Application not found.")
    cursor.close()
    conn.close()

def displayall():
    conn = sqlite3.connect('spassword_database.db')
    cursor = conn.cursor()
    cursor.execute("Select * from passwords_table")
    record = cursor.fetchall()
    if not record:
        print("No records found.")
    else:
        for i in record:
            print("Application:", i[1])
            print("Username:", i[2])
            print("Password:", i[3])
            print()

conn = sqlite3.connect('spassword_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS passwords_table (
    id TEXT PRIMARY KEY,
    application TEXT,
    username TEXT,
    password TEXT
)''')

conn.commit()
conn.close()
conn2 = sqlite3.connect('start_password.db')
cursor2 = conn2.cursor()
cursor2.execute('''create table if not exists start_table(
    id text primary key,
    mainpassword text
)''')

conn2.commit()
conn2.close()

start_program()
