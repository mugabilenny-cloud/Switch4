import streamlit as st
from supabase_client import submit_student_upload
from ui_components import inject_base_css, bottom_nav

st.set_page_config(page_title="Upload | Switch", layout="centered")
inject_base_css()

st.markdown("### ⬆️ Upload Student Material")
user_id = st.session_state.get("authenticated_user_id")

with st.form("upload_form"):
    title = st.text_input("Resource Title")
    file_url = st.text_input("Drive or Document URL")
    file_type = st.selectbox("Resource Kind", ["pdf", "doc", "slides", "notes"])
    submit = st.form_submit_button("Submit Material")

if submit:
    if not user_id:
        st.error("Please log in to submit resources.")
    elif not title or not file_url:
        st.error("Title and URL are required.")
    else:
        submit_student_upload(user_id, title, file_url, file_type)
        st.success("Resource submitted for admin verification!")

bottom_nav(active="Upload")
