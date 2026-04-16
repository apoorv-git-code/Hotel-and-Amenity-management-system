import tkinter as tk
from tkinter import ttk, messagebox

#Accessing function data which is already used in hotel,auth,room,amenities,customers,booking
from auth import authenticate_user, register_user
from hotel import add_hotel, view_hotels
from room import add_room, view_rooms
from amenities import add_amenity, view_amenities
from customers import add_customer, view_customers
from booking import add_booking, view_bookings

# Modern Color Palette
BG_COLOR = "#F8FAFC"
SIDEBAR_COLOR = "#1E293B"
BUTTON_COLOR = "#3B82F6"
TEXT_MAIN = "#0F172A"
TEXT_LIGHT = "#FFFFFF"

# Defining font type and size
TITLE_FONT = ("Helvetica", 24, "bold")
HEADER_FONT = ("Helvetica", 14, "bold")
BODY_FONT = ("Helvetica", 11)

# Defining login screen function which will be displayed when the code is run initially 
def run_login_screen():
    login_root = tk.Tk()
    login_root.title("Hotel Management - Login")
    login_root.geometry("450x450")
    login_root.configure(bg=BG_COLOR)           #Accessing predefined bg_color

# Login gate which can be used further 
    main_frame = tk.Frame(login_root, bg=BG_COLOR, padx=40, pady=40)
    main_frame.pack(fill="both", expand=True)

# Registration/login page which is visible when we first run the code 
    tk.Label(main_frame, text="Welcome Back", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(pady=(0, 30))

# Entries which are to be user inputted
    tk.Label(main_frame, text="Username", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w")
    username_entry = tk.Entry(main_frame, font=BODY_FONT, relief="solid", bd=1)
    username_entry.pack(fill="x", pady=(5, 20), ipady=6)
    
    tk.Label(main_frame, text="Password", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w")
    password_entry = tk.Entry(main_frame, font=BODY_FONT, show="*", relief="solid", bd=1)
    password_entry.pack(fill="x", pady=(5, 30), ipady=6)
# Defining login function   
    def on_login():
        username = username_entry.get()
        password = password_entry.get()
        success, msg = authenticate_user(username, password)
        if success:
            login_root.destroy()
            run_app()
        else:
            messagebox.showerror("Error", msg)
            
    def on_register():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please fill both fields")
            return
        success, msg = register_user(username, password)
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)
            
    # Modern Buttons
    login_btn = tk.Button(main_frame, text="Log In", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=on_login)
    login_btn.pack(fill="x", pady=5, ipady=6)
    
    reg_btn = tk.Button(main_frame, text="Create Account", font=("Helvetica", 12, "bold"), bg="#94A3B8", fg=TEXT_LIGHT, relief="flat", command=on_register)
    reg_btn.pack(fill="x", pady=5, ipady=6)
    
    login_root.mainloop()


def run_app():
    root = tk.Tk()
    root.title("Hotel & Amenity Management Dashboard")
    root.geometry("1100x750")
    root.configure(bg=BG_COLOR)

    # Apply modern theme to Treeview
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", background="#FFFFFF", foreground=TEXT_MAIN, rowheight=35, fieldbackground="#FFFFFF", font=BODY_FONT, borderwidth=0)
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#E2E8F0", foreground=TEXT_MAIN, padding=(0, 5))
    style.map("Treeview", background=[("selected", BUTTON_COLOR)], foreground=[("selected", TEXT_LIGHT)])

    # Top Header
    header_frame = tk.Frame(root, bg="#0F172A", height=80)
    header_frame.pack(fill="x")
    title = tk.Label(header_frame, text="Hotel Operations Dashboard", font=TITLE_FONT, bg="#0F172A", fg=TEXT_LIGHT)
    title.pack(pady=20, padx=30, anchor="w")

    main_frame = tk.Frame(root, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True)

    # Sidebar setup
    sidebar_container = tk.Frame(main_frame, bg=SIDEBAR_COLOR, width=250)
    sidebar_container.pack(side="left", fill="y")
    
    canvas = tk.Canvas(sidebar_container, bg=SIDEBAR_COLOR, highlightthickness=0, width=250)
    scrollbar = tk.Scrollbar(sidebar_container, orient="vertical", command=canvas.yview)
    sidebar = tk.Frame(canvas, bg=SIDEBAR_COLOR, width=250)

    sidebar.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=sidebar, anchor="nw", width=250)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    content_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=40, pady=40)
    content_frame.pack(side="right", fill="both", expand=True)

    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    # Reusable style functions for forms
    def style_toplevel(window, title_text):
        window.title(title_text)
        window.geometry("500x500")
        window.configure(bg=BG_COLOR)
        main_win = tk.Frame(window, bg=BG_COLOR, padx=40, pady=30)
        main_win.pack(fill="both", expand=True)
        tk.Label(main_win, text=title_text, font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(pady=(0, 25), anchor="w")
        return main_win

    def create_lbl_entry(parent, text, is_pwd=False):
        tk.Label(parent, text=text, font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w")
        entry = tk.Entry(parent, font=BODY_FONT, relief="solid", bd=1, show="*" if is_pwd else "")
        entry.pack(fill="x", pady=(5, 20), ipady=6)
        return entry

    # ------------- Forms & Views Logics -------------
    def open_add_hotel():
        w = tk.Toplevel(root)
        main_w = style_toplevel(w, "Add New Hotel")
        n_ent = create_lbl_entry(main_w, "Hotel Name")
        l_ent = create_lbl_entry(main_w, "Location")
        r_ent = create_lbl_entry(main_w, "Rating (e.g. 1-5)")

        def save():
            if add_hotel(n_ent.get(), l_ent.get(), r_ent.get()):
                messagebox.showinfo("Success", "Hotel Added Successfully")
                w.destroy()
            else:
                messagebox.showerror("Error", "Failed to add hotel")
                
        tk.Button(main_w, text="Save Hotel", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=save).pack(fill="x", pady=15, ipady=6)

    def open_view_hotels():
        clear_content()
        tk.Label(content_frame, text="Hotels Registry", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        tree = ttk.Treeview(content_frame, columns=("Name", "Location", "Rating"), show="headings")
        tree.heading("Name", text="Hotel Name"); tree.heading("Location", text="Location"); tree.heading("Rating", text="Rating")
        tree.pack(fill="both", expand=True)
        for h in view_hotels():
            tree.insert("", tk.END, values=(h.get("name", ""), h.get("location", ""), h.get("rating", "")))

    def open_add_room():
        w = tk.Toplevel(root)
        main_w = style_toplevel(w, "Add New Room")
        n_ent = create_lbl_entry(main_w, "Room Number")
        t_ent = create_lbl_entry(main_w, "Type (e.g. Suite, Single)")
        p_ent = create_lbl_entry(main_w, "Price Per Night")

        def save():
            if add_room(n_ent.get(), t_ent.get(), p_ent.get()):
                messagebox.showinfo("Success", "Room Added Successfully")
                w.destroy()
            else:
                messagebox.showerror("Error", "Failed to add room")
                
        tk.Button(main_w, text="Save Room", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=save).pack(fill="x", pady=15, ipady=6)

    def open_view_rooms():
        clear_content()
        tk.Label(content_frame, text="Rooms Dashboard", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        tree = ttk.Treeview(content_frame, columns=("Room", "Type", "Price"), show="headings")
        tree.heading("Room", text="Room No."); tree.heading("Type", text="Type"); tree.heading("Price", text="Price")
        tree.pack(fill="both", expand=True)
        for r in view_rooms():
            tree.insert("", tk.END, values=(r.get("room_no", ""), r.get("type", ""), r.get("price", "")))

    def open_add_amenity():
        w = tk.Toplevel(root)
        main_w = style_toplevel(w, "Add New Amenity")
        n_ent = create_lbl_entry(main_w, "Amenity Name")
        d_ent = create_lbl_entry(main_w, "Detailed Description")

        def save():
            if add_amenity(n_ent.get(), d_ent.get()):
                messagebox.showinfo("Success", "Amenity Added Successfully")
                w.destroy()
            else:
                messagebox.showerror("Error", "Failed to add amenity")
                
        tk.Button(main_w, text="Save Amenity", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=save).pack(fill="x", pady=15, ipady=6)

    def open_view_amenities():
        clear_content()
        tk.Label(content_frame, text="Hotel Amenities", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        tree = ttk.Treeview(content_frame, columns=("Name", "Description"), show="headings")
        tree.heading("Name", text="Amenity Name"); tree.heading("Description", text="Description")
        tree.column("Description", width=400)
        tree.pack(fill="both", expand=True)
        for a in view_amenities():
            tree.insert("", tk.END, values=(a.get("name", ""), a.get("description", "")))

    def open_add_customer():
        w = tk.Toplevel(root)
        main_w = style_toplevel(w, "Register Customer")
        n_ent = create_lbl_entry(main_w, "Full Name")
        c_ent = create_lbl_entry(main_w, "Contact Number")
        i_ent = create_lbl_entry(main_w, "Government ID / Passport No.")

        def save():
            if add_customer(n_ent.get(), c_ent.get(), i_ent.get()):
                messagebox.showinfo("Success", "Customer Registered")
                w.destroy()
            else:
                messagebox.showerror("Error", "Failed to register customer")
                
        tk.Button(main_w, text="Save Customer", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=save).pack(fill="x", pady=15, ipady=6)

    def open_view_customers():
        clear_content()
        tk.Label(content_frame, text="Customer Directory", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        tree = ttk.Treeview(content_frame, columns=("Name", "Contact", "ID"), show="headings")
        tree.heading("Name", text="Name"); tree.heading("Contact", text="Contact"); tree.heading("ID", text="Identifier")
        tree.pack(fill="both", expand=True)
        for c in view_customers():
            tree.insert("", tk.END, values=(c.get("name", ""), c.get("contact", ""), c.get("id", "")))

    def open_add_booking():
        w = tk.Toplevel(root)
        main_w = style_toplevel(w, "New Booking")
        c_ent = create_lbl_entry(main_w, "Customer Name")
        r_ent = create_lbl_entry(main_w, "Room Number")
        d_ent = create_lbl_entry(main_w, "Check-in Date")

        def save():
            if add_booking(c_ent.get(), r_ent.get(), d_ent.get()):
                messagebox.showinfo("Success", "Booking Saved")
                w.destroy()
            else:
                messagebox.showerror("Error", "Failed to add booking")
                
        tk.Button(main_w, text="Save Booking", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=save).pack(fill="x", pady=15, ipady=6)

    def open_view_bookings():
        clear_content()
        tk.Label(content_frame, text="Active Bookings", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        tree = ttk.Treeview(content_frame, columns=("Customer", "Room", "Date"), show="headings")
        tree.heading("Customer", text="Customer Name"); tree.heading("Room", text="Room No."); tree.heading("Date", text="Check-in Date")
        tree.pack(fill="both", expand=True)
        for b in view_bookings():
            tree.insert("", tk.END, values=(b.get("customer", ""), b.get("room_no", ""), b.get("date", "")))

    # Setup Navigation Buttons
    buttons = [
        ("Register Hotel", open_add_hotel),
        ("View Hotels", open_view_hotels),
        ("Add New Room", open_add_room),
        ("View Rooms Matrix", open_view_rooms),
        ("Add Amenity", open_add_amenity),
        ("View Amenities List", open_view_amenities),
        ("Register Customer", open_add_customer),
        ("Customer Directory", open_view_customers),
        ("Process Booking", open_add_booking),
        ("View Active Bookings", open_view_bookings),
    ]

    tk.Label(sidebar, text="MAIN MENU", font=("Helvetica", 11, "bold"), bg=SIDEBAR_COLOR, fg="#94A3B8").pack(pady=(30, 15), padx=20, anchor="w")
    
    for text, command in buttons:
        btn = tk.Button(
            sidebar,
            text=text,
            bg=SIDEBAR_COLOR,
            fg="#CBD5E1",
            font=("Helvetica", 11, "bold"),
            command=command,
            relief="flat",
            anchor="w",
            padx=25,
            cursor="hand2",
            activebackground="#334155",
            activeforeground="#FFFFFF"
        )
        btn.pack(fill="x", pady=2, ipady=6)
        
        # Add hover effects 
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#334155", fg="#FFFFFF"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=SIDEBAR_COLOR, fg="#CBD5E1"))

    # Select the first view by default
    open_view_hotels()
    root.mainloop()

if __name__ == "__main__":
    run_login_screen()
