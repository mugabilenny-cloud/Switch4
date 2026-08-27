import streamlit as st
import requests
import os

st.set_page_config(page_title="Student Journey | Admin Dashboard", layout="wide")

SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
SUPABASE_KEY = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", os.environ.get("SUPABASE_ANON_KEY", ""))
HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"}

st.title("🎓 Student Academic Journey Management")

students_resp = requests.get(f"{SUPABASE_URL}/rest/v1/profiles?select=*", headers=HEADERS)
students = students_resp.json() if students_resp.status_code == 200 else []

for s in students:
    with st.expander(f"{s.get('full_name')} ({s.get('email')}) — {s.get('department')}"):
        col1, col2, col3 = st.columns(3)
        y = col1.number_input("Year", 1, 6, int(s.get("current_year", 1)), key=f"y_{s['id']}")
        sem = col2.number_input("Semester", 1, 3, int(s.get("current_semester", 1)), key=f"s_{s['id']}")
        
        if col3.button("Save Journey State", key=f"btn_{s['id']}"):
            update_payload = {"current_year": int(y), "current_semester": int(sem)}
            resp = requests.patch(f"{SUPABASE_URL}/rest/v1/profiles?id=eq.{s['id']}", headers=HEADERS, json=update_payload)
            if resp.status_code in [200, 204]:
                st.success("Student progress updated!")
                st.rerun()
            else:
                st.error("Failed to update profile.")
