import mysql.connector



def connect_mysql(host, user, password, database):

    mysql_db = mysql.connector.connect(
                host = host,
                user = user,
                passwd = password,
                database = database
            )
    return mysql_db


def fetch_all_titles(mysql_db):
    curr = mysql_db.cursor()
    curr.execute(""" SELECT title FROM books_tb """)
    result = curr.fetchall()
    return result

def books_between_dates(mysql_db, start_date, end_date):
    curr = mysql_db.cursor()
    curr.execute(f"""SELECT title 
                    FROM books_tb 
                    WHERE publishDate BETWEEN '{start_date}' AND '{end_date}' """)
    result = curr.fetchall()
    return result

def rank_titles(mysql_db):
    curr = mysql_db.cursor()
    curr.execute("""SELECT title, avgRating
                    FROM books_tb
                    ORDER BY avgRating DESC """)
    result = curr.fetchall()
    return result

#connecting database
mysqlDb = connect_mysql('localhost', 'root', '_placeholder_', 'goodreadsBooks')

for i in books_between_dates(mysqlDb, "1900-01-01", "1950-01-01"):
    print(i[0])

for i in rank_titles(mysqlDb):
    print(i[0])