import json
from tkinter import *
from tkinter import messagebox, END
import random
import os
from unittest.mock import right

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

    if len(website) == 0 or len(link) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning", message="Please fill out all fields!")
        return

    new_entry = {
        "link": link,
        "email": email,
        "password": password
    }

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

    if website in data:
        # Check if the email already exists for this website
        existing_entries = data[website]
        if isinstance(existing_entries, list):
            for entry in existing_entries:
                if entry['email'] == email:
                    messagebox.showwarning(title="Warning", message="This website and email combination already exists!")
                    return
            # If no matching email, append new entry
            existing_entries.append(new_entry)
        else:
            # If existing entry is not a list, convert it to a list
            if existing_entries['email'] == email:
                messagebox.showwarning(title="Warning", message="This website and email combination already exists!")
                return
            else:
                data[website] = [existing_entries, new_entry]  # Convert to list
    else:
        # If the website doesn't exist, create a new entry
        data[website] = [new_entry]

    with open("data.json", "w") as data_file:
        # Saving the updated data back to the file
        json.dump(data, data_file, indent=4)

    # Clear the input fields after saving
    website_entry.delete(0, END)
    link_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().strip().lower()
    email = email_entry.get().strip().lower()  # Get email from input
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    except json.JSONDecodeError:
        messagebox.showerror(title="Error", message="No data found in the file.")
    else:
        if website in data:
            entries = data[website]
            found = False  # Flag to check if any entry was found
            if isinstance(entries, list):
                for entry in entries:
                    # Check for a specific email, partial email, or show all
                    if not email or email in entry['email']:  # Check if email is empty or is in entry's email
                        link = entry.get("link", "No link available")
                        email_found = entry.get("email", "No email available")
                        password = entry.get("password", "No password available")
                        show_custom_popup(website, link, email_found, password)
                        found = True
                if not found and email:  # If email is provided but no matches were found
                    messagebox.showwarning(title="Warning", message="No matching email found for this website.")
            else:
                # Prepare message for a single entry
                link = entries.get("link", "No link available")
                email_found = entries.get("email", "No email available")
                password = entries.get("password", "No password available")
                show_custom_popup(website, link, email_found, password)
        else:
            messagebox.showwarning(title="Warning", message=f"No details for the website '{website}' exists")

# ---------------------------- CUSTOM POPUP WINDOW ------------------------------- #
def show_custom_popup(website, link, email, password):
    popup = Toplevel(window)
    popup.title(website)
    popup.config(padx=10, pady=10, bg=YELLOW)

    # Create Labels and Entry for displaying details
    link_label = Label(popup, text="Link:", bg=YELLOW)
    link_label.grid(row=0, column=0, sticky='e')
    link_entry = Entry(popup, width=40)
    link_entry.grid(row=0, column=1)
    link_entry.insert(0, link)
    link_entry.config(state='readonly')  # Make it read-only for copying

    email_label = Label(popup, text="Email:", bg=YELLOW)
    email_label.grid(row=1, column=0, sticky='e')
    email_entry = Entry(popup, width=40)
    email_entry.grid(row=1, column=1)
    email_entry.insert(0, email)
    email_entry.config(state='readonly')  # Make it read-only for copying

    password_label = Label(popup, text="Password:", bg=YELLOW)
    password_label.grid(row=2, column=0, sticky='e')
    password_entry = Entry(popup, width=40)
    password_entry.grid(row=2, column=1)
    password_entry.insert(0, password)
    password_entry.config(state='readonly')  # Make it read-only for copying

    # Add a button to close the popup
    close_button = Button(popup, text="Close", command=popup.destroy)
    close_button.grid(row=3, columnspan=2)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40, width=300, height=300, bg=YELLOW, highlightthickness=0)

# Canvas for the logo Image
canvas = Canvas(width=200, height=200, bg=YELLOW, highlightthickness=0)

# Get the current script directory
current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "logo.png")

# Load the image using the relative path
try:
    logo_img = PhotoImage(file=logo_path)
    canvas.create_image(100, 100, image=logo_img)
except TclError:
    messagebox.showerror("Error", f"Unable to load logo.png from {logo_path}")

canvas.grid(column=1, row=0)

# Website Label and Entry
website_label = Label(text="WebsiteName:", font=(FONT_NAME, 12), fg="black", bg=YELLOW,)
website_label.grid(column=0, row=1, sticky="e")
website_entry = Entry(font=(FONT_NAME, 12), width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()  # Automatically focus on the website entry

# Link Label and Entry
link_label = Label(text="Link:", font=(FONT_NAME, 12), fg="black", bg=YELLOW,)
link_label.grid(column=0, row=2, sticky="e")
link_entry = Entry(font=(FONT_NAME, 12), width=37)
link_entry.grid(column=1, row=2, columnspan=2)

# Search Button
search_button = Button(text="Search", command=find_password, font=(FONT_NAME, 10, "bold"), width=18)
search_button.grid(column=2, row=1)

# Email/Username Label and Entry
email_label = Label(text="Email/Username:", font=(FONT_NAME, 12), fg="black", bg=YELLOW)
email_label.grid(column=0, row=3, sticky="e")
email_entry = Entry(font=(FONT_NAME, 12), width=37)
email_entry.grid(column=1, row=3, columnspan=2)

# Password Label and Entry
password_label = Label(text="Password:", font=(FONT_NAME, 12), fg="black", bg=YELLOW)
password_label.grid(column=0, row=4, sticky="e")
password_entry = Entry(font=(FONT_NAME, 12), width=21)
password_entry.grid(column=1, row=4)

# Generate Password Button
generate_button = Button(text="Generate Password", command=generate_password, font=(FONT_NAME, 10, "bold"))
generate_button.grid(column=2, row=4)

# Add Button
add_button = Button(text="Add", command=save_password, font=(FONT_NAME, 12, "bold"), width=36)
add_button.grid(column=1, row=5, columnspan=2)

window.mainloop()
