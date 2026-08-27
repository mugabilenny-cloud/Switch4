import streamlit as st

# Configure the page specifically for the admin interface
st.set_page_config(page_title="Admin | Switch Platform", page_icon="⚙️", layout="wide")

st.title("⚙️ Switch Platform: Admin Control Center")
st.markdown("Welcome to the administrative backend for the student portal.")

st.info("👈 Please select a management module from the sidebar to manage students and academic repositories.")

st.divider()

# System Overview Dashboard
st.markdown("### 📊 System Overview")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Course Nodes", "70", "Fully mapped")
col2.metric("Pending Uploads", "12", "-3 from yesterday")
col3.metric("Database Status", "Online", "Supabase active")
col4.metric("System Alerts", "0", "All clear")

st.divider()

st.markdown("### 🛠️ Quick Actions")
action1, action2 = st.columns(2)

with action1:
    st.button("Review Pending Student Uploads", use_container_width=True)
with action2:
    if st.button("Manage Student Journeys", use_container_width=True):
        st.switch_page("pages/5_Student_Journey.py")
