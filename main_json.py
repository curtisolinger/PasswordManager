from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import re

FONT_NAME = "Courier"
FONT_SIZE = None

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def gen_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
               'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
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
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 3:
        messagebox.showinfo(title="Missing info", message="Please enter all info")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH FUNCTION ------------------------------- #


def search():
    search_query = website_entry.get()
    search_results = []
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        print("File not found")
    else:
        for key, value in data.items():
            if len(re.findall(search_query, key)) > 0:
                search_results.append(key)
        if len(search_results) == 1:
            key = search_results[0]
            pyperclip.copy(data[key]['password'])
            messagebox.showinfo(title=f"{search_query}", message=f"Website: {key}\n"
                                f"Email: {data[key]['email']}\nPassword: {data[key]['password']}")
        else:
            print("Multiple search results found: ", search_results)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
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
# Changed column span from 2 to 1
website_entry.grid(row=1, column=1, columnspan=1, sticky="EW")
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

search_button = Button(text='Search', command=search)
search_button.grid(row=1, column=2, sticky="EW")

window.mainloop()
