import tkinter as tk
from tkinter import ttk, messagebox

from hotel import add_hotel, view_hotels
from room import add_room, view_rooms
from amenities import add_amenity, view_amenities
from booking import add_booking, view_bookings


root = tk.Tk()
root.title("Hotel & Amenity Management System")
root.geometry("1000x600")
root.configure(bg="#2c3e50")


title = tk.Label(
    root,
    text="Hotel & Amenity Management System",
    font=("Segoe UI", 20, "bold"),
    bg="#2c3e50",
    fg="white"
)
title.pack(pady=10)


main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)


sidebar = tk.Frame(main_frame, bg="#34495e", width=200)
sidebar.pack(side="left", fill="y")


content = tk.Frame(main_frame, bg="white")
content.pack(side="right", fill="both", expand=True)


def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


# HOTEL FUNCTIONS

def open_add_hotel():
    window = tk.Toplevel(root)
    window.title("Add Hotel")

    tk.Label(window, text="Hotel Name").pack()
    name = tk.Entry(window)
    name.pack()

    tk.Label(window, text="Location").pack()
    location = tk.Entry(window)
    location.pack()

    tk.Label(window, text="Rating").pack()
    rating = tk.Entry(window)
    rating.pack()

    def save():
        add_hotel(name.get(), location.get(), rating.get())
        messagebox.showinfo("Success", "Hotel Added")

    tk.Button(window, text="Add", command=save).pack()


def open_view_hotels():
    clear_content()

    tree = ttk.Treeview(content, columns=("Name", "Location", "Rating"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Location", text="Location")
    tree.heading("Rating", text="Rating")

    tree.pack(fill="both", expand=True)

    for hotel in view_hotels():
        tree.insert("", tk.END, values=(hotel["name"], hotel["location"], hotel["rating"]))


# ROOM FUNCTIONS

def open_add_room():
    window = tk.Toplevel(root)

    tk.Label(window, text="Room Number").pack()
    room = tk.Entry(window)
    room.pack()

    tk.Label(window, text="Type").pack()
    type = tk.Entry(window)
    type.pack()

    tk.Label(window, text="Price").pack()
    price = tk.Entry(window)
    price.pack()

    def save():
        add_room(room.get(), type.get(), price.get())
        messagebox.showinfo("Success", "Room Added")

    tk.Button(window, text="Add", command=save).pack()


def open_view_rooms():
    clear_content()

    tree = ttk.Treeview(content, columns=("Room", "Type", "Price"), show="headings")
    tree.heading("Room", text="Room")
    tree.heading("Type", text="Type")
    tree.heading("Price", text="Price")

    tree.pack(fill="both", expand=True)

    for room in view_rooms():
        tree.insert("", tk.END, values=(room["room_no"], room["type"], room["price"]))


# AMENITIES

def open_add_amenity():
    window = tk.Toplevel(root)

    tk.Label(window, text="Amenity Name").pack()
    name = tk.Entry(window)
    name.pack()

    tk.Label(window, text="Description").pack()
    desc = tk.Entry(window)
    desc.pack()

    def save():
        add_amenity(name.get(), desc.get())
        messagebox.showinfo("Success", "Amenity Added")

    tk.Button(window, text="Add").pack()


def open_view_amenities():
    clear_content()

    tree = ttk.Treeview(content, columns=("Name", "Description"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Description", text="Description")

    tree.pack(fill="both", expand=True)

    for amenity in view_amenities():
        tree.insert("", tk.END, values=(amenity["name"], amenity["description"]))


# SIDEBAR BUTTONS

buttons = [
    ("Add Hotel", open_add_hotel),
    ("View Hotels", open_view_hotels),
    ("Add Room", open_add_room),
    ("View Rooms", open_view_rooms),
    ("Add Amenity", open_add_amenity),
    ("View Amenities", open_view_amenities),
]

for text, command in buttons:
    btn = tk.Button(
        sidebar,
        text=text,
        bg="#3498db",
        fg="white",
        font=("Segoe UI", 11),
        command=command
    )
    btn.pack(fill="x", pady=5, padx=10)


root.mainloop()