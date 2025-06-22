
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="CQVS CMS Demo", layout="wide")

# Simulated data
sites_data = pd.DataFrame([
    {"Company": "ABC Pty Ltd", "Site": "Burleigh Plant", "Address": "157 Cowell Dr", "Contact": "Jane Smith", "Phone": "0400 123 456", "Email": "jane@abc.com", "Notes": "Bitumen tank access issue"},
])
contacts_data = pd.DataFrame([
    {"Name": "Jane Smith", "Role": "Plant Manager", "Mobile": "0400 123 456", "Email": "jane@abc.com", "Company": "ABC Pty Ltd", "Notes": "Prefers email contact"},
])
clients_data = pd.DataFrame([
    {"Company": "ABC Pty Ltd", "Type": "Contractor", "Notes": "Regular client"},
])
jobs_data = pd.DataFrame([
    {"Job #": "J-102", "Client": "ABC Pty Ltd", "Site": "Burleigh Plant", "Status": "In Progress", "Assigned To": "Jonny", "Scope": "Pump calibration and test", "Notes": "Waiting on part"},
])
tasks_data = pd.DataFrame([
    {"Task": "Call Jane re: access", "Assigned To": "Jonny", "Due Date": "2025-06-24", "Status": "To Do"},
])

# Sidebar
st.sidebar.title("CMS Sections")
section = st.sidebar.radio("Go to", ["Sites", "Contacts", "Clients", "Jobs", "Tasks", "Files (Coming Soon)"])

# Sites
if section == "Sites":
    st.title("📍 Sites")
    st.dataframe(sites_data)
    with st.expander("Add New Site"):
        company = st.text_input("Company")
        site = st.text_input("Site Name")
        address = st.text_input("Address")
        contact = st.text_input("Contact Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        notes = st.text_area("Notes")
        if st.button("Save Site"):
            st.success("Site saved (mock action)")

# Contacts
elif section == "Contacts":
    st.title("👥 Contacts")
    st.dataframe(contacts_data)
    with st.expander("Add New Contact"):
        name = st.text_input("Full Name")
        role = st.text_input("Role")
        mobile = st.text_input("Mobile")
        email = st.text_input("Email")
        company = st.text_input("Company")
        notes = st.text_area("Notes")
        if st.button("Save Contact"):
            st.success("Contact saved (mock action)")

# Clients
elif section == "Clients":
    st.title("🏢 Clients")
    st.dataframe(clients_data)
    with st.expander("Add New Client"):
        cname = st.text_input("Client Name")
        ctype = st.selectbox("Type", ["Contractor", "Principal", "Supplier", "Other"])
        cnotes = st.text_area("Notes")
        if st.button("Save Client"):
            st.success("Client saved (mock action)")

# Jobs
elif section == "Jobs":
    st.title("🛠️ Jobs")
    st.dataframe(jobs_data)
    with st.expander("Add New Job"):
        job_id = st.text_input("Job Number")
        client = st.text_input("Client")
        site = st.text_input("Site")
        status = st.selectbox("Status", ["Quote", "In Progress", "Completed"])
        assigned = st.text_input("Assigned To")
        scope = st.text_area("Scope of Work")
        notes = st.text_area("Notes")
        if st.button("Save Job"):
            st.success("Job saved (mock action)")

# Tasks
elif section == "Tasks":
    st.title("✅ Tasks / To-Do")
    st.dataframe(tasks_data)
    with st.expander("Add New Task"):
        task = st.text_input("Task")
        assigned = st.text_input("Assigned To")
        due = st.date_input("Due Date")
        status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
        if st.button("Save Task"):
            st.success("Task saved (mock action)")

# Files (placeholder)
else:
    st.title("📂 Files")
    st.info("File management coming soon. This will support uploads, filtering and linking to jobs.")
