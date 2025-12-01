# Database connection
import sqlite3

def connect_db():
    con = sqlite3.connect("notes-app.db")
    return con
    
def check_table():
    con = connect_db()
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    res.fetchone()
    print("Database connected and tables checked.")
    print(res.fetchone())
    con.close()
    
def insert_user(username, email, password):
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
    INSERT INTO user (username, email, password) VALUES (?, ?, ?)
    """, (username, email, password))
    con.commit()
    con.close()
    
