import streamlit as st
from supabase_client import intelligent_search
from ui_components import inject_base_css, bottom_nav, wordmark

st.set_page_config(page_title="Home | Switch", layout="centered")
inject_base_css()
wordmark()

profile = st.session_state.get("user_profile", {})
if profile:
    st.write(f"**{profile.get('full_name')}** · Year {profile.get('current_year')}, Semester {profile.get('current_semester')}")

# Dynamic Intelligent Search Bar
query = st.text_input("Search notes, course codes, or documents...", placeholder="Type to search tree...", label_visibility="collapsed")
if query:
    results = intelligent_search(query)
    if results:
        for r in results:
            st.write(f"🔍 **{r['title']}** (`{r['result_type']}`) — *{r['node_path']}*")
    else:
        st.info("No matching records found across course structures.")

st.divider()

# Files Last Accessed (Placed at the top active courses section)
st.markdown("#### Files Last Accessed")
recent_files = st.session_state.get("recently_accessed_files", [])
if not recent_files:
    st.caption("No recently viewed documents.")
else:
    for f in recent_files:
        col1, col2 = st.columns([4, 1])
        col1.write(f"📄 **{f['title']}**")
        if col2.button("Open", key=f"recent_{f['id']}"):
            st.session_state["active_resource_id"] = f["id"]
            st.switch_page("pages/3_Course_Detail.py")

st.divider()

# What's New on Campus (Horizontal Sliding Cards Layout)
st.markdown("#### What's New on Campus")
mock_updates = [
    {"code": "PHARM 3101", "title": "Updated Quality Control Past Papers added to Unit 3.", "url": "#"},
    {"code": "CAMPUS", "title": "Semester 2 Examinations Timetable has been officially uploaded.", "url": "#"},
    {"code": "MED 2204", "title": "New Pathology Slide Annotations uploaded to Drive Notes.", "url": "#"}
]

cards_html = '<div class="horizontal-scroll-container">'
for item in mock_updates:
    cards_html += f"""
    <div class="horizontal-tile">
        <span style="color:#E85D2C; font-weight:700; font-size:0.75rem;">{item['code']}</span>
        <div style="font-weight:600; font-size:1.05rem; margin:0.4rem 0;">{item['title']}</div>
        <a href="{item['url']}" style="color:#E85D2C; font-size:0.85rem; text-decoration:none; font-weight:600;">View update →</a>
    </div>
    """
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

bottom_nav(active="Home")
