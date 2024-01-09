import customtkinter as ctk
import tkinter.messagebox as tkmb
from connect import connect, close_connection, close_cursor
import subprocess
import sys


class RenamePasswordForm(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rename and Change Password")
        self.geometry("400x400")
        self.wm_attributes("-toolwindow", 1)  # Remove minimize and maximize buttons, keep close button
        self.setup_ui()

    def show_message_box(self, message, title="Message"):
        tkmb.showinfo(parent=self, title=title, message=message)

    def setup_ui(self):
        # Labels and Entry Widgets for Rename File
        ctk.CTkLabel(self, text="Old File Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.old_name_entry = ctk.CTkEntry(self)
        self.old_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="New File Name:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.new_name_entry = ctk.CTkEntry(self)
        self.new_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        rename_button = ctk.CTkButton(self, text="Rename File", command=self.rename_file)
        rename_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # Labels and Entry Widgets for Change Password
        ctk.CTkLabel(self, text="Old Password:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.old_password_entry = ctk.CTkEntry(self, show="*")
        self.old_password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="New Password:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.new_password_entry = ctk.CTkEntry(self, show="*")
        self.new_password_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        change_password_button = ctk.CTkButton(self, text="Change Password", command=self.change_password)
        change_password_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        # Result Label
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

        # Button to perform both operations
        change_both_button = ctk.CTkButton(self, text="Change Both", command=self.change_both)
        change_both_button.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

        # Adjust column weights for resizing
        self.columnconfigure(1, weight=1)

    def rename_file(self):
        old_name = self.old_name_entry.get()
        new_name = self.new_name_entry.get()

        try:
            con = connect()
            cursor = con.cursor()

            # Update the database with the new file name
            update_query = "UPDATE users SET Username = %s WHERE Username = %s"
            cursor.execute(update_query, (new_name, old_name))

            con.commit()
            self.result_label.configure(text=f"File renamed from {old_name} to {new_name}")
            self.show_message_box("File renamed successfully")

        except Exception as e:
            self.result_label.configure(text=f"Error renaming file: {str(e)}")
            self.show_message_box(f"Error renaming file: {str(e)}", "Error")

        finally:
            close_cursor(cursor)
            close_connection(con)

    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()

        try:
            con = connect()
            cursor = con.cursor()

            # Update the database with the new password
            update_query = "UPDATE users SET Password = %s WHERE Password = %s"
            cursor.execute(update_query, (new_password, old_password))

            con.commit()
            self.result_label.configure(text="Password changed successfully")
            self.show_message_box("Password changed successfully")

        except Exception as e:
            self.result_label.configure(text=f"Error changing password: {str(e)}")
            self.show_message_box(f"Error changing password: {str(e)}", "Error")

        finally:
            close_cursor(cursor)
            close_connection(con)

    def change_both(self):
        old_name = self.old_name_entry.get()
        new_name = self.new_name_entry.get()
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()

        try:
            con = connect()
            cursor = con.cursor()

            # Update the database with both the new file name and new password
            rename_query = "UPDATE users SET Username = %s WHERE Username = %s"
            cursor.execute(rename_query, (new_name, old_name))

            password_query = "UPDATE users SET Password = %s WHERE Password = %s"
            cursor.execute(password_query, (new_password, old_password))

            con.commit()
            self.result_label.configure(text="File and Password changed successfully")
            self.show_message_box("File and Password changed successfully")

            # Close the current form and open main.py
            self.destroy()
            subprocess.Popen([sys.executable, 'main.py'])

        except Exception as e:
            self.result_label.configure(text=f"Error changing file and password: {str(e)}")
            self.show_message_box(f"Error changing file and password: {str(e)}", "Error")

        finally:
            close_cursor(cursor)
            close_connection(con)


if __name__ == "__main__":
    app = RenamePasswordForm()
    app.mainloop()
