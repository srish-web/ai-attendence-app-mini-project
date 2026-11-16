import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():
    style_background_home()
    style_base_layout()

    header_home()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=96)
            st.subheader("I'm a student")
            st.caption("Log in with FaceID to see your subjects and attendance.")
            if st.button('Student portal', type='primary', key='home_student_btn',
                         icon=':material/arrow_outward:', icon_position='right', width='stretch'):
                st.session_state['login_type'] = 'student'
                st.rerun()

    with col2:
        with st.container(border=True):
            st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=96)
            st.subheader("I'm a teacher")
            st.caption("Create subjects, take attendance and review records.")
            if st.button('Teacher portal', type='primary', key='home_teacher_btn',
                         icon=':material/arrow_outward:', icon_position='right', width='stretch'):
                st.session_state['login_type'] = 'teacher'
                st.rerun()

    footer_home()
