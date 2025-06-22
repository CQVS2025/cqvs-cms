import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Load Data ---
@st.cache_data
def load_data():
    scans = pd.read_csv("Scans data - Sheet1.csv")
    vehicles = pd.read_csv("Vehicles data - Sheet1.csv")
    refills = pd.read_csv("refills data - Sheet1.csv")
    clients = pd.read_csv("clients_contacts/SE - QLD - Sites 20d6ed160c548001939bd5fd1fe1f212.csv")
    contacts = pd.read_csv("parsed_contacts.csv")
    return scans, vehicles, refills, clients, contacts

scans, vehicles, refills, clients, contacts = load_data()

# --- Sidebar Navigation ---
st.sidebar.title("CMS Navigation")
tabs = ["Dashboard", "Vehicles", "Scans", "Refills", "Clients", "Contacts", "Tasks"]
page = st.sidebar.radio("Go to", tabs)

# --- Dashboard Tab ---
if page == "Dashboard":
    st.title("📊 Wash Dashboard with Alerts")
    site_filter = st.selectbox("Filter by Site", ["All"] + sorted(scans["Site"].dropna().unique()))
    filtered = scans.copy()
    if site_filter != "All":
        filtered = filtered[filtered["Site"] == site_filter]

    filtered['Created'] = pd.to_datetime(filtered['Created'], errors='coerce')
    recent = filtered[filtered['Created'] > (datetime.now() - timedelta(days=7))]

    st.subheader("Washes in Past 7 Days")
    st.metric("Wash Count", len(recent))
    st.bar_chart(recent['Vehicle Name'].value_counts())

    st.subheader("⚠️ Missed Wash Alerts")
    missed = filtered.groupby('Vehicle Name')['Created'].max()
    inactive = missed[missed < datetime.now() - timedelta(days=3)]
    for v, t in inactive.items():
        st.warning(f"{v} last washed on {t.strftime('%Y-%m-%d')}")

# --- Vehicles Tab ---
elif page == "Vehicles":
    st.title("🚛 Vehicle Directory")
    st.dataframe(vehicles)
    with st.expander("Upload Vehicle Photo"):
        uploaded_image = st.file_uploader("Choose a vehicle image", type=["jpg", "png"])
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Vehicle Photo", use_column_width=True)

# --- Scans Tab ---
elif page == "Scans":
    st.title("🧼 Wash Logs")
    st.dataframe(scans)
    st.line_chart(scans['Wash Time'].fillna(0).head(50))

# --- Refills Tab ---
elif page == "Refills":
    st.title("🧪 Refill Deliveries")
    st.dataframe(refills)
    st.subheader("⚠️ Refill Gaps")
    refills['Parsed Date'] = pd.to_datetime(refills['Date'], errors='coerce')
    recent_refill = refills.groupby('Site')['Parsed Date'].max()
    alert_sites = recent_refill[recent_refill < datetime.now() - timedelta(days=30)]
    for site, date in alert_sites.items():
        st.error(f"No refill at {site} since {date.strftime('%Y-%m-%d')}")

    with st.expander("Upload Delivery PDF"):
        pdf = st.file_uploader("Attach PDF", type=["pdf"])
        if pdf:
            st.success("PDF uploaded (simulated).")

# --- Clients Tab ---
elif page == "Clients":
    st.title("🏢 Client Sites")
    st.dataframe(clients[['Company', 'Site', 'Location', 'Phone Number', 'Status', 'Notes']])

# --- Contacts Tab ---
elif page == "Contacts":
    st.title("📇 Contacts")
    st.dataframe(contacts)

# --- Tasks Tab ---
elif page == "Tasks":
    st.title("✅ Task Tracker")
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    with st.form("task_form"):
        new_task = st.text_input("New Task")
        submitted = st.form_submit_button("Add Task")
        if submitted and new_task:
            st.session_state.tasks.append({"task": new_task, "done": False})

    for i, t in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([0.8, 0.2])
        done = col1.checkbox(t["task"], value=t["done"], key=f"task_{i}")
        st.session_state.tasks[i]["done"] = done
        if col2.button("❌", key=f"delete_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()
