import tkinter as tk

def on_resize(event):
    # Update the label text with the current width and height of the window
    label.config(text=f"Width: {event.width}, Height: {event.height}")

root = tk.Tk()
root.title("Dynamic UI Adaptation")

# Create and place widgets in the grid
label = tk.Label(root, text="Resize the window to see dynamic adaptation.")
label.grid(row=0, column=0, sticky="nsew")  # "nsew" makes the label expand with the window

# Set row and column weights to make the label expand with the window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Bind the on_resize function to the Configure event
root.bind("<Configure>", on_resize)

root.mainloop()