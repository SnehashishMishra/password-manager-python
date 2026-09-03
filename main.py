from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip, re

# --------------------------------- VALIDATION ---------------------------------- #
def is_valid_domain(domain):
    pattern = r"^(?:https?://)?(?:www\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:[/:?#].*)?$"
    return re.match(pattern, domain.strip()) is not None

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\];'`~]", password):
        return False

    return True

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate_password():
    password_entry.delete(0, END)

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get()

    if website == "" or email == "" or password == "":
        messagebox.showerror("Oops", "Please don't leave any fields empty")
        return

    if not is_valid_domain(website):
        messagebox.showerror(
            "Invalid Website",
            "Please enter a valid domain name.\n\n"
            "Example:\n"
            "www.example.com"
        )
        return

    if not is_valid_password(password):
        messagebox.showerror(
            "Invalid Password",
            "Password must contain:\n"
            "• At least 8 characters\n"
            "• At least one uppercase letter\n"
            "• At least one lowercase letter\n"
            "• At least one number\n"
            "• At least one special character"
        )
        return

    is_ok = messagebox.askokcancel(
        website,
        f"These are the details entered:\n\n"
        f"Email/Username: {email}\n"
        f"Password: {password}\n\n"
        f"Is it ok to save?"
    )

    if not is_ok:
        return

    with open("data.txt", "a") as file:
        file.write(f"{website} | {email} | {password}\n")

    website_entry.delete(0, END)
    password_entry.delete(0, END)

    pyperclip.copy(password)

# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Password Manager")
# root.geometry("400x400")
root.resizable(False, False)
root.config(padx=40, pady=40)

# Logo Canvas
canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="./assets/logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# Label
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entry
website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
email_entry = Entry(width=35)
email_entry.insert(0, "emailid@example.com")
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="EW")

# Button
password_generate_button = Button(text="Generate Password", command=generate_password)
password_generate_button.grid(row=3, column=2, sticky="EW")
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

root.mainloop()
