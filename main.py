import customtkinter
import tkinter
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import date
import googlemaps
from tkintermapview import TkinterMapView
import geocoder
from geopy.geocoders import Nominatim
import sys
from connect import connect, close_connection
from tkinter import messagebox
from datetime import datetime
import subprocess

username_db = sys.argv[2] if len(sys.argv) > 2 else "Guest"

connection = connect()
cursor = connection.cursor()

def get_current_location():
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode("me")

    if location:
        return location.latitude, location.longitude
    else:
        return None




def search():
    location_name = entry_location.get()
    if location_name:
        geolocator = Nominatim(user_agent="my_geocoder")
        location = geolocator.geocode(location_name)

        if location:
            latitude, longitude = location.latitude, location.longitude
            gap_widget.set_position(latitude, longitude, marker=True)
            gap_widget.set_zoom(12)
        else:
            print(f"Location not found for {location_name}")


def select_labels():
    selected_date = mycal.selection_get()
    ldate.configure(text=str(selected_date.day))
    lmonth.configure(text=str(selected_date.month))
    lyear.configure(text=str(selected_date.year))

def refresh_calendar():
    mycal.selection_set(date.today())


root = customtkinter.CTk()
root.geometry("1366x815")
root.title("Event")


def logout():
    root.destroy()
    subprocess.run(["python", "login.py"], check=True)

labeldate_font = ("Times New Roman", 50, 'bold')
labeldate_font1 = ("Times New Roman", 30, 'bold')

lb_hader = tkinter.Label(root,text="Evnet")
lb_hader.pack(side="top",fill="x")
lb_hader.config(font=('Times New Roman',20),bg='gray',fg='black')

lb_footer = tkinter.Label(root)
lb_footer.pack(side="bottom",fill="x")
lb_footer.config(font=('Times New Roman',20),bg='gray',fg='black')


labeldate = customtkinter.CTkLabel(root, font=labeldate_font,text="", fg_color="gray", width=720, height=80,corner_radius=10)
labeldate.place(x=5, y=60)

labeldate = customtkinter.CTkLabel(root, font=labeldate_font, text="Date", fg_color="gray")
labeldate.place(x=10, y=70)

ldate = customtkinter.CTkLabel(root, font=labeldate_font, text="00", fg_color="black")
ldate.place(x=140, y=70)

labelmonth = customtkinter.CTkLabel(root, font=labeldate_font, text="Month", fg_color="gray")
labelmonth.place(x=230, y=70)

lmonth = customtkinter.CTkLabel(root, font=labeldate_font, text="00", fg_color="black")
lmonth.place(x=400, y=70)

labelyear = customtkinter.CTkLabel(root, font=labeldate_font, text="Year", fg_color="gray")
labelyear.place(x=480, y=70)

lyear = customtkinter.CTkLabel(root, font=labeldate_font, text="0000", fg_color="black")
lyear.place(x=600, y=70)

count = 0  

if len(sys.argv) > 1:
        count = 0  
        username_from_login = sys.argv[1]

query_all = "SELECT UserID FROM users WHERE username ='" + username_from_login + "'"
cursor.execute(query_all)
result = cursor.fetchall()
userID = str(result[0][0])

def reloads():
        
    
    if len(sys.argv) > 1:
        count = 0  
        username_from_login = sys.argv[1]
        luser = customtkinter.CTkLabel(root, font=labeldate_font1, text=f"Username: {username_from_login}")
        luser.place(x=45, y=160)

        # Assuming cursor is a global variable and is connected to the database
        query_all = "SELECT id, eventdate, Name FROM dataevents where UserID = " + str(userID)
        cursor.execute(query_all)
        records_all = cursor.fetchall()
        myTree.delete(*myTree.get_children())

        for record in records_all:
            myTree.insert(parent='', index='end', iid=count, text='', values=record)
            count += 1

def Delete():
    record = cursor.fetchall()
    result = messagebox.askyesno("Verify", "Do you want to save this???")

    if result:
        index = myTree.selection()
        memID = myTree.item(index)["values"]
        delid = str(memID[0])  
        
        # Your deletion logic here
        query = "DELETE FROM dataevents WHERE id = " + delid
        cursor.execute(query)
        cursor.execute("Set @autoid:=0;")
        cursor.execute("UPDATE dataevents set id=@autoid := (@autoid+1);")
        cursor.execute(" ALTER TABLE dataevents AUTO_INCREMENT =1")
        cursor.execute("commit")

        # Delete the selected item in the Treeview
        myTree.delete(index)
        Cleas()

def Cleas():
    mycal.selection_set(date.today())
    selected_date = mycal.selection_get()

    ldate.configure(text=str(selected_date.day))
    lmonth.configure(text=str(selected_date.month))
    lyear.configure(text=str(selected_date.year))
    event_entry.delete(0, tk.END)
    textbox.delete(1.0, tk.END)
    entry_location.delete(0, tk.END)

    


def updates():
    selected_item = myTree.selection()
    if selected_item:
        # Get the ID of the selected item
        item_id = myTree.item(selected_item, "values")[0]

        # Fetch data from the database based on the selected ID
        cursor.execute("SELECT id FROM dataevents WHERE id="+ str(item_id))
        result = cursor.fetchone()
        if result:
            id = result[0]
            selected_date = mycal.selection_get()
            evalname = event_entry.get()
            eventtext = textbox.get("1.0", "end-1c")
            locl = entry_location.get()

    msg = messagebox.askquestion("Confirm","Do you want to update this information ?")
    if(msg =='yes'):
        query="update dataevents set eventdate = '"+str(selected_date)+"',Name='"+evalname+"', Detail ='"+eventtext+"',Location='"+locl+"' where id='"+str(id)+"' "
        cursor.execute(query)
        cursor.execute("commit")
        result = cursor.fetchone()
        query_all = "SELECT id,eventdate, Name FROM dataevents"
        cursor.execute(query_all)
        records_all = cursor.fetchall()

        myTree.delete(*myTree.get_children())

        count = 0
        for record in records_all:
            myTree.insert(parent='', index='end', iid=count, text='', values=record)
            count += 1
        Cleas()


def on_tree_select(event):
    selected_item = myTree.selection()

    if selected_item:
        # Get the ID of the selected item
        item_id = myTree.item(selected_item, "values")[0]

        # Fetch data from the database based on the selected ID
        cursor.execute("SELECT eventdate, Name, Detail, Location FROM dataevents WHERE id="+ str(item_id))
        result = cursor.fetchone()

        if result:
            result_date_str = result[0].strftime('%Y-%m-%d')
            
            mycal.selection_set(result_date_str)
            selected_date = mycal.selection_get()

            ldate.configure(text=str(selected_date.day))
            lmonth.configure(text=str(selected_date.month))
            lyear.configure(text=str(selected_date.year))
            
            event_entry.delete(0, tk.END)
            event_entry.insert(0, result[1])

            textbox.delete(1.0, tk.END)
            textbox.insert(1.0, result[2])

            entry_location.delete(0, tk.END)
            entry_location.insert(0, result[3])
            


def save(): 
    username_from_login = sys.argv[1]
    myevel = mycal.get_date()
    eventname = event_entry.get()
    eventdetail = textbox.get("1.0", "end-1c")
    evenrlocal = entry_location.get()
    users = username_from_login

    query = "insert into dataevents(eventdate,Name,Detail,Location,UserID) values(%s,%s,%s,%s,%s)"
    values = (myevel,eventname,eventdetail,evenrlocal,users)
    cursor.execute(query,values)
    cursor.execute("commit")
    result = cursor.fetchone()

    

    query_all = "SELECT id, eventdate, Name FROM dataevents where UserID = "+ str(userID) 
    cursor.execute(query_all)
    records_all = cursor.fetchall()

    myTree.delete(*myTree.get_children())

    count = 0
    for record in records_all:
        myTree.insert(parent='', index='end', iid=count, text='', values=record)
        count += 1

    Cleas()

    

levent = customtkinter.CTkLabel(root, font=labeldate_font1, text="Event Name:")
levent.place(x=20, y=220)

leventde = customtkinter.CTkLabel(root, font=labeldate_font1, text="Detail:")
leventde.place(x=100, y=290)


event_entry= customtkinter.CTkEntry(root,placeholder_text="Event",font=labeldate_font1,width=300) 
event_entry.place(x=200,y=220) 

textbox = customtkinter.CTkTextbox(root,width=300,height=200,fg_color="gray" )
textbox.place(x=200,y=290) 

button_Load = customtkinter.CTkButton(root,text='Load',font=labeldate_font1,fg_color="green",command=reloads) 
button_Load.place(x=0,y=0) 

button_ADD = customtkinter.CTkButton(root,text='ADD',font=labeldate_font1,fg_color="green",command=save) 
button_ADD.place(x=550,y=220) 

button_Update = customtkinter.CTkButton(root,text='Update',font=labeldate_font1,command=updates)
button_Update.place(x=550,y=270) 

button_Delete = customtkinter.CTkButton(root,text='Delete',font=labeldate_font1,fg_color="red",command=Delete) 
button_Delete.place(x=550,y=320) 

button_Clear = customtkinter.CTkButton(root,text='Clear',font=labeldate_font1,fg_color="gray",command=Cleas) 
button_Clear.place(x=550,y=370) 

button_logout = customtkinter.CTkButton(root,text='logout',font=labeldate_font1,fg_color="red",command=logout) 
button_logout.place(x=1000,y=720) 

button_Exit = customtkinter.CTkButton(root,text='Exit',font=labeldate_font1,fg_color="red",command=quit) 
button_Exit.place(x=1150,y=720)



calendar_font = ("Times New Roman", 25)
calendar_foreground = "white"  # Text color
calendar_background = "black"   # Background color

mycal = Calendar(
    root,
    setmode="day",
    font=calendar_font,
    foreground=calendar_foreground,
    background=calendar_background,
    date_pattern='yyyy-mm-dd'
)
mycal.place(x=750, y=90)

select_button = customtkinter.CTkButton(root, text="Set Date", command=select_labels)
select_button.place(x=1150, y=50)

update_button = customtkinter.CTkButton(root, text="Reload", command=refresh_calendar)
update_button.place(x=1000, y=50)


myTree = ttk.Treeview(root,columns=(1,2,3),show = "headings")
myTree.place(x=750,y=480)

style = ttk.Style()
style.configure("TreeView.Heading",font=('Times New Roman',14))
style.configure("TreeView",font=('Times New Roman',14))

myTree.heading(1,text="id", anchor='center')
myTree.heading(2,text="Date",anchor='center')
myTree.heading(3,text="Name",anchor='center')

myTree.column(1,width=20,anchor='center')
myTree.column(2,width=260,anchor='center')
myTree.column(3,width=260,anchor='center')

entry_location = customtkinter.CTkEntry(root, placeholder_text="Enter Location", font=labeldate_font1, width=210)
entry_location.place(x=520, y=500)

search_button = customtkinter.CTkButton(root, text="Search", command=search)
search_button.place(x=550, y=570)


gap_widget = TkinterMapView(root, width=400, height=200)
gap_widget.place(x=100, y=500)
gap_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")



myTree.bind("<<TreeviewSelect>>", on_tree_select)
root.mainloop()
