import pymysql.cursors
from parses import mainParse

# -----------------------------------------
# Parsing and writing data to the database.
# -----------------------------------------

def main():
    tables = mainParse("url")

    #connect to mysql database

    connection = pymysql.connect(
        host='127.0.0.1',user='root',
        password='0000',db='our_users', 
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
        )

    try:
        with connection.cursor() as cursor:
            for table in tables:
                try:
                    
                    # create query (select) for mysql DB
                    listOfQuery = str(f'INSERT INTO item (title, type_transport,color,transmission,mileage,occasion,price,image,engine,note) '
                                      f'VALUES( "{table["title"]}","{table["type_transport"]}",'
                               f'"{table["color"]}","{table["transmission"]}","{table["mileage"]}","{table["occasion"]}",'
                               f'"{table["price"]}","{table["image"]}", "{table["engine"]}", "{table["note"]}")')

                    # add query 
                    cursor.execute(listOfQuery)

                    # save new changes
                    connection.commit()

                except:
                    continue

    finally:
        connection.close()


if __name__ == "__main__":
    main()
