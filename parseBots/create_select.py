import pymysql.cursors

# -----------------------------------------
# In this .py file, when the main function 
# is executed, we will receive a response 
# to a COMAND request, which we will enter customly, 
# according to different sorting or filtering.
# -----------------------------------------

def main(COMAND):
    # connect to mysql db
    connection = pymysql.connect(
        host='127.0.0.1',user='root',
        password='0000',db='our_users', 
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )
    # add connect to cursor
    mycursor = connection.cursor()

    # fulfillment of our request and returning the table
    mycursor.execute(COMAND)
    myresult = mycursor.fetchall()
    return myresult


# a test part of the code on which 
# you can check the correctness of a particular request
if __name__ == "__main__":
    myresult = main("SELECT * FROM item")
    for item in myresult:
        print(item["image"])
