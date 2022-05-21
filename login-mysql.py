'''
REQUISITOS:
* XAMPP
* mysql-connector-python

source
* Center window - https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
* info, warning window - https://www.geeksforgeeks.org/python-tkinter-messagebox-widget/
* tomato icon - https://icon-icons.com/icon/tomato-vegetables-vegetable-food-agriculture-fruit/220780
'''

import tkinter as tk
from tkinter import messagebox
import mysql.connector

# mysql

connection = mysql.connector.connect(host="localhost", user="root", password="")
cursor = connection.cursor()
db = "lista8_rivas"
table_login = "login"

# fn
def db_login_add():
    login = login_txt_login.get()
    passw = login_txt_pass.get()

    if not login or not passw:
         messagebox.showerror("Invalid login", "Login credentials can't be empty!")
         return

    # insert default login if not exists
    cursor.execute("INSERT IGNORE INTO %s (user, pass) VALUES ('%s','%s')"%(table_login,login,passw))
    connection.commit()
    print(cursor.fetchall())
    messagebox.showinfo("Login","New login created: user: %s, pass: %s"%(login,passw))

def db_login_check():
    cursor.execute("SELECT * from %s WHERE user = '%s' and pass = '%s'"%(table_login,login_txt_login.get(),login_txt_pass.get()))
    if cursor.fetchall():
         messagebox.showinfo("Login","Login successfull")
    else:
         messagebox.showerror("Error", "Login incorrect!")

# init
cursor.execute("create database if not exists %s" % db)
cursor.fetchall()

cursor.execute("use %s" % db)
cursor.fetchall()

# create login table
cursor.execute(" \
CREATE TABLE IF NOT EXISTS %s( \
    id int PRIMARY KEY AUTO_INCREMENT, \
    user varchar(40) UNIQUE KEY, \
    pass varchar(30) \
) \
" % table_login)
print(cursor.fetchall())

ret = cursor.fetchall()
print(len(ret), bool(ret))

# tkinter

# window login

win_login = tk.Tk()
win_login.eval('tk::PlaceWindow . center')

win_login.geometry("300x250")
win_login.minsize(300, 250)
win_login.title("Login")
win_login.iconbitmap("tomato.ico")

win_login.grid_columnconfigure(0, weight=0)
win_login.grid_columnconfigure(1, weight=0)
win_login.grid_columnconfigure(2, weight=0)
win_login.grid_columnconfigure(3, weight=1)

win_login.grid_rowconfigure(0, weight=0)
win_login.grid_rowconfigure(1, weight=0)
win_login.grid_rowconfigure(2, weight=0)

login_label_login = tk.Label(
    win_login,
    text="Login",
)
login_label_login.grid(
    padx=10,
    pady=5,
    row=0,
    column=0,
)

login_txt_login = tk.Entry(
    win_login,
)
login_txt_login.grid(
    padx=10,
    pady=5,
    row=0,
    column=1,
    sticky="ew",
    columnspan=3,
)

login_label_pass = tk.Label(
    win_login,
    text="Password",
)
login_label_pass.grid(
    padx=10,
    pady=5,
    row=1,
    column=0,
)

login_txt_pass = tk.Entry(
    win_login,
)
login_txt_pass.grid(
    padx=10,
    pady=5,
    row=1,
    column=1,
    sticky="ew",
    columnspan=3,
)

login_login = tk.Button(
    win_login,
    text="Login",
    command=db_login_check,
)
login_login.grid(
    padx=10,
    pady=5,
    row=2,
    column=0,
)
login_new = tk.Button(
    win_login,
    text="New account",
    command=db_login_add,
)
login_new.grid(
    padx=10,
    pady=5,
    row=2,
    column=1,
)

win_login.mainloop()
