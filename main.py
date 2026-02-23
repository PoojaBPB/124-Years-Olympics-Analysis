import streamlit as st
import summerolympics
import winterolympics

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# ---------------- HOME PAGE ----------------
if st.session_state.page == 'home':
    st.title('124 Years of Olympics Analysis (1896 - 2020)')
    st.image('https://thesuffolkjournal.com/wp-content/uploads/2020/03/olympic-rings.jpg')
    if st.button('Summer Olympics'):
        st.session_state.page = 'summer'
    if st.button('Winter Olympics'):
        st.session_state.page = 'winter'

# ---------------- SUMMER PAGE ----------------
elif st.session_state.page == 'summer':
    if st.sidebar.button('← Back'):
        st.session_state.page = 'home'
    summerolympics.run()

# ---------------- WINTER PAGE ----------------
elif st.session_state.page == 'winter':
    if st.sidebar.button('← Back'):
        st.session_state.page = 'home'
    winterolympics.run()