import streamlit as st
from supabase_client import fetch_chronological_unit_links
from ui_components import inject_base_css, bottom_nav

st.set_page_config(page_title="Course Detail | Switch", layout="centered")
inject_base_css()

active_node = st.session_state.get("active_course", {"id": "00000000-0000-0000-0000-000000000000", "name": "Course Material"})
st.markdown(f"### {active_node['name']}")

links = fetch_chronological_unit_links(active_node["id"])

# Chronological link organization with strictly 1 Notes link & 1 Questions link allowed
notes_link = next((l for l in links if l["link_kind"] == "drive_notes"), None)
questions_link = next((l for l in links if l["link_kind"] == "drive_questions"), None)
youtube_links = [l for l in links if l["link_kind"] == "youtube"]

st.markdown("#### Lecture Resources")

if notes_link:
    st.markdown(f"📝 **Drive Notes:** [{notes_link.get('title') or 'Open Lecture Notes'}]({notes_link['url']})")

if questions_link:
    st.markdown(f"❓ **Drive Questions:** [{questions_link.get('title') or 'Open Revision Questions'}]({questions_link['url']})")

if youtube_links:
    st.markdown("**🎥 Video Tutorials:**")
    for yt in youtube_links:
        st.markdown(f"- [{yt.get('title') or 'Watch Tutorial'}]({yt['url']})")

bottom_nav(active="Courses")
