from tkinter import *
# import csv
import sqlite3
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

FONT_NAME = "Courier"
FONT_SIZE = None

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for n in range(randint(8, 10))]
    password_symbols = [choice(symbols) for n in range(randint(2, 4))]
    password_numbers = [choice(numbers) for n in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pass():
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(email) == 0 or len(password) == 3:
        messagebox.showinfo(title="Missing info", message="Please enter all info")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n Email: {email} "
                                                              f"\nPassword: {password}\nIs it ok to save?")
        if is_ok:
            try:
                connection = sqlite3.connect("data.db")
                cursor = connection.cursor()
                print("Successfully Connected to SQLite")

                sqlite3_query = f"""INSERT INTO data VALUES('{website}', '{email}', '{password}')"""

                cursor.execute(sqlite3_query)
                connection.commit()
                print("Successfully inserted data")
                cursor.close()

            except sqlite3.Error as error:
                print("Failed to insert data into sqlite3 table", error)

            finally:
                if connection:
                    connection.close()
                    print("The sqlite connection is closed")

    website_entry.delete(0, END)
    password_entry.delete(0,END)


# ---------------------------- UI SETUP ------------------------------- #
window =Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text='Website:')
website_label.grid(row=1, column=0)

email_username_label = Label(text='Email/Username:')
email_username_label.grid(row=2, column=0)

password_label = Label(text='Password:')
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry()
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
website_entry.focus()

email_username_entry = Entry()
email_username_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_username_entry.insert(0, "xyz@gmail.com")

password_entry = Entry()
password_entry.grid(row=3, column=1, sticky="EW")

# Buttons
gen_pass_button = Button(text='Generate password', command=gen_pass)
gen_pass_button.grid(row=3, column=2, sticky="EW")

add_button = Button(text='Add', width=35, command=save_pass)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")


window.mainloop()