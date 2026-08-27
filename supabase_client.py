import os
import requests
import streamlit as st

# Explicit configuration retrieval with strict validation
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL", "")
SUPABASE_ANON_KEY = st.secrets.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_ANON_KEY", "")

if not SUPABASE_URL or not SUPABASE_URL.startswith("https://"):
    st.error("Configuration Error: SUPABASE_URL is missing or incorrectly formatted in your Streamlit Secrets.")

HEADERS = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json",
}

def sign_up_user(email: str, password: str, full_name: str, university: str, department: str, year: int, semester: int):
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/auth/v1/signup"
        resp = requests.post(url, headers=HEADERS, json={"email": email, "password": password})
        
        if resp.status_code == 200:
            res_data = resp.json()
            user_data = res_data.get("user") or res_data
            user_id = user_data.get("id")
            
            if user_id:
                profile_payload = {
                    "id": user_id,
                    "email": email,
                    "full_name": full_name,
                    "university": university,
                    "department": department,
                    "current_year": year,
                    "current_semester": semester,
                }
                profile_url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/profiles"
                requests.post(profile_url, headers={**HEADERS, "Prefer": "return=minimal"}, json=profile_payload)
            return user_data
        else:
            st.error(f"Sign up failure: {resp.text}")
    except Exception as e:
        st.error(f"Connection failure: {e}")
    return None

def sign_in_user(email: str, password: str):
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/auth/v1/token?grant_type=password"
        resp = requests.post(url, headers=HEADERS, json={"email": email, "password": password})
        if resp.status_code == 200:
            return resp.json()
        else:
            st.error(f"Sign in failure: {resp.text}")
    except Exception as e:
        st.error(f"Connection failure: {e}")
    return None

def fetch_user_profile(user_id: str):
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/profiles?id=eq.{user_id}"
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            data = resp.json()
            return data[0] if isinstance(data, list) and len(data) > 0 else None
    except Exception:
        pass
    return None

def intelligent_search(query: str):
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/rpc/fn_search_tree_intelligent"
        resp = requests.post(url, headers=HEADERS, json={"search_query": query, "result_limit": 20})
        return resp.json() if resp.status_code == 200 else []
    except Exception:
        return []

def fetch_chronological_unit_links(node_id: str):
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/links?node_id=eq.{node_id}&order=sequence_number.asc,created_at.asc"
        resp = requests.get(url, headers=HEADERS)
        return resp.json() if resp.status_code == 200 else []
    except Exception:
        return []

def submit_student_upload(user_id: str, title: str, file_url: str, file_type: str):
    try:
        payload = {"user_id": user_id, "title": title, "file_url": file_url, "file_type": file_type, "status": "pending_review"}
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/student_uploads"
        resp = requests.post(url, headers={**HEADERS, "Prefer": "return=representation"}, json=payload)
        return resp.json() if resp.status_code in [200, 201] else None
    except Exception:
        return None
