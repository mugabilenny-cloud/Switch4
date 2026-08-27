import streamlit as st

def inject_base_css():
    st.markdown("""
        <style>
        .horizontal-scroll-container {
            display: flex;
            overflow-x: auto;
            gap: 1rem;
            padding: 0.5rem 0 1rem 0;
            scroll-snap-type: x mandatory;
            -webkit-overflow-scrolling: touch;
        }
        .horizontal-tile {
            flex: 0 0 80%;
            scroll-snap-align: start;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 1.2rem;
            background: #FFFFFF;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        </style>
    """, unsafe_allow_html=True)

def wordmark(size="1.5rem"):
    st.markdown(f"<h2 style='color:#E85D2C; margin:0; font-size:{size}; font-weight:800;'>SWITCH</h2>", unsafe_allow_html=True)

def bottom_nav(active="Home"):
    st.markdown("---")
    cols = st.columns(4)
    pages = [("Home", "pages/1_Home.py"), ("Courses", "pages/3_Course_Detail.py"), ("Upload", "pages/4_Upload.py"), ("Auth", "pages/0_Auth.py")]
    for idx, (name, path) in enumerate(pages):
        label = f"**{name}**" if name == active else name
        if cols[idx].button(label, key=f"nav_{name}"):
            st.switch_page(path)
