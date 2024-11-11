import sqlite3

connection = sqlite3.connect("initiate_db.db")
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
)
''')
connection.commit()

#for i in range(6):
    #title = 'Product' + str(i)
   # description = 'desctiption' + str(i)
   # price = 100 * i
  ##                 (title, description, price))

#connection.commit()


def get_all_products():
    get_products = cursor.execute('SELECT * from Products')
    products = cursor.fetchall()
    return products



prod = get_all_products()

connection.close()

connection = sqlite3.connect("initiate_db.db")
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
)
''')
connection.commit()
connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect("initiate_db.db")
    cursor = connection.cursor()
    balance = 1000

    cursor.execute(f"INSERT INTO USERS (username, email, age, balance) values (?,?,?,?)",
                  (username, email, age, balance))
    connection.commit()
    connection.close()





def is_included(username):
    connection = sqlite3.connect("initiate_db.db")
    cursor = connection.cursor()
    x = cursor.execute("SELECT * from Users WHERE username = ?", (username,))

    if x.fetchone() is None:
        connection.close()
        return False
    else:
        connection.close()
        return True




