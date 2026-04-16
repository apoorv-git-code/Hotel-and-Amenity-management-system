import streamlit as st
import sys
import os

# Allow relative imports from the same directory
sys.path.insert(0, os.path.dirname(__file__))

from auth import authenticate_user, register_user
from hotel import add_hotel, view_hotels
from room import add_room, view_rooms
from amenities import add_amenity, view_amenities
from customers import add_customer, view_customers
from booking import add_booking, view_bookings

# ─────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hotel & Amenity Management System",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
#  CUSTOM CSS – Premium dark-accented theme
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── Main background ── */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0f172a 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1a2744 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.2) !important;
}
[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}
[data-testid="stSidebarNav"] { display: none; }

/* ── Hero header ── */
.hero-header {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 32px;
    box-shadow: 0 20px 60px rgba(99,102,241,0.35);
    display: flex;
    align-items: center;
    gap: 20px;
}
.hero-header h1 {
    color: #ffffff !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    margin: 0 !important;
    letter-spacing: -0.5px;
}
.hero-header p {
    color: rgba(255,255,255,0.8) !important;
    font-size: 1rem !important;
    margin: 4px 0 0 0 !important;
}
.hero-icon { font-size: 3rem; }

/* ── Cards ── */
.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 14px;
    padding: 24px 28px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.3);
}
.metric-card .metric-value {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.metric-card .metric-label {
    color: #94a3b8;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-top: 8px;
}
.metric-card .metric-icon { font-size: 1.8rem; margin-bottom: 8px; }

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    padding-bottom: 12px;
    border-bottom: 2px solid rgba(99,102,241,0.3);
}
.section-header h2 {
    color: #f1f5f9 !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
}
.section-icon { font-size: 1.6rem; }

/* ── Login card ── */
.login-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
}
.login-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 48px 52px;
    width: 100%;
    max-width: 440px;
    backdrop-filter: blur(20px);
    box-shadow: 0 30px 80px rgba(0,0,0,0.4);
}
.login-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 8px;
}
.login-subtitle {
    text-align: center;
    color: #64748b;
    font-size: 0.9rem;
    margin-bottom: 32px;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stDateInput"] label,
[data-testid="stSelectbox"] label {
    color: #94a3b8 !important;
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.4px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 10px 22px !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Secondary button override via key class trick */
.sec-btn > button {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
}

/* ── Dataframes / tables ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
}
[data-testid="stDataFrame"] table {
    background: rgba(15,23,42,0.8) !important;
}
[data-testid="stDataFrame"] thead th {
    background: rgba(99,102,241,0.15) !important;
    color: #a5b4fc !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid rgba(99,102,241,0.3) !important;
}
[data-testid="stDataFrame"] tbody td {
    color: #cbd5e1 !important;
    border-color: rgba(99,102,241,0.1) !important;
    font-size: 0.88rem !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
    background: rgba(99,102,241,0.08) !important;
}

/* ── Success / error alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* ── Divider ── */
hr { border-color: rgba(99,102,241,0.2) !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent !important;
    border-bottom: 1px solid rgba(99,102,241,0.2) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px 8px 0 0 !important;
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 10px 20px !important;
}
[aria-selected="true"] {
    background: rgba(99,102,241,0.15) !important;
    color: #a5b4fc !important;
    border-bottom: 2px solid #6366f1 !important;
}

/* ── Sidebar nav items ── */
.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    border-radius: 10px;
    cursor: pointer;
    transition: background 0.15s;
    color: #94a3b8;
    font-weight: 500;
    font-size: 0.9rem;
    margin-bottom: 4px;
    text-decoration: none;
}
.nav-item.active {
    background: rgba(99,102,241,0.2);
    color: #a5b4fc;
}
.nav-item:hover { background: rgba(99,102,241,0.12); color: #c7d2fe; }

/* ── Form panel ── */
.form-panel {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 28px;
}
.form-title {
    color: #a5b4fc;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 64px 32px;
    color: #475569;
}
.empty-state .es-icon { font-size: 3.5rem; margin-bottom: 12px; }
.empty-state .es-text { font-size: 1.1rem; font-weight: 600; }
.empty-state .es-sub { font-size: 0.85rem; margin-top: 6px; color: #334155; }

/* ── Badge ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.4px;
}
.badge-indigo { background: rgba(99,102,241,0.2); color: #a5b4fc; }
.badge-cyan   { background: rgba(6,182,212,0.2);  color: #67e8f9;  }
.badge-green  { background: rgba(16,185,129,0.2); color: #6ee7b7;  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"


# ─────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────
def section_header(icon: str, title: str):
    st.markdown(f"""
    <div class="section-header">
        <span class="section-icon">{icon}</span>
        <h2>{title}</h2>
    </div>
    """, unsafe_allow_html=True)


def metric_card(icon: str, value, label: str):
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def nav_button(label: str, icon: str, page_name: str):
    active = "active" if st.session_state.page == page_name else ""
    if st.button(f"{icon}  {label}", key=f"nav_{page_name}", use_container_width=True):
        st.session_state.page = page_name
        st.rerun()


# ─────────────────────────────────────────────────────────
#  LOGIN / REGISTER SCREEN
# ─────────────────────────────────────────────────────────
def render_auth():
    col_l, col_c, col_r = st.columns([1, 1.4, 1])
    with col_c:
        # Logo / brand
        st.markdown("""
        <div style="text-align:center;margin-bottom:12px;">
            <div style="font-size:3.5rem;margin-bottom:8px;">🏨</div>
            <div style="font-size:1.8rem;font-weight:800;color:#f1f5f9;letter-spacing:-0.5px;">HotelOS</div>
            <div style="color:#64748b;font-size:0.88rem;margin-top:4px;">Unified Hotel & Amenity Platform</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        mode = st.session_state.auth_mode
        tab_login, tab_register = st.tabs(["🔑  Log In", "✨  Create Account"])

        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                username = st.text_input("Username", placeholder="Enter your username", key="login_user")
                password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Log In →", use_container_width=True)
                if submitted:
                    if not username or not password:
                        st.error("Please fill in both fields.")
                    else:
                        ok, msg = authenticate_user(username, password)
                        if ok:
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.page = "Dashboard"
                            st.rerun()
                        else:
                            st.error(f"❌  {msg}")

        with tab_register:
            with st.form("register_form", clear_on_submit=True):
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                reg_user = st.text_input("Username", placeholder="Choose a username", key="reg_user")
                reg_pass = st.text_input("Password", type="password", placeholder="Choose a strong password", key="reg_pass")
                reg_pass2 = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="reg_pass2")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Create Account →", use_container_width=True)
                if submitted:
                    if not reg_user or not reg_pass:
                        st.error("Please fill in all fields.")
                    elif reg_pass != reg_pass2:
                        st.error("Passwords do not match.")
                    else:
                        ok, msg = register_user(reg_user, reg_pass)
                        if ok:
                            st.success(f"✅  {msg} — You can now log in.")
                        else:
                            st.error(f"❌  {msg}")


# ─────────────────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 20px 4px 8px;">
            <div style="font-size:1.6rem;font-weight:800;color:#f1f5f9;letter-spacing:-0.4px;">🏨 HotelOS</div>
            <div style="color:#334155;font-size:0.78rem;margin-top:2px;">Logged in as <b style="color:#6366f1">{st.session_state.username}</b></div>
        </div>
        <hr style="margin:12px 0 20px;">
        <div style="color:#475569;font-size:0.72rem;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;padding: 0 4px 8px;">Navigation</div>
        """, unsafe_allow_html=True)

        nav_button("Dashboard",          "📊", "Dashboard")
        nav_button("Hotels",             "🏨", "Hotels")
        nav_button("Rooms",              "🛏️", "Rooms")
        nav_button("Amenities",          "🌟", "Amenities")
        nav_button("Customers",          "👤", "Customers")
        nav_button("Bookings",           "📋", "Bookings")

        st.markdown("<hr style='margin:20px 0 16px;'>", unsafe_allow_html=True)
        if st.button("🚪  Log Out", use_container_width=True, key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.page = "Dashboard"
            st.rerun()


# ─────────────────────────────────────────────────────────
#  PAGES
# ─────────────────────────────────────────────────────────
def page_dashboard():
    st.markdown("""
    <div class="hero-header">
        <span class="hero-icon">🏨</span>
        <div>
            <h1>Hotel Operations Dashboard</h1>
            <p>Manage hotels, rooms, amenities, customers and bookings from one place.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    hotels    = view_hotels()
    rooms     = view_rooms()
    amenities = view_amenities()
    customers = view_customers()
    bookings  = view_bookings()

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, icon, val, label in [
        (c1, "🏨", len(hotels),    "Hotels"),
        (c2, "🛏️", len(rooms),     "Rooms"),
        (c3, "🌟", len(amenities), "Amenities"),
        (c4, "👤", len(customers), "Customers"),
        (c5, "📋", len(bookings),  "Bookings"),
    ]:
        with col:
            st.markdown(metric_card(icon, val, label), unsafe_allow_html=True)

    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        section_header("🏨", "Recent Hotels")
        if hotels:
            import pandas as pd
            df = pd.DataFrame(hotels)[["name", "location", "rating"]].head(5)
            df.columns = ["Name", "Location", "Rating ⭐"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">🏨</div><div class="es-text">No hotels registered yet</div></div>', unsafe_allow_html=True)

    with col_right:
        section_header("📋", "Recent Bookings")
        if bookings:
            import pandas as pd
            df = pd.DataFrame(bookings)[["customer", "room_no", "date"]].head(5)
            df.columns = ["Customer", "Room No.", "Check-in Date"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">📋</div><div class="es-text">No bookings yet</div></div>', unsafe_allow_html=True)


def page_hotels():
    section_header("🏨", "Hotels Registry")

    tab_view, tab_add = st.tabs(["📋  View All Hotels", "➕  Register Hotel"])

    with tab_view:
        hotels = view_hotels()
        if hotels:
            import pandas as pd
            df = pd.DataFrame(hotels)[["name", "location", "rating"]]
            df.columns = ["Hotel Name", "Location", "Rating ⭐"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(hotels)} hotel(s) registered")
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">🏨</div><div class="es-text">No hotels found</div><div class="es-sub">Use the tab above to register your first hotel.</div></div>', unsafe_allow_html=True)

    with tab_add:
        st.markdown('<div class="form-title">Hotel Details</div>', unsafe_allow_html=True)
        with st.form("add_hotel_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Hotel Name *", placeholder="e.g. Grand Hyatt")
            with col2:
                location = st.text_input("Location *", placeholder="e.g. New York, USA")
            rating = st.slider("Star Rating", min_value=1.0, max_value=5.0, step=0.5, value=3.0)
            submitted = st.form_submit_button("🏨  Register Hotel", use_container_width=True)
            if submitted:
                if not name or not location:
                    st.error("Hotel name and location are required.")
                else:
                    result = add_hotel(name, location, rating)
                    if result:
                        st.success(f"✅  **{name}** has been registered successfully!")
                        st.rerun()
                    else:
                        st.error("❌  Failed to register hotel. Please check the details and try again.")


def page_rooms():
    section_header("🛏️", "Room Management")

    tab_view, tab_add = st.tabs(["📋  View All Rooms", "➕  Add Room"])

    with tab_view:
        rooms = view_rooms()
        if rooms:
            import pandas as pd
            df = pd.DataFrame(rooms)[["room_no", "type", "price"]]
            df.columns = ["Room No.", "Type", "Price / Night (₹)"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(rooms)} room(s) listed")
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">🛏️</div><div class="es-text">No rooms found</div><div class="es-sub">Add your first room using the tab above.</div></div>', unsafe_allow_html=True)

    with tab_add:
        st.markdown('<div class="form-title">Room Details</div>', unsafe_allow_html=True)
        with st.form("add_room_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                room_no = st.text_input("Room Number *", placeholder="e.g. 101")
            with col2:
                room_type = st.selectbox("Room Type *", ["Single", "Double", "Suite", "Deluxe", "Presidential Suite", "Penthouse"])
            price = st.number_input("Price Per Night (₹) *", min_value=0.0, step=100.0, value=2000.0)
            submitted = st.form_submit_button("🛏️  Add Room", use_container_width=True)
            if submitted:
                if not room_no:
                    st.error("Room number is required.")
                else:
                    result = add_room(room_no, room_type, price)
                    if result:
                        st.success(f"✅  Room **{room_no}** ({room_type}) added at ₹{price:,.0f}/night!")
                        st.rerun()
                    else:
                        st.error("❌  Failed to add room.")


def page_amenities():
    section_header("🌟", "Amenities Management")

    tab_view, tab_add = st.tabs(["📋  View Amenities", "➕  Add Amenity"])

    with tab_view:
        amenities = view_amenities()
        if amenities:
            import pandas as pd
            df = pd.DataFrame(amenities)[["name", "description"]]
            df.columns = ["Amenity Name", "Description"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(amenities)} amenity/amenities available")
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">🌟</div><div class="es-text">No amenities found</div><div class="es-sub">Add your first amenity using the tab above.</div></div>', unsafe_allow_html=True)

    with tab_add:
        st.markdown('<div class="form-title">Amenity Details</div>', unsafe_allow_html=True)
        with st.form("add_amenity_form", clear_on_submit=True):
            name = st.text_input("Amenity Name *", placeholder="e.g. Rooftop Swimming Pool")
            description = st.text_area("Description *", placeholder="Describe the amenity in detail…", height=120)
            submitted = st.form_submit_button("🌟  Add Amenity", use_container_width=True)
            if submitted:
                if not name or not description:
                    st.error("Both name and description are required.")
                else:
                    result = add_amenity(name, description)
                    if result:
                        st.success(f"✅  Amenity **{name}** added!")
                        st.rerun()
                    else:
                        st.error("❌  Failed to add amenity.")


def page_customers():
    section_header("👤", "Customer Directory")

    tab_view, tab_add = st.tabs(["📋  All Customers", "➕  Register Customer"])

    with tab_view:
        customers = view_customers()
        if customers:
            import pandas as pd
            df = pd.DataFrame(customers)[["name", "contact", "id"]]
            df.columns = ["Full Name", "Contact", "Gov. ID / Passport"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(customers)} customer(s) registered")
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">👤</div><div class="es-text">No customers found</div><div class="es-sub">Register your first customer using the tab above.</div></div>', unsafe_allow_html=True)

    with tab_add:
        st.markdown('<div class="form-title">Customer Details</div>', unsafe_allow_html=True)
        with st.form("add_customer_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma")
            with col2:
                contact = st.text_input("Contact Number *", placeholder="e.g. +91-9876543210")
            customer_id = st.text_input("Government ID / Passport No. *", placeholder="e.g. ABCDE1234F")
            submitted = st.form_submit_button("👤  Register Customer", use_container_width=True)
            if submitted:
                if not name or not contact or not customer_id:
                    st.error("All fields are required.")
                else:
                    result = add_customer(name, contact, customer_id)
                    if result:
                        st.success(f"✅  Customer **{name}** registered!")
                        st.rerun()
                    else:
                        st.error("❌  Failed to register customer.")


def page_bookings():
    section_header("📋", "Booking Management")

    tab_view, tab_add = st.tabs(["📋  Active Bookings", "➕  New Booking"])

    with tab_view:
        bookings = view_bookings()
        if bookings:
            import pandas as pd
            df = pd.DataFrame(bookings)[["customer", "room_no", "date"]]
            df.columns = ["Customer Name", "Room No.", "Check-in Date"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(bookings)} active booking(s)")
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">📋</div><div class="es-text">No bookings found</div><div class="es-sub">Create a new booking using the tab above.</div></div>', unsafe_allow_html=True)

    with tab_add:
        st.markdown('<div class="form-title">Booking Details</div>', unsafe_allow_html=True)

        # Pre-fill selectors from DB if data available
        customers_list = [c.get("name", "") for c in view_customers()]
        rooms_list     = [r.get("room_no", "") for r in view_rooms()]

        with st.form("add_booking_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                if customers_list:
                    customer = st.selectbox("Customer *", options=customers_list)
                else:
                    customer = st.text_input("Customer Name *", placeholder="Enter customer name")
            with col2:
                if rooms_list:
                    room_no = st.selectbox("Room Number *", options=rooms_list)
                else:
                    room_no = st.text_input("Room Number *", placeholder="e.g. 101")

            import datetime
            checkin_date = st.date_input("Check-in Date *", value=datetime.date.today())
            submitted = st.form_submit_button("📋  Confirm Booking", use_container_width=True)
            if submitted:
                if not customer or not room_no:
                    st.error("Customer and room fields are required.")
                else:
                    result = add_booking(customer, str(room_no), str(checkin_date))
                    if result:
                        st.success(f"✅  Booking confirmed for **{customer}** in Room **{room_no}** on **{checkin_date}**!")
                        st.rerun()
                    else:
                        st.error("❌  Failed to create booking.")


# ─────────────────────────────────────────────────────────
#  MAIN ROUTER
# ─────────────────────────────────────────────────────────
def main():
    if not st.session_state.authenticated:
        render_auth()
        return

    render_sidebar()

    page = st.session_state.page
    if page == "Dashboard":
        page_dashboard()
    elif page == "Hotels":
        page_hotels()
    elif page == "Rooms":
        page_rooms()
    elif page == "Amenities":
        page_amenities()
    elif page == "Customers":
        page_customers()
    elif page == "Bookings":
        page_bookings()


if __name__ == "__main__":
    main()
