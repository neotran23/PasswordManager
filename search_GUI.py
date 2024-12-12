
import json
from tkinter import *
from tkinter import messagebox, END
import random

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!@#$%&*'

    password_list = (
        [random.choice(letters) for _ in range(8)] +
        [random.choice(numbers) for _ in range(2)] +
        [random.choice(symbols) for _ in range(2)]
    )
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)  # Clear the entry field
    password_entry.insert(0, password)  # Insert the generated password into the entry field

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get().strip().lower()
    link = link_entry.get().strip().lower()
    email = email_entry.get().strip().lower()
    password = password_entry.get()
    new_data = {
        website: {
            "link": link,
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(link) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning", message="Please fill out all fields!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            # If the file does not exist, create a new dictionary
            data = {}
        except json.JSONDecodeError:
            # If the file is empty or contains invalid JSON, create an empty dictionary
            data = {}
            # Check if the website already exists in the data
        if website in data:
            # Check if the email matches the existing data for this website
            existing_email = data[website]["email"]
            if existing_email != email:
                messagebox.showinfo(title="Info",
                                    message="A different email is associated with this website. A new entry will be created.")
            else:
                messagebox.showwarning(title="Warning", message="This website and email combination already exists!")
                return
        # Updating old data with new data
        data.update(new_data)

        with open("data.json", "w") as data_file:
            # Saving the updated data back to the file
            json.dump(data, data_file, indent=4)

        website_entry.delete(0, END)
        link_entry.delete(0,END)
        password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().strip().lower()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    except json.JSONDecodeError:
        messagebox.showerror(title="Error", message="No data found in the file.")
    else:
        if website in data:
            # Check if the 'link' key exists
            link = data[website].get("link", "No link available")  # Default message if no link
            email = data[website].get("email", "No email available")  # Default message if no email
            password = data[website].get("password", "No password available")  # Default message if no password
            messagebox.showinfo(title=website, message=f"Link: {link}\nEmail: {email}\nPassword: {password}")
        else:
            messagebox.showwarning(title="Warning", message=f"No details for the website '{website}' exists")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, width=300, height=300, bg=YELLOW, highlightthickness=0)

# Canvas for the logo Image
canvas = Canvas(width=200, height=200, bg=YELLOW, highlightthickness=0)
logo_img = PhotoImage(file=r"D:\NHAT\Python_Project_Study\Day_29_start\PasswordSearch\logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Website Label and Entry
website_label = Label(text="Website:", font=(FONT_NAME, 12), fg="black", bg=YELLOW)
website_label.grid(column=0, row=1)
website_entry = Entry(font=(FONT_NAME, 12), width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()  # Automatically focus on the website entry

# Link Label and Entry
link_label = Label(text="Link:", font=(FONT_NAME, 12), fg="black", bg=YELLOW)
link_label.grid(column=0, row=2)
link_entry = Entry(font=(FONT_NAME, 12), width=36)
link_entry.grid(column=1, row=2, columnspan=2)

# Search Button
search_button = Button(text="Search", command=find_password, font=(FONT_NAME, 10, "bold"), width=18)
search_button.grid(column=2, row=1)

# Email/Username Label and Entry
email_label = Label(text="Email/Username:", font=(FONT_NAME, 12), fg="black", bg=YELLOW)
email_label.grid(column=0, row=3)
email_entry = Entry(font=(FONT_NAME, 12), width=36)
email_entry.grid(column=1, row=3, columnspan=2)

# Password Label and Entry
password_label = Label(text="Password:", font=(FONT_NAME, 12), fg="black", bg=YELLOW)
password_label.grid(column=0, row=4)
password_entry = Entry(font=(FONT_NAME, 12), width=21)
password_entry.grid(column=1, row=4)

# Generate Password Button
generate_button = Button(text="Generate Password", command=generate_password, font=(FONT_NAME, 10, "bold"))
generate_button.grid(column=2, row=4)

# Add Button
add_button = Button(text="Add", command=save_password, font=(FONT_NAME, 12, "bold"), width=36)
add_button.grid(column=1, row=5, columnspan=2)

window.mainloop()
