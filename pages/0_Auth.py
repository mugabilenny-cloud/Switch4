import streamlit as st
from supabase_client import sign_in_user, sign_up_user, fetch_user_profile
from ui_components import inject_base_css, wordmark

st.set_page_config(page_title="Sign In | Switch", layout="centered")
inject_base_css()
wordmark("2rem")

st.caption("Access academic course structures and learning materials.")
tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

with tab_login:
    email = st.text_input("Email", key="l_email")
    password = st.text_input("Password", type="password", key="l_pass")
    if st.button("Sign In", type="primary", use_container_width=True):
        res = sign_in_user(email, password)
        if res and "user" in res:
            uid = res["user"]["id"]
            st.query_params["session_user_id"] = uid
            st.session_state["authenticated_user_id"] = uid
            st.session_state["user_profile"] = fetch_user_profile(uid)
            st.success("Authenticated successfully!")
            st.switch_page("pages/1_Home.py")
        else:
            st.error("Invalid credentials provided.")

with tab_signup:
    su_email = st.text_input("Email", key="s_email")
    su_pass = st.text_input("Password", type="password", key="s_pass")
    su_name = st.text_input("Full Name")
    su_uni = st.text_input("University", value="Kampala International University")
    su_dept = st.text_input("Department", placeholder="e.g. Pharmacy")
    c1, c2 = st.columns(2)
    su_year = c1.number_input("Year", 1, 6, 1)
    su_sem = c2.number_input("Semester", 1, 3, 1)

    if st.button("Register Account", type="primary", use_container_width=True):
        user = sign_up_user(su_email, su_pass, su_name, su_uni, su_dept, int(su_year), int(su_sem))
        if user:
            st.query_params["session_user_id"] = user["id"]
            st.session_state["authenticated_user_id"] = user["id"]
            st.session_state["user_profile"] = fetch_user_profile(user["id"])
            st.success("Account created!")
            st.switch_page("pages/1_Home.py")
