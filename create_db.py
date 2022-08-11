import mysql.connector

# -------------------------------------
# This is a file that runs only once. 
# In order to create a database with 
# the appropriate connection parameters 
# (user, root, host)
# -------------------------------------

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="0000",
)

my_cursor = mydb.cursor()

# ---------------------------------------------------------------
# after creating the database we don't need this command anymore
#
# my_cursor.execute("CREATE DATABASE our_users")
# ---------------------------------------------------------------

my_cursor.execute("CREATE DATABASE our_users")

my_cursor.execute("SHOW DATABASES")

# test command

for db in my_cursor:
    print(db)