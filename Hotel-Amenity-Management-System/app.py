import streamlit as st
import sys
import os

# Allow relative imports from the same directory
sys.path.insert(0, os.path.dirname(__file__))

from auth import authenticate_user, register_user
from hotel import add_hotel, view_hotels, update_hotel
from room import add_room, view_rooms
from amenities import add_amenity, view_amenities
from customers import add_customer, view_customers
from booking import add_booking, view_bookings, cancel_booking
from database import client

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


def get_db_status():
    try:
        client.admin.command('ping')
        return True
    except Exception:
        return False

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
        """, unsafe_allow_html=True)
        
        # MongoDB Live Monitor
        db_status = get_db_status()
        status_color = "#10b981" if db_status else "#ef4444"
        status_text = "Online" if db_status else "Offline"
        
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.6); padding: 12px 16px; border-radius: 10px; margin: 10px 4px 24px; border: 1px solid rgba(99,102,241,0.2); display: flex; align-items: center; justify-content: space-between;">
            <div style="font-size: 0.82rem; color: #cbd5e1; font-weight: 600; display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 1rem;">🍃</span> MongoDB Data
            </div>
            <div style="display: flex; align-items: center; gap: 6px; background: rgba(0,0,0,0.2); padding: 4px 10px; border-radius: 20px;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: {status_color}; box-shadow: 0 0 8px {status_color}; animation: pulse 2s infinite;"></div>
                <div style="font-size: 0.72rem; color: {status_color}; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">{status_text}</div>
            </div>
        </div>
        <style>
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        </style>
        <div style="color:#475569;font-size:0.72rem;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;padding: 0 4px 8px;">Navigation</div>
        """, unsafe_allow_html=True)

        nav_button("Dashboard",          "📊", "Dashboard")
        nav_button("Hotels",             "🏨", "Hotels")
        nav_button("Rooms",              "🛏️", "Rooms")
        nav_button("Amenities",          "🌟", "Amenities")
        is_admin = st.session_state.get("username", "").lower() == "admin"
        if is_admin:
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

    is_admin = st.session_state.get("username", "").lower() == "admin"
    current_username = st.session_state.get("username", "")

    if not is_admin:
        bookings = [b for b in bookings if b.get("booked_by", "") == current_username or b.get("customer", "") == current_username or b.get("customer_id", "") == current_username]

    metrics = [
        ("🏨", len(hotels),    "Hotels"),
        ("🛏️", len(view_rooms()),     "Rooms"),
        ("🌟", len(amenities), "Amenities"),
    ]
    if is_admin:
        metrics.append(("👤", len(customers), "Customers"))
    metrics.append(("📋", len(bookings),  "Bookings" if is_admin else "My Bookings"))

    cols = st.columns(len(metrics))
    for col, (icon, val, label) in zip(cols, metrics):
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
            
            customer_map = {}
            for c in view_customers():
                real_name = c.get("name") or c.get("customer_name") or "Unknown"
                for key in ["id", "customer_id", "email_id", "email", "name", "customer_name"]:
                    if c.get(key):
                        customer_map[str(c.get(key))] = real_name

            mapped = []
            for b in bookings:
                raw_c = str(b.get("customer") or b.get("customer_id", "Unknown"))
                g_name = customer_map.get(raw_c, raw_c)
                mapped.append({
                    "Customer": g_name,
                    "Room No.": b.get("room_no") or b.get("room_number", "Unknown"),
                    "Check-in Date": b.get("date") or b.get("check_in", "Unknown"),
                    "Check-out Date": b.get("checkout_date", "N/A")
                })
            df = pd.DataFrame(mapped).head(5)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">📋</div><div class="es-text">No bookings yet</div></div>', unsafe_allow_html=True)


def page_hotels():
    section_header("🏨", "Hotels Registry")

    is_admin = st.session_state.get("username", "").lower() == "admin"
    if is_admin:
        tab_view, tab_add, tab_update = st.tabs(["📋  View All Hotels", "➕  Register Hotel", "✏️  Update Hotel"])
    else:
        tab_view, = st.tabs(["📋  View All Hotels"])

    with tab_view:
        hotels = view_hotels()
        if hotels:
            import pandas as pd
            import datetime
            locations = ["Anywhere"] + sorted(list(set([h.get("location", "") for h in hotels if h.get("location")])))
            
            # Booking-style Hero Banner & Search Console
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 36px 40px; border-radius: 16px; margin-bottom: 28px; border: 1px solid rgba(99,102,241,0.25); box-shadow: 0 15px 40px rgba(0,0,0,0.4); position: relative; overflow: hidden;">
                <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%); border-radius: 50%;"></div>
                <h2 style="color: #f8fafc; font-size: 2.2rem; margin-top: 0; margin-bottom: 12px; font-weight: 800; letter-spacing: -0.5px;">Find your next stay</h2>
                <p style="color: #94a3b8; font-size: 1.05rem; margin-bottom: 26px; font-weight: 400;">Search competitive prices on hotels, homes, and much more...</p>
            """, unsafe_allow_html=True)
            
            st.markdown("##### 🔍 Search Criteria")
            col_a, col_b = st.columns([1.5, 1])
            with col_a:
                filter_location = st.selectbox("📍 Destination / Location", locations)
            with col_b:
                filter_rating = st.selectbox("⭐ Min. Rating", ["Any", "3+ Stars", "4+ Stars", "5 Stars"])
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Filter Application Logic
            filtered_hotels = hotels
            if filter_location != "Anywhere":
                filtered_hotels = [h for h in filtered_hotels if h.get("location") == filter_location]
            
            if filter_rating != "Any":
                min_stars = int(filter_rating[0])
                filtered_hotels = [h for h in filtered_hotels if float(h.get("rating", 0)) >= min_stars]
                
            st.markdown(f"<h3 style='color: #f1f5f9; font-size: 1.4rem; margin-bottom: 16px;'>Properties match your search</h3>", unsafe_allow_html=True)
            
            if filtered_hotels:
                import urllib.parse
                import hashlib
                customers_list = sorted(list(set([c.get("name") for c in view_customers() if c.get("name")])))
                current_username = st.session_state.get("username", "")
                
                # Fetch all active bookings to see which rooms are taken
                all_bookings = view_bookings()
                booked_rooms_set = set(str(b.get("room_no") or b.get("room_number", "")) for b in all_bookings)

                for i, hotel in enumerate(filtered_hotels):
                    h_name = hotel.get('name', 'Unknown')
                    h_loc = hotel.get('location', 'Unknown')
                    h_rate = hotel.get('rating', 0.0)
                    
                    rooms_list = view_rooms(hotel_name=h_name)
                    
                    # Generate a unique stable seed based on the hotel name using md5 to avoid collisions
                    seed = int(hashlib.md5(h_name.encode('utf-8')).hexdigest(), 16) % 10000 + 1
                    # Use loremflickr to fetch a unique, stable luxury hotel image
                    img_url = f"https://loremflickr.com/1200/500/hotel,luxury?lock={seed}"
                    
                    # Hotel Listing Card
                    with st.container():
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 0; margin-bottom: 20px; transition: transform 0.2s, background 0.2s; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);">
                            <div style="height: 250px; width: 100%; background: url('{img_url}') center/cover no-repeat; border-bottom: 1px solid rgba(255,255,255,0.1);"></div>
                            <div style="padding: 24px;">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 16px;">
                                    <div>
                                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                                            <h3 style="margin: 0; color: #f8fafc; font-size: 1.5rem; font-weight: 700;">{h_name}</h3>
                                            <span style="background: rgba(16,185,129,0.2); color: #6ee7b7; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">Featured</span>
                                        </div>
                                        <div style="color: #94a3b8; font-size: 0.9rem; display: flex; align-items: center; gap: 6px;">
                                            <span>📍</span> <a href="#" style="color: #6366f1; text-decoration: none;">{h_loc}</a> • <span style="color: #cbd5e1;">Show on map</span>
                                        </div>
                                    </div>
                                    <div style="display: flex; flex-direction: column; align-items: flex-end;">
                                        <div style="display: flex; align-items: center; gap: 8px;">
                                            <div style="text-align: right;">
                                                <div style="color: #f1f5f9; font-weight: 700; font-size: 0.9rem;">Excellent</div>
                                                <div style="color: #64748b; font-size: 0.75rem;">Guest reviews</div>
                                            </div>
                                            <div style="background: #4f46e5; color: white; padding: 6px 10px; border-radius: 8px 8px 8px 0; font-weight: 800; font-size: 1rem;">{h_rate}</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander(f"🛒 Check Availability & Book — {h_name}"):
                            st.markdown("#### Select Rooms to Book")
                            
                            with st.form(f"form_book_{i}"):
                                selected_rooms = []
                                if rooms_list:
                                    for j, r in enumerate(rooms_list):
                                        r_no = str(r.get("room_no"))
                                        r_type = r.get("type", "Unknown")
                                        r_price = r.get("price", 0.0)
                                        is_booked = r_no in booked_rooms_set
                                        
                                        if is_booked:
                                            st.markdown(f"<p style='color: #475569; margin: 4px 0 8px 30px; font-size: 0.95rem;'>🛏️ <s><b>Room {r_no}</b> ({r_type}) — ₹{r_price}/night</s> <span style='color: #ef4444; font-size: 0.8rem; font-weight: 600; margin-left: 6px;'>[Already Taken]</span></p>", unsafe_allow_html=True)
                                        else:
                                            room_label = f"🛏️ **Room {r_no}** ({r_type}) — ₹{r_price}/night"
                                            if st.checkbox(room_label, key=f"chk_room_{i}_{j}"):
                                                selected_rooms.append(r_no)
                                else:
                                    st.info("No rooms available currently.")
                                
                                st.markdown("#### 👤 Primary Guest Details")
                                if is_admin and customers_list:
                                    customer = st.selectbox("Select Customer from Directory", options=["-- Select --"] + customers_list, key=f"cust_{i}")
                                else:
                                    customer = st.text_input("Guest Name", placeholder="Enter actual guest name", key=f"inp_cust_{i}")
                                    
                                # Prevent booking more than 4 days ahead
                                today = datetime.date.today()
                                max_allowed = today + datetime.timedelta(days=4)
                                
                                default_checkin = today
                                
                                col_d1, col_d2 = st.columns(2)
                                with col_d1:
                                    checkin_date = st.date_input("Check-in Date", value=default_checkin, min_value=today, max_value=max_allowed, key=f"date_{i}")
                                with col_d2:
                                    # Default checkout to check-in + 1 day, bounded by max_allowed if needed
                                    default_checkout = min(checkin_date + datetime.timedelta(days=1), max_allowed) if checkin_date < max_allowed else checkin_date
                                    checkout_date = st.date_input("Check-out Date", value=default_checkout, min_value=checkin_date, max_value=max_allowed, key=f"cout_{i}")
                                
                                submitted = st.form_submit_button("💳 Confirm Secure Booking", use_container_width=True)
                                if submitted:
                                    if not selected_rooms:
                                        st.error("Please select at least one room to book.")
                                    elif (is_admin and customers_list and customer == "-- Select --") or not customer:
                                        st.error("Please provide guest details.")
                                    else:
                                        success_count = 0
                                        for room_no in selected_rooms:
                                            result = add_booking(customer or current_username, str(room_no), str(checkin_date), str(checkout_date), booked_by=current_username)
                                            if result:
                                                success_count += 1
                                        if success_count == len(selected_rooms):
                                            st.success(f"✅ Successfully booked {success_count} room(s) for {customer}!")
                                            st.balloons()
                                        elif success_count > 0:
                                            st.warning(f"⚠️ Partially booked {success_count} out of {len(selected_rooms)} rooms.")
                                        else:
                                            st.error("❌ Failed to create booking(s).")
                        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            else:
                st.info("No hotels match your filters.")
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">🏨</div><div class="es-text">No properties found</div><div class="es-sub">Use the tab above to list your first property.</div></div>', unsafe_allow_html=True)

    if is_admin:
        with tab_add:
            st.markdown('<div class="form-title">Hotel Details</div>', unsafe_allow_html=True)
            with st.form("add_hotel_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Hotel Name *", placeholder="e.g. Grand Hyatt")
                with col2:
                    location = st.text_input("Location *", placeholder="e.g. New York, USA")
                rating = st.slider("Star Rating", min_value=1.0, max_value=5.0, step=0.1, value=3.0)
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
                            
        with tab_update:
            st.markdown('<div class="form-title">Update Hotel Details</div>', unsafe_allow_html=True)
            hotels_list = view_hotels()
            if hotels_list:
                hotel_names = sorted(list(set([h.get("name", "") for h in hotels_list if h.get("name")])))
                selected_hotel_name = st.selectbox("Select Hotel to Update", options=["-- Select Hotel --"] + hotel_names)
                
                if selected_hotel_name != "-- Select Hotel --":
                    # Get the current details to prefill
                    selected_hotel = next((h for h in hotels_list if h.get("name") == selected_hotel_name), None)
                    if selected_hotel:
                        with st.form("update_hotel_form", clear_on_submit=False):
                            st.markdown(f"**Updating:** {selected_hotel_name}")
                            new_location = st.text_input("New Location (leave blank to keep current)", placeholder=selected_hotel.get("location", ""))
                            curr_rating = selected_hotel.get("rating", 3.0)
                            new_rating = st.slider("New Star Rating", min_value=1.0, max_value=5.0, step=0.1, value=float(curr_rating))
                            
                            submitted_update = st.form_submit_button("✏️  Update Hotel", use_container_width=True)
                            if submitted_update:
                                loc_to_update = new_location if new_location.strip() else None
                                
                                result = update_hotel(selected_hotel_name, location=loc_to_update, rating=new_rating)
                                if result:
                                    st.success(f"✅  **{selected_hotel_name}** has been updated successfully!")
                                    st.rerun()
                                else:
                                    st.error("❌  Failed to update hotel. Please try again.")
            else:
                st.info("No hotels registered yet to update.")

def page_rooms():
    section_header("🛏️", "Room Management")

    is_admin = st.session_state.get("username", "").lower() == "admin"
    if is_admin:
        tab_view, tab_add = st.tabs(["📋  View All Rooms", "➕  Add Room"])
    else:
        tab_view, = st.tabs(["📋  View All Rooms"])

    with tab_view:
        rooms = view_rooms()
        if rooms:
            import pandas as pd
            df = pd.DataFrame(rooms)[["hotel_name", "room_no", "type", "price"]]
            df.columns = ["Hotel", "Room No.", "Type", "Price / Night (₹)"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(rooms)} room(s) listed")
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">🛏️</div><div class="es-text">No rooms found</div><div class="es-sub">Add your first room using the tab above.</div></div>', unsafe_allow_html=True)

    if is_admin:
        with tab_add:
            st.markdown('<div class="form-title">Room Details</div>', unsafe_allow_html=True)
            with st.form("add_room_form", clear_on_submit=True):
                col0, col1, col2 = st.columns([1.5, 1, 1])
                
                hotels_av = [h.get("name") for h in view_hotels() if h.get("name")]
                with col0:
                    selected_hotel = st.selectbox("Hotel *", options=sorted(hotels_av) if hotels_av else ["-- None --"])
                with col1:
                    room_no = st.text_input("Room Number *", placeholder="e.g. 101")
                with col2:
                    room_type = st.selectbox("Room Type *", ["Single", "Double", "Suite", "Deluxe", "Presidential Suite", "Penthouse"])
                price = st.number_input("Price Per Night (₹) *", min_value=0.0, step=100.0, value=2000.0)
                submitted = st.form_submit_button("🛏️  Add Room", use_container_width=True)
                if submitted:
                    if not room_no or not selected_hotel or selected_hotel == "-- None --":
                        st.error("Hotel and Room number are required.")
                    else:
                        result = add_room(selected_hotel, room_no, room_type, price)
                        if result == "duplicate":
                            st.warning(f"⚠️  Room {room_no} already exists in {selected_hotel}! Please enter a unique room number.")
                        elif result:
                            st.success(f"✅  Room **{room_no}** ({room_type}) added to {selected_hotel} at ₹{price:,.0f}/night!")
                            st.rerun()
                        else:
                            st.error("❌  Failed to add room.")


def page_amenities():
    section_header("🌟", "Amenities Management")

    is_admin = st.session_state.get("username", "").lower() == "admin"
    if is_admin:
        tab_view, tab_add = st.tabs(["📋  View Amenities", "➕  Add Amenity"])
    else:
        tab_view, = st.tabs(["📋  View Amenities"])

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

    if is_admin:
        with tab_add:
            st.markdown('<div class="form-title">Amenity Details</div>', unsafe_allow_html=True)

            predefined_amenities = {
                "Free Wi-Fi": "High-speed internet access available throughout the property.",
                "Swimming Pool": "Outdoor/Indoor temperature controlled swimming pool.",
                "Gym / Fitness Center": "Fully equipped modern fitness center open 24/7.",
                "Spa & Wellness": "Luxury spa offering massages, sauna, and beauty treatments.",
                "Restaurant & Bar": "In-house dining and bar featuring international cuisine.",
                "Room Service": "24-hour room service for food, beverages, and essentials.",
                "Parking": "Secure and monitored on-site parking for guests.",
                "Airport Shuttle": "Complimentary pickup and drop-off to the nearest airport.",
                "Conference Room": "Fully equipped meeting rooms for business conferences.",
                "Laundry Service": "Same-day laundry, ironing, and dry cleaning services."
            }

            # Placing selectbox outside the form so it dynamically updates the form fields
            options = ["-- Custom Amenity / Manual Entry --"] + list(predefined_amenities.keys())
            selected_option = st.selectbox("Choose Predefined Facility / Amenity", options, help="Select a predefined facility to auto-fill the details, or create your own.")

            with st.form("add_amenity_form", clear_on_submit=True):
                if selected_option != "-- Custom Amenity / Manual Entry --":
                    name = st.text_input("Amenity Name *", value=selected_option)
                    description = st.text_area("Description *", value=predefined_amenities[selected_option], height=120)
                else:
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

    is_admin = st.session_state.get("username", "").lower() == "admin"
    if is_admin:
        tab_view, tab_add = st.tabs(["📋  All Customers", "➕  Register Customer"])
    else:
        tab_view, = st.tabs(["📋  All Customers"])

    with tab_view:
        customers = view_customers()
        if customers:
            import pandas as pd
            mapped_customers = []
            for c in customers:
                mapped_customers.append({
                    "Full Name": c.get("name") or c.get("customer_name", "N/A"),
                    "Contact": c.get("contact") or c.get("phone", "N/A"),
                    "Email ID": c.get("email_id") or c.get("email") or c.get("id", "N/A"),
                    "City": c.get("city", "N/A")
                })
            df = pd.DataFrame(mapped_customers)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(customers)} customer(s) registered")
        else:
            st.markdown('<div class="empty-state"><div class="es-icon">👤</div><div class="es-text">No customers found</div><div class="es-sub">Register your first customer using the tab above.</div></div>', unsafe_allow_html=True)

    if is_admin:
        with tab_add:
            st.markdown('<div class="form-title">Customer Details</div>', unsafe_allow_html=True)
            with st.form("add_customer_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma")
                with col2:
                    contact = st.text_input("Contact Number *", placeholder="e.g. +91-9876543210")
                email_id = st.text_input("Email ID *", placeholder="e.g. user@example.com")
                city = st.text_input("City *", placeholder="e.g. Mumbai")
                submitted = st.form_submit_button("👤  Register Customer", use_container_width=True)
                if submitted:
                    if not name or not contact or not email_id or not city:
                        st.error("All fields are required.")
                    else:
                        result = add_customer(name, contact, email_id, city)
                        if result:
                            st.success(f"✅  Customer **{name}** registered!")
                            st.rerun()
                        else:
                            st.error("❌  Failed to register customer.")

def page_bookings():
    section_header("📋", "Bookings & Reservations" if st.session_state.get("username", "").lower() == "admin" else "My Bookings")

    bookings = view_bookings()
    is_admin = st.session_state.get("username", "").lower() == "admin"
    current_username = st.session_state.get("username", "")

    if not is_admin:
        bookings = [b for b in bookings if b.get("booked_by", "") == current_username or b.get("customer", "") == current_username or b.get("customer_id", "") == current_username]

    if bookings:
        import pandas as pd
        
        customer_map = {}
        for c in view_customers():
            real_name = c.get("name") or c.get("customer_name") or "Unknown"
            for key in ["id", "customer_id", "email_id", "email", "name", "customer_name"]:
                if c.get(key):
                    customer_map[str(c.get(key))] = real_name

        mapped_bookings = []
        cancellation_options = {}
        for b in bookings:
            raw_c = str(b.get("customer") or b.get("customer_id", "Unknown"))
            g_name = customer_map.get(raw_c, raw_c)
            r_no = b.get("room_no") or b.get("room_number", "Unknown")
            c_in = b.get("date") or b.get("check_in", "Unknown")
            c_out = b.get("checkout_date", "N/A")
            b_id = str(b.get("_id", ""))
            
            mapped_bookings.append({
                "ID": b_id,
                "Guest Name": g_name,
                "Room Number": r_no,
                "Check-in Date": c_in,
                "Check-out Date": c_out
            })
            
            if b_id:
                label = f"[{b_id[-4:]}] {g_name} — Room {r_no} ({c_in})"
                cancellation_options[label] = b_id

        df = pd.DataFrame(mapped_bookings)
        
        st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)
        st.caption(f"Total: {len(bookings)} reservation(s) in system")
        
        st.markdown("<hr style='margin:24px 0; border-color: rgba(99,102,241,0.2);'>", unsafe_allow_html=True)
        st.markdown("#### Manage Reservations")
        with st.expander("🗑️ Cancel a Booking"):
            with st.form("cancel_booking_form"):
                selected_label = st.selectbox("Select Booking to Cancel", options=["-- Select --"] + list(cancellation_options.keys()))
                submitted = st.form_submit_button("Cancel Booking")
                if submitted:
                    if selected_label == "-- Select --":
                        st.error("Please select a booking to cancel.")
                    else:
                        booking_id_to_cancel = cancellation_options[selected_label]
                        res = cancel_booking(booking_id_to_cancel)
                        if res and res.deleted_count > 0:
                            st.success("✅ Booking cancelled successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to cancel booking. It may have already been deleted.")
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">📋</div>
            <div class="es-text">No active bookings</div>
            <div class="es-sub">Reservations will appear here once guests book a room through the Hotels registry.</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
#  MAIN ROUTER
# ─────────────────────────────────────────────────────────
def main():
    if not st.session_state.authenticated:
        render_auth()
    else:
        render_sidebar()
        
        # Route to the selected page
        if st.session_state.page == "Dashboard":
            page_dashboard()
        elif st.session_state.page == "Hotels":
            page_hotels()
        elif st.session_state.page == "Rooms":
            page_rooms()
        elif st.session_state.page == "Amenities":
            page_amenities()
        elif st.session_state.page == "Customers":
            # Extra security layer for the admin-only customer page
            if st.session_state.get("username", "").lower() == "admin":
                page_customers()
            else:
                st.error("Access Denied: You do not have permission to view the Customer Directory.")
                st.session_state.page = "Dashboard"
                st.rerun()
        elif st.session_state.page == "Bookings":
            page_bookings()

if __name__ == "__main__":
    main()