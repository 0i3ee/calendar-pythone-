import customtkinter as ctk
import tkinter as tk
import subprocess
import mysql.connector
from mysql.connector import errorcode
import tkinter.messagebox
from connect import connect, close_connection, get_cursor,close_cursor

conn = connect()
cursor = get_cursor(conn)

def clear_entries():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    gender_var.set("Male")
    entry_email.delete(0, tk.END)
    region_dropdown.set("")

def register():
    try:
        # Get values from the form
        username = entry_username.get()
        password = entry_password.get()
        gender = gender_var.get()
        email = entry_email.get()
        region = region_dropdown.get()

        # Validate gender and region values
        valid_genders = {'Male', 'Female'}
        valid_regions = {'Laos', 'Thai'}

        if gender not in valid_genders or region not in valid_regions:
            raise ValueError("Invalid gender or region value")

        # Check if the username already exists
        check_query = "SELECT * FROM users WHERE Username = %s"
        cursor.execute(check_query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            tkinter.messagebox.showerror(title="Registration Error", message="Username already exists. Please choose a different username.")
            return  # Stop the registration process if the username already exists

        # Insert data into the 'users' table
        insert_query = "INSERT INTO users (Username, Password, Gender, Email, Region) VALUES (%s, %s, %s, %s, %s)"
        data = (username, password, gender, email, region)

        cursor.execute(insert_query, data)

        # Commit the changes
        conn.commit()

        # Close the connection
        close_cursor(cursor)
        close_connection(conn)

        # Inform the user about successful registration
        tkinter.messagebox.showinfo(title="Registration Successful", message="You have successfully registered!")

        clear_entries()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied, check your username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: The specified database does not exist.")
        else:
            print(f"Error: {err}")

        # Print the values that caused the error for debugging
        print(f"Failed values: {username}, {password}, {gender}, {email}, {region}")

        # You can also display an error message to the user if needed
        tkinter.messagebox.showerror(title="Registration Error", message=f"Error: {err}")
    except ValueError as e:
        # Handle invalid gender or region values
        tkinter.messagebox.showerror(title="Registration Error", message=str(e))

def login():
    try:
        # Close the registration form
        app.destroy()

        # Open the new login form
        subprocess.run(["python", "login.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

app = ctk.CTk()
app.title("Registration Form")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
center_x = int((screen_width - 400) / 2)  # Adjust 400 as per your form's width
center_y = int((screen_height - 300) / 2)  # Adjust 300 as per your form's height
# Create the main window
app.geometry(f"400x300+{center_x}+{center_y}")




# Create labels and entry widgets for username, password, email
label_username = ctk.CTkLabel(app, text="Username:")
label_username.grid(row=0, column=0, padx=5, pady=5, sticky="e")

entry_username = ctk.CTkEntry(app)
entry_username.grid(row=0, column=1, padx=5, pady=5, sticky="w")

label_password = ctk.CTkLabel(app, text="Password:")
label_password.grid(row=1, column=0, padx=5, pady=5, sticky="e")

entry_password = ctk.CTkEntry(app, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5, sticky="w")

label_gender = ctk.CTkLabel(app, text="Gender:")
label_gender.grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Create a variable to store the selected gender
gender_var = tk.StringVar()
gender_var.set("Male")

# Create radio buttons for gender
radio_male = ctk.CTkRadioButton(app, text="Male", variable=gender_var, value="Male")
radio_male.grid(row=2, column=1, padx=5, pady=5, sticky="w")

radio_female = ctk.CTkRadioButton(app, text="Female", variable=gender_var, value="Female")
radio_female.grid(row=2, column=2, padx=5, pady=5, sticky="w")

label_email = ctk.CTkLabel(app, text="Email:")
label_email.grid(row=3, column=0, padx=5, pady=5, sticky="e")

entry_email = ctk.CTkEntry(app)
entry_email.grid(row=3, column=1, padx=5, pady=5, sticky="w")

label_region = ctk.CTkLabel(app, text="Region:")
label_region.grid(row=4, column=0, padx=5, pady=5, sticky="e")

# Sample list of regions (replace it with your own list)
regions = ["Laos", "Thai"]

# Create a dropdown list for regions
region_dropdown = ctk.CTkComboBox(app, values=regions, state="readonly")
region_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="w")

# Create a button to perform registration
register_button = ctk.CTkButton(app, text="Register", command=register)
register_button.grid(row=5, column=0, columnspan=2, pady=5)

# Create a button to perform login
login_button = ctk.CTkButton(app, text="Login", command=login)
login_button.grid(row=6, column=0, columnspan=2, pady=5)

# Start the main event loop
app.mainloop()