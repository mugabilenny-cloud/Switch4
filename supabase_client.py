import os
import requests
import streamlit as st

SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
SUPABASE_ANON_KEY = st.secrets.get("SUPABASE_ANON_KEY", os.environ.get("SUPABASE_ANON_KEY", ""))
HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json",
}

def sign_up_user(email: str, password: str, full_name: str, university: str, department: str, year: int, semester: int):
    try:
        resp = requests.post(f"{SUPABASE_URL}/auth/v1/signup", headers=HEADERS, json={"email": email, "password": password})
        if resp.status_code == 200:
            user_data = resp.json().get("user")
            if user_data:
                profile_payload = {
                    "id": user_data["id"],
                    "email": email,
                    "full_name": full_name,
                    "university": university,
                    "department": department,
                    "current_year": year,
                    "current_semester": semester,
                }
                requests.post(f"{SUPABASE_URL}/rest/v1/profiles", headers={**HEADERS, "Prefer": "return=minimal"}, json=profile_payload)
            return user_data
    except Exception as e:
        st.error(f"Sign up failure: {e}")
    return None

def sign_in_user(email: str, password: str):
    try:
        resp = requests.post(f"{SUPABASE_URL}/auth/v1/token?grant_type=password", headers=HEADERS, json={"email": email, "password": password})
        return resp.json() if resp.status_code == 200 else None
    except Exception:
        return None

def fetch_user_profile(user_id: str):
    try:
        resp = requests.get(f"{SUPABASE_URL}/rest/v1/profiles?id=eq.{user_id}", headers=HEADERS)
        data = resp.json()
        return data[0] if isinstance(data, list) and len(data) > 0 else None
    except Exception:
        return None

def intelligent_search(query: str):
    try:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/rpc/fn_search_tree_intelligent", headers=HEADERS, json={"search_query": query, "result_limit": 20})
        return resp.json() if resp.status_code == 200 else []
    except Exception:
        return []

def fetch_chronological_unit_links(node_id: str):
    try:
        resp = requests.get(f"{SUPABASE_URL}/rest/v1/links?node_id=eq.{node_id}&order=sequence_number.asc,created_at.asc", headers=HEADERS)
        return resp.json() if resp.status_code == 200 else []
    except Exception:
        return []

def submit_student_upload(user_id: str, title: str, file_url: str, file_type: str):
    payload = {"user_id": user_id, "title": title, "file_url": file_url, "file_type": file_type, "status": "pending_review"}
    return requests.post(f"{SUPABASE_URL}/rest/v1/student_uploads", headers={**HEADERS, "Prefer": "return=representation"}, json=payload).json()
