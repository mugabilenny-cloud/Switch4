import streamlit as st
from supabase_client import fetch_user_profile

st.set_page_config(page_title="Switch", page_icon="🟠", layout="centered", initial_sidebar_state="collapsed")

stored_uid = st.query_params.get("session_user_id") or st.session_state.get("authenticated_user_id")

if stored_uid:
    profile = fetch_user_profile(stored_uid)
    if profile:
        st.session_state["user_profile"] = profile
        st.session_state["authenticated_user_id"] = stored_uid
        st.switch_page("pages/1_Home.py")

st.switch_page("pages/0_Auth.py")
