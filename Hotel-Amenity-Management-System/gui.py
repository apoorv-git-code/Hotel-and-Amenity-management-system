import tkinter as tk
from tkinter import ttk, messagebox

#Accessing function data which is already used in hotel,auth,room,amenities,customers,booking
from auth import authenticate_user, register_user
from hotel import add_hotel, view_hotels, update_hotel
from room import add_room, view_rooms
from amenities import add_amenity, view_amenities
from customers import add_customer, view_customers
from booking import add_booking, view_bookings, cancel_booking

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
            run_app(username)
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


def run_app(username):
    is_admin = username.lower() == "admin"
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
    title = tk.Label(header_frame, text=f"Hotel Operations Dashboard (User: {username})", font=TITLE_FONT, bg="#0F172A", fg=TEXT_LIGHT)
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
        window.geometry("500x650")
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
            if add_hotel(n_ent.get(), l_ent.get(), float(r_ent.get()) if r_ent.get() else 3.0):
                messagebox.showinfo("Success", "Hotel Added Successfully")
                w.destroy()
            else:
                messagebox.showerror("Error", "Failed to add hotel")
                
        tk.Button(main_w, text="Save Hotel", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=save).pack(fill="x", pady=15, ipady=6)

    def open_update_hotel():
        w = tk.Toplevel(root)
        main_w = style_toplevel(w, "Update Hotel")
        
        tk.Label(main_w, text="Select Hotel", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w")
        hotels_av = [h.get("name") for h in view_hotels() if h.get("name")]
        h_combo = ttk.Combobox(main_w, values=hotels_av, state="readonly", font=BODY_FONT)
        h_combo.pack(fill="x", pady=(5, 20), ipady=6)

        l_ent = create_lbl_entry(main_w, "New Location (leave blank to keep)")
        r_ent = create_lbl_entry(main_w, "New Rating (1-5, leave blank to keep)")

        def update():
            sel_h = h_combo.get()
            if not sel_h:
                messagebox.showerror("Error", "Please select a hotel")
                return
            
            loc_val = l_ent.get() if l_ent.get() else None
            rate_val = float(r_ent.get()) if r_ent.get() else None
            
            if update_hotel(sel_h, location=loc_val, rating=rate_val):
                messagebox.showinfo("Success", "Hotel Updated Successfully")
                w.destroy()
            else:
                messagebox.showerror("Error", "Failed to update hotel")
                
        tk.Button(main_w, text="Update Hotel", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=update).pack(fill="x", pady=15, ipady=6)

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
        
        tk.Label(main_w, text="Select Hotel", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w")
        hotels_av = [h.get("name") for h in view_hotels() if h.get("name")]
        h_combo = ttk.Combobox(main_w, values=hotels_av, state="readonly", font=BODY_FONT)
        h_combo.pack(fill="x", pady=(5, 20), ipady=6)

        n_ent = create_lbl_entry(main_w, "Room Number")
        
        tk.Label(main_w, text="Room Type", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w")
        t_combo = ttk.Combobox(main_w, values=["Single", "Double", "Suite", "Deluxe", "Presidential Suite", "Penthouse"], state="readonly", font=BODY_FONT)
        t_combo.pack(fill="x", pady=(5, 20), ipady=6)

        p_ent = create_lbl_entry(main_w, "Price Per Night (₹)")

        def save():
            if not h_combo.get() or not n_ent.get():
                messagebox.showerror("Error", "Hotel and Room number are required.")
                return
            result = add_room(h_combo.get(), n_ent.get(), t_combo.get(), float(p_ent.get()) if p_ent.get() else 0.0)
            if result == "duplicate":
                messagebox.showwarning("Warning", "Room already exists!")
            elif result:
                messagebox.showinfo("Success", "Room Added Successfully")
                w.destroy()
            else:
                messagebox.showerror("Error", "Failed to add room")
                
        tk.Button(main_w, text="Save Room", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=save).pack(fill="x", pady=15, ipady=6)

    def open_view_rooms():
        clear_content()
        tk.Label(content_frame, text="Rooms Dashboard", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        tree = ttk.Treeview(content_frame, columns=("Hotel", "Room", "Type", "Price"), show="headings")
        tree.heading("Hotel", text="Hotel"); tree.heading("Room", text="Room No."); tree.heading("Type", text="Type"); tree.heading("Price", text="Price")
        tree.pack(fill="both", expand=True)
        for r in view_rooms():
            tree.insert("", tk.END, values=(r.get("hotel_name", ""), r.get("room_no", ""), r.get("type", ""), r.get("price", "")))

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
        e_ent = create_lbl_entry(main_w, "Email ID")
        cy_ent = create_lbl_entry(main_w, "City")

        def save():
            if add_customer(n_ent.get(), c_ent.get(), e_ent.get(), cy_ent.get()):
                messagebox.showinfo("Success", "Customer Registered")
                w.destroy()
            else:
                messagebox.showerror("Error", "Failed to register customer")
                
        tk.Button(main_w, text="Save Customer", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=save).pack(fill="x", pady=15, ipady=6)

    def open_view_customers():
        clear_content()
        tk.Label(content_frame, text="Customer Directory", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        tree = ttk.Treeview(content_frame, columns=("Name", "Contact", "Email", "City"), show="headings")
        tree.heading("Name", text="Name"); tree.heading("Contact", text="Contact"); tree.heading("Email", text="Email ID"); tree.heading("City", text="City")
        tree.pack(fill="both", expand=True)
        for c in view_customers():
            name = c.get("name") or c.get("customer_name", "")
            contact = c.get("contact") or c.get("phone", "")
            email = c.get("email_id") or c.get("email") or c.get("id", "")
            city = c.get("city", "")
            tree.insert("", tk.END, values=(name, contact, email, city))

    def open_add_booking():
        w = tk.Toplevel(root)
        main_w = style_toplevel(w, "New Booking")
        
        tk.Label(main_w, text="Customer", font=HEADER_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w")
        customers_list = [c.get("name") for c in view_customers() if c.get("name")]
        
        if is_admin:
            c_combo = ttk.Combobox(main_w, values=customers_list, state="readonly", font=BODY_FONT)
            c_combo.pack(fill="x", pady=(5, 20), ipady=6)
        else:
            c_ent = tk.Entry(main_w, font=BODY_FONT, relief="solid", bd=1)
            c_ent.insert(0, username)
            c_ent.config(state="disabled")
            c_ent.pack(fill="x", pady=(5, 20), ipady=6)
            
        r_ent = create_lbl_entry(main_w, "Room Number")
        d_ent = create_lbl_entry(main_w, "Check-in Date (YYYY-MM-DD)")
        out_ent = create_lbl_entry(main_w, "Check-out Date (YYYY-MM-DD)")

        def save():
            cust = c_combo.get() if is_admin else c_ent.get()
            if not cust or not r_ent.get() or not d_ent.get() or not out_ent.get():
                messagebox.showerror("Error", "All fields are required")
                return
            if add_booking(cust, r_ent.get(), d_ent.get(), out_ent.get()):
                messagebox.showinfo("Success", "Booking Saved")
                w.destroy()
            else:
                messagebox.showerror("Error", "Failed to add booking")
                
        tk.Button(main_w, text="Save Booking", font=("Helvetica", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_LIGHT, relief="flat", command=save).pack(fill="x", pady=15, ipady=6)

    def open_view_bookings():
        clear_content()
        tk.Label(content_frame, text="Active Bookings", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        tree_frame = tk.Frame(content_frame, bg=BG_COLOR)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Customer", "Room", "In", "Out"), show="headings")
        tree.heading("ID", text="Booking ID"); tree.heading("Customer", text="Customer"); tree.heading("Room", text="Room No."); tree.heading("In", text="Check-in"); tree.heading("Out", text="Check-out")
        tree.column("ID", width=120)
        tree.pack(side="left", fill="both", expand=True)
        
        v_scroll = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        v_scroll.pack(side="right", fill="y")
        tree.configure(yscrollcommand=v_scroll.set)

        all_bookings = view_bookings()
        if not is_admin:
            all_bookings = [b for b in all_bookings if b.get("customer", "") == username or b.get("customer_id", "") == username]

        for b in all_bookings:
            cst = b.get("customer") or b.get("customer_id", "")
            rm = b.get("room_no") or b.get("room_number", "")
            cin = b.get("date") or b.get("check_in", "")
            cout = b.get("checkout_date", "")
            tree.insert("", tk.END, values=(str(b.get("_id", "")), cst, rm, cin, cout))

        def on_cancel():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a booking to cancel.")
                return
            item = tree.item(selected[0])
            b_id = item["values"][0]
            if messagebox.askyesno("Confirm", f"Are you sure you want to cancel booking {b_id}?"):
                if cancel_booking(b_id):
                    messagebox.showinfo("Success", "Booking Cancelled")
                    open_view_bookings()
                else:
                    messagebox.showerror("Error", "Failed to cancel booking. It may have already been deleted.")

        tk.Button(content_frame, text="Cancel Selected Booking", font=("Helvetica", 12, "bold"), bg="#EF4444", fg=TEXT_LIGHT, relief="flat", command=on_cancel).pack(anchor="e", pady=10)


    # Setup Navigation Buttons with Role Based Access
    buttons_config = [
        ("View Hotels", open_view_hotels, False),
        ("Register Hotel", open_add_hotel, True),
        ("Update Hotel", open_update_hotel, True),
        ("View Rooms Matrix", open_view_rooms, False),
        ("Add New Room", open_add_room, True),
        ("View Amenities List", open_view_amenities, False),
        ("Add Amenity", open_add_amenity, True),
        ("Customer Directory", open_view_customers, True),
        ("Register Customer", open_add_customer, True),
        ("Process Booking", open_add_booking, False),
        ("View Active Bookings", open_view_bookings, False),
    ]

    tk.Label(sidebar, text="MAIN MENU", font=("Helvetica", 11, "bold"), bg=SIDEBAR_COLOR, fg="#94A3B8").pack(pady=(30, 15), padx=20, anchor="w")
    
    for text, command, admin_only in buttons_config:
        if admin_only and not is_admin:
            continue
            
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
        
    # Logout button
    def logout():
        root.destroy()
        run_login_screen()
        
    tk.Label(sidebar, text="", bg=SIDEBAR_COLOR).pack(pady=20) # spacer
    tk.Button(sidebar, text="Logout", font=("Helvetica", 11, "bold"), bg="#EF4444", fg=TEXT_LIGHT, relief="flat", command=logout).pack(fill="x", pady=5, padx=20, ipady=6)

    # Select the first view by default
    open_view_hotels()
    root.mainloop()

if __name__ == "__main__":
    run_login_screen()
