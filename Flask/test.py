from cgitb import reset
from operator import rshift
import sqlite3 as sql

#Plot graph imports
import datetime as DT
import matplotlib.pyplot as plt

#USER INFO
def create_users_info():
    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")

    #Create table
    #username + email (unique) + password + icon_photo
    conn.execute("""CREATE TABLE user (username TEXT, email TEXT PRIMARY KEY, password TEXT, icon_photo TEXT)""")
    cur = conn.cursor()
    print("table created")
    
    #DEMO user
    insert_query = """INSERT INTO user (username, email, password, icon_photo)
                                       VALUES (?,?,?,?)"""
    cur.execute(insert_query, ("imcoolthanks", "queena1234@gmail.com", "1234", "/static/Assets/user_icons/default.jpg"))
    print("user added")

    conn.commit()

    conn.close()

def login(email, password):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    try:
        query = 'SELECT password FROM user WHERE email = ?'
        cur.execute(query, (email,))
    except:
        print("Invalid Email Address.")

    true_password = cur.fetchall()[0][0]

    if password == true_password:
        print("Logged in")
    else:
        print("Wrong Password")

    conn.close()

def sign_up(username, email, password):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()
    
    insert_query = """INSERT INTO user (username, email, password, icon_photo)
                                       VALUES (?,?,?,?)"""
    cur.execute(insert_query, (username, email, password, "/static/Assets/user_icons/default.jpg"))
    print("user added")

    conn.commit()
    conn.close()

#BLOCKED WEBSITE
def create_blocked_website():
    #blocked_website(email,seq_no,url)
    #select url from blocked_website where email = ?;

    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")

    #Create table
    #email,seq_no,url
    conn.execute("""CREATE TABLE blocked_website (email TEXT, url TEXT )""")
    print("table created")

    #DEMO 
    cur = conn.cursor()
    insert_query = """INSERT INTO blocked_website (email, url)
                                       VALUES (?,?)"""
    cur.execute(insert_query, ("queena1234@gmail.com", "https://www.youtube.com/"))
    print("user added")

    conn.commit()

    conn.close()

    print("Loading completed")
#return list of all blocked website
def get_blocked_website_list(email):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    try:
        query = 'SELECT url FROM blocked_website WHERE email = ?'
        cur.execute(query, (email,))
    except:
        print("Invalid Email Address.")

    rows = cur.fetchall()
    url_list = []

    for i in rows:
        url_list.append(i[0])

    conn.close()

    return url_list

def add_blocked_website(email, url):
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    insert_query = """INSERT INTO blocked_website (email, url)
                                       VALUES (?,?)"""
    cur.execute(insert_query, (email, url))
    conn.commit()

    conn.close()

def remove_blocked_website(email, url):
    
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    delete_query = "DELETE FROM blocked_website WHERE email = ? and url = ?"
    cur.execute(delete_query, (email, url))
    conn.commit()

    conn.close()

#FOCUS TIME
def create_focus_time():
    #focus_time(email,days_ago,hours)
    #select url from blocked_website where email = ?;

    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")

    #Create table
    #email, days_ago, hours
    conn.execute("""CREATE TABLE focus_time (email TEXT, days_ago INTEGER, hours INTEGER )""")
    print("table created")

    #DEMO
    cur = conn.cursor()
    insert_query = """INSERT INTO focus_time (email, days_ago, hours)
                                       VALUES (?,?,?)"""
    for i in range(7):                                   
        cur.execute(insert_query, ("queena1234@gmail.com", i, i))
    print("user added")

    conn.commit()
    conn.close()
#Update Focus time at end of day !!!CHANGE
def insert_focus_time(email, today_hours):
    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #find the one thats a week ago and update that value
    query = "UPDATE focus_time SET hours = "+str(today_hours)+" where email = ? and days_ago = 0"
    cur.execute(query, (email, ))

    conn.commit()
    conn.close()

#execute when 12am
def update_all_focus_time():
    #Create database file/connect to it
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #all +1
    query = "UPDATE focus_time SET days_ago = days_ago + 1"
    cur.execute(query)

    query = "update focus_time set days_ago = REPLACE(days_ago, 7, 0)"
    cur.execute(query)

    #find the one thats a week ago and update that value
    query = "UPDATE focus_time SET hours = 0 where days_ago = 0"
    cur.execute(query)

    conn.commit()
    conn.close()

#graph
def graph(email):    
    today = DT.date.today()

    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    #get username
    query = 'SELECT username FROM user WHERE email = ?'
    cur.execute(query, (email,))
    username = cur.fetchall()[0][0]

    #get focus_time
    query = 'SELECT hours FROM focus_time WHERE email = ?'
    cur.execute(query, (email,))
    rows = cur.fetchall()
    focus_time = []

    for i in rows:
        focus_time.append(i[0])

    conn.close()

    #Get x-axis data
    days = []
    for i in range(7):
        d = today - DT.timedelta(days=(6-i))
        days.append(d.strftime("%m/%d"))

    #Plot average line
    average = sum(focus_time) / len(focus_time)

    #Plot the 2 graphs
    plt.plot(days, focus_time)
    plt.axhline(y=average, color='r', linestyle='--')

    #Graph settings
    plt.axis([0, 6, 0, max(focus_time)+1]) #set axis
    plt.xlabel('Date')
    plt.ylabel('Number of hours focusing')
    plt.title('Past 7 Days Stats')

    #Save Graph
    plt.savefig('Flask/static/Assets/graphs/'+username+'.png')


#USED FOR DEBUGGING
def list_all():
    conn = sql.connect("Flask/static/Databases/database.db")
    cur = conn.cursor()

    tables = ["user", "blocked_website", "focus_time"]

    for t in tables:
        print(t+":")
        cur.execute("SELECT * FROM "+t)

        rows = cur.fetchall()

        for row in rows:
            print(row)

        print("\n")

#Delete and restart with basic DEMOs
def reset_database():
    create_blocked_website()
    create_focus_time()
    create_users_info()
    list_all()
