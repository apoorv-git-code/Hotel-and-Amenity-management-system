import tkinter as tk
from tkinter import ttk, messagebox

from hotel import add_hotel, view_hotels
from room import add_room, view_rooms
from amenities import add_amenity, view_amenities
from customers import add_customer, view_customers
from booking import add_booking, view_bookings


def run_app():
    root = tk.Tk()
    root.title("Hotel & Amenity Management System")
    root.geometry("1000x700")
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

    # Wrap sidebar in a Canvas to allow scrolling if many buttons are added
    canvas = tk.Canvas(main_frame, bg="#34495e", width=200, highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    sidebar = tk.Frame(canvas, bg="#34495e", width=200)

    sidebar.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=sidebar, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="y", expand=False)
    scrollbar.pack(side="left", fill="y")

    content = tk.Frame(main_frame, bg="white")
    content.pack(side="right", fill="both", expand=True)

    def clear_content():
        for widget in content.winfo_children():
            widget.destroy()

    def open_add_hotel():
        window = tk.Toplevel(root)
        window.title("Add Hotel")

        tk.Label(window, text="Hotel Name").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="Location").pack()
        location_entry = tk.Entry(window)
        location_entry.pack()

        tk.Label(window, text="Rating").pack()
        rating_entry = tk.Entry(window)
        rating_entry.pack()

        def save():
            inserted_id = add_hotel(name_entry.get(), location_entry.get(), rating_entry.get())
            if inserted_id:
                messagebox.showinfo("Success", "Hotel Added")
                window.destroy()
            else:
                messagebox.showerror("Error", "Failed to add hotel")

        tk.Button(window, text="Add", command=save).pack()

    def open_view_hotels():
        clear_content()

        tree = ttk.Treeview(content, columns=("Name", "Location", "Rating"), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("Location", text="Location")
        tree.heading("Rating", text="Rating")
        tree.pack(fill="both", expand=True)

        for hotel in view_hotels():
            tree.insert("", tk.END, values=(hotel.get("name", ""), hotel.get("location", ""), hotel.get("rating", "")))

    def open_add_room():
        window = tk.Toplevel(root)
        window.title("Add Room")

        tk.Label(window, text="Room Number").pack()
        room_number_entry = tk.Entry(window)
        room_number_entry.pack()

        tk.Label(window, text="Type").pack()
        room_type_entry = tk.Entry(window)
        room_type_entry.pack()

        tk.Label(window, text="Price").pack()
        price_entry = tk.Entry(window)
        price_entry.pack()

        def save():
            inserted_id = add_room(room_number_entry.get(), room_type_entry.get(), price_entry.get())
            if inserted_id:
                messagebox.showinfo("Success", "Room Added")
                window.destroy()
            else:
                messagebox.showerror("Error", "Failed to add room")

        tk.Button(window, text="Add", command=save).pack()

    def open_view_rooms():
        clear_content()

        tree = ttk.Treeview(content, columns=("Room", "Type", "Price"), show="headings")
        tree.heading("Room", text="Room")
        tree.heading("Type", text="Type")
        tree.heading("Price", text="Price")
        tree.pack(fill="both", expand=True)

        for room in view_rooms():
            tree.insert("", tk.END, values=(room.get("room_no", ""), room.get("type", ""), room.get("price", "")))

    def open_add_amenity():
        window = tk.Toplevel(root)
        window.title("Add Amenity")

        tk.Label(window, text="Amenity Name").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="Description").pack()
        desc_entry = tk.Entry(window)
        desc_entry.pack()

        def save():
            inserted_id = add_amenity(name_entry.get(), desc_entry.get())
            if inserted_id:
                messagebox.showinfo("Success", "Amenity Added")
                window.destroy()
            else:
                messagebox.showerror("Error", "Failed to add amenity")

        tk.Button(window, text="Add", command=save).pack()

    def open_view_amenities():
        clear_content()

        tree = ttk.Treeview(content, columns=("Name", "Description"), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("Description", text="Description")
        tree.pack(fill="both", expand=True)

        for amenity in view_amenities():
            tree.insert("", tk.END, values=(amenity.get("name", ""), amenity.get("description", "")))

    def open_add_customer():
        window = tk.Toplevel(root)
        window.title("Add Customer")

        tk.Label(window, text="Customer Name").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        tk.Label(window, text="Contact").pack()
        contact_entry = tk.Entry(window)
        contact_entry.pack()

        tk.Label(window, text="ID").pack()
        id_entry = tk.Entry(window)
        id_entry.pack()

        def save():
            inserted_id = add_customer(name_entry.get(), contact_entry.get(), id_entry.get())
            if inserted_id:
                messagebox.showinfo("Success", "Customer Added")
                window.destroy()
            else:
                messagebox.showerror("Error", "Failed to add customer")

        tk.Button(window, text="Add", command=save).pack()

    def open_view_customers():
        clear_content()

        tree = ttk.Treeview(content, columns=("Name", "Contact", "ID"), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("Contact", text="Contact")
        tree.heading("ID", text="ID")
        tree.pack(fill="both", expand=True)

        for customer in view_customers():
            tree.insert("", tk.END, values=(customer.get("name", ""), customer.get("contact", ""), customer.get("id", "")))

    def open_add_booking():
        window = tk.Toplevel(root)
        window.title("Add Booking")

        tk.Label(window, text="Customer Name").pack()
        customer_entry = tk.Entry(window)
        customer_entry.pack()

        tk.Label(window, text="Room Number").pack()
        room_entry = tk.Entry(window)
        room_entry.pack()

        tk.Label(window, text="Date").pack()
        date_entry = tk.Entry(window)
        date_entry.pack()

        def save():
            inserted_id = add_booking(customer_entry.get(), room_entry.get(), date_entry.get())
            if inserted_id:
                messagebox.showinfo("Success", "Booking Added")
                window.destroy()
            else:
                messagebox.showerror("Error", "Failed to add booking")

        tk.Button(window, text="Add", command=save).pack()

    def open_view_bookings():
        clear_content()

        tree = ttk.Treeview(content, columns=("Customer", "Room", "Date"), show="headings")
        tree.heading("Customer", text="Customer")
        tree.heading("Room", text="Room")
        tree.heading("Date", text="Date")
        tree.pack(fill="both", expand=True)

        for booking in view_bookings():
            tree.insert("", tk.END, values=(booking.get("customer", ""), booking.get("room_no", ""), booking.get("date", "")))

    buttons = [
        ("Add Hotel", open_add_hotel),
        ("View Hotels", open_view_hotels),
        ("Add Room", open_add_room),
        ("View Rooms", open_view_rooms),
        ("Add Amenity", open_add_amenity),
        ("View Amenities", open_view_amenities),
        ("Add Customer", open_add_customer),
        ("View Customers", open_view_customers),
        ("Add Booking", open_add_booking),
        ("View Bookings", open_view_bookings),
    ]

    for text, command in buttons:
        btn = tk.Button(
            sidebar,
            text=text,
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 11),
            command=command,
            width=20
        )
        btn.pack(fill="x", pady=5, padx=10)

    root.mainloop()


if __name__ == "__main__":
    run_app()
