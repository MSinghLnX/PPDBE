import psycopg2
import math
import getpass
import sys

# Receives input to establish database connection
def connect():
    try:
        defPort = "5432"
        localhost = "127.0.0.1"
        defDB = "postgres"
        print("Please enter your database information below: ")
        ht = input("Hostname (Default is localhost): ")
        db = input("Database (Default is postgres): ")
        usr = input("Username: ")
        pwd = getpass.getpass("Password: ")
        prt = input("Port (Default is 5432): ")
        if prt == "":
            prt = defPort
        if ht == "":
            ht = localhost
        if db == "":
            db = defDB

        print("Connecting ...")
    except KeyboardInterrupt:
        sys.exit("\nExiting PPDBE")

    # Check if input is valid, otherwise reenter credentials
    try:
        conn = psycopg2.connect(
                host = ht,
                database = db,
                user = usr,
                password = pwd,
                port = prt)
    except:
        print("Invalid inputs detected. Try again.")
        connect()
    print("Succesfully Connected!")
    return conn 

# Initialize cursor for database access
def cursorInit(connection):
    dbCursor = connection.cursor()
    return dbCursor

# Writes changes to database
def writeDB(connection):
    cond = input("Would you like to write changes to the database? [y/n]: ")
    if cond == 'y':
        print("Writing changes")
        connection.commit()
    elif cond == 'n':
        print("No changes made.")
    else:
        print("Invalid option. Try again")
        writeDB(connection)
    return 0

# Function to create table in current database
def createTable(cursor, connection):
    print("Initializing Table")
    name = input("Name for table?: ")
    colNum = input("How many columns?: ")
    print("WIP")
    return 0
    
    cursor.execute()
    writeDB(connection)
    return 0

# Handling manual SQL requests
def manualSQL(cursor, connection):
    try: 
        sqlIn = input("Type your SQL input below:\n")
        while sqlIn != "exit":
            try:
                cursor.execute(sqlIn)
                writeDB(connection)
            except:
                print("SQL input was invalid, try again")
                manualSQL(cursor, connection)
            return 0
    except KeyboardInterrupt:
            print("\nExiting Manual Mode")
            return 0

# This will be used for simple assignments that don't need much customization or interaction
def demo(cursor, connection):
    cursor.execute('''CREATE TABLE students(hofstra_ID VARCHAR (100) PRIMARY KEY, name VARCHAR (100));''')
    cursor.execute('''CREATE TABLE grades(prim SERIAL PRIMARY KEY, hofstra_ID VARCHAR (100), course VARCHAR (100), grade INTEGER);''')
    cursor.execute("INSERT INTO students(hofstra_ID, name) VALUES('h0','Python')")
    cursor.execute("INSERT INTO students(hofstra_ID, name) VALUES('h1','Java')")
    cursor.execute("INSERT INTO grades(hofstra_ID, course, grade) VALUES('h0','CSC123','90')")
    cursor.execute("INSERT INTO grades(hofstra_ID, course, grade) VALUES('h0','CSC112','86')")
    cursor.execute("INSERT INTO grades(hofstra_ID, course, grade) VALUES('h0','CSC161','79')")
    cursor.execute("INSERT INTO grades(hofstra_ID, course, grade) VALUES('h1','CSC123','84')")
    cursor.execute("INSERT INTO grades(hofstra_ID, course, grade) VALUES('h1','CSC024','87')")
    cursor.execute("INSERT INTO grades(hofstra_ID, course, grade) VALUES('h1','CSC190','76')")
    cursor.execute("SELECT grades.hofstra_ID, ROUND(AVG(grade)), students.name FROM grades JOIN students ON students.hofstra_ID = grades.hofstra_ID GROUP BY grades.hofstra_ID, students.name")
    print("Grades Table")
    print(cursor.fetchall())
    writeDB(connection)
    #connection.commit()

# Main Function
def main():
    option = "3"
    print("Hello, welcome to PPDBE!")
    connMan = connect()

    # Establish cursor to act on database
    dbCur = cursorInit(connMan)
    demoCond = False # Make sure demo is only run once, otherwise crash
    try:
        while option != 0:
            print("Options:\n 1. Create Table\n 2. See Table\n 3. Manual \n 4. Demo Mode\n Press Ctrl + C to exit")
            option = input("Choose option here: ")
            if option == "1":
                createTable(dbCur, connMan)
            elif option == "2":
                try:
                    print(dbCur.fetchall())
                except: 
                    print("The database is empty!")
            elif option == "3":
                print("Welcome to the deep end! Ctrl + C to exit")
                manualSQL(dbCur, connMan)
            elif option == "4":
                if demoCond == True:
                    print("Demo already executed. Continuing loop.")
                    continue
                print("Demo initiating")
                demo(dbCur, connMan)
                print("Demo Complete!")
                demoCond = True
            else:
                print("Invalid option.")
    except KeyboardInterrupt:
        print("\nClosing connections...")
        dbCur.close()
        connMan.close()
        print("Goodbye!")
        return 0
    
    return 0

main()
