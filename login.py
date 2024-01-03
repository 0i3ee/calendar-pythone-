import customtkinter as ctk
import tkinter.messagebox as tkmb
import subprocess
from connect import connect, close_connection
import os


app = ctk.CTk()
app.title("Login Form")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
center_x = int((screen_width - 400) / 2)  # Adjust 400 as per your form's width
center_y = int((screen_height - 300) / 2)  # Adjust 300 as per your form's height
# Create the main window
app.geometry(f"400x400+{center_x}+{center_y}")


def cancel():
     app.destroy()



def login():
    # Retrieve credentials from the database
    query = "SELECT username, password FROM users WHERE username = %s"
    cursor.execute(query, (user_entry.get(),))
    result = cursor.fetchone()
    if result:
        username_db, password_db = result
        if user_pass.get() == password_db:
            tkmb.showinfo(title="Login Successful", message="You have logged in successfully")  
            cancel()
            os.system(f"python main.py {username_db}")
            return username_db
        else:
            tkmb.showwarning(title='Wrong password', message='Please check your password')
    else:
        tkmb.showerror(title="Login Failed", message="Invalid Username")


def register():
        cancel()
        subprocess.run(["python", "register_form.py"], check=True)


ctk.set_appearance_mode("dark") 
  
ctk.set_default_color_theme("blue") 
  

  
connection = connect()
cursor = connection.cursor()
  
label = ctk.CTkLabel(app,text="Welcome to Calendar Program") 
label.pack(pady=20) 
  
  
frame = ctk.CTkFrame(master=app) 
frame.pack(pady=20,padx=40,fill='both',expand=True) 
  
label = ctk.CTkLabel(master=frame,text='For Login page') 
label.pack(pady=12,padx=10) 
  
  
user_entry= ctk.CTkEntry(master=frame,placeholder_text="Username") 
user_entry.pack(pady=12,padx=10) 
  
user_pass= ctk.CTkEntry(master=frame,placeholder_text="Password",show="*") 
user_pass.pack(pady=12,padx=10) 
  
  
button = ctk.CTkButton(master=frame,text='Login',command=login) 
button.pack(pady=12,padx=10) 
  
bt_register = ctk.CTkButton(master=frame,text='Register',command=register) 
bt_register.pack(pady=12,padx=10) 

  
app.mainloop()