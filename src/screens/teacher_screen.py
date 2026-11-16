import time
from datetime import datetime
from html import escape

import numpy as np
import pandas as pd
import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher, get_subject_students
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
from src.database.config import supabase
from src.components.dialog_voice_attendance import voice_attendance_dialog


def teacher_screen():
    logged_in = "teacher_data" in st.session_state
    # Wide layout for the dashboard, narrow centred column for login/register.
    style_background_dashboard("1080px" if logged_in else "520px")
    style_base_layout()

    if logged_in:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    # Sidebar: brand, navigation, account. Navigation keys start with
    # "teacher_nav_" so base_layout.py can style them as a quiet list.
    with st.sidebar:
        header_dashboard()
        st.caption("Teacher workspace")
        st.space()

        nav_items = [
            ("take_attendance", "Take attendance", ":material/face:"),
            ("manage_subjects", "Manage subjects", ":material/menu_book:"),
            ("attendance_records", "Attendance records", ":material/assignment:"),
        ]
        for tab_key, label, icon in nav_items:
            button_type = (
                "primary"
                if st.session_state.current_teacher_tab == tab_key
                else "secondary"
            )
            if st.button(
                label,
                key=f"teacher_nav_{tab_key}",
                icon=icon,
                type=button_type,
                width="stretch",
            ):
                st.session_state.current_teacher_tab = tab_key
                st.rerun()

        st.divider()
        st.markdown(
            f'<div class="at-label">Signed in as</div>'
            f'<div class="at-user">{escape(str(teacher_data["name"]))}</div>',
            unsafe_allow_html=True,
        )
        if st.button(
            "Logout",
            key="teacher_sidebar_logout",
            type="secondary",
            icon=":material/logout:",
            width="stretch",
        ):
            st.session_state["is_logged_in"] = False
            del st.session_state.teacher_data
            st.rerun()

    st.title(f"Welcome, {teacher_data['name']}")
    st.caption("Manage your subjects and take attendance from one place.")
    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    st.header('Take attendance')
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []
    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.info("You haven't created any subjects yet. Create one in Manage subjects to begin.")
        return
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}
    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')
    with col1:
        selected_subject_label = st.selectbox('Subject', options=list(subject_options.keys()))
    with col2:
        if st.button('Add photos', type='secondary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]
    st.divider()

    if st.session_state.attendance_images:
        st.subheader('Added photos')
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Run face analysis', width='stretch', type='primary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}
                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")
                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()

                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')

                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(sources) > 0
                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })
                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })
                    # Fix: only open the dialog when there are results to show.
                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c2:
        if st.button('Use voice attendance', type='secondary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)

    with c3:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()


@st.dialog("Enrolled Students", width="large")
def show_subject_students(subject_id, subject_name):
    st.caption(f"Students enrolled in {subject_name}")

    students = get_subject_students(subject_id)

    if not students:
        st.info("No students enrolled in this subject yet.")
        return

    st.metric("Total enrolled students", len(students))

    search = st.text_input(
        "Search students",
        placeholder="Enter student name..."
    )

    filtered = [
        s for s in students
        if search.lower() in s["name"].lower()
    ]

    if filtered:
        df = pd.DataFrame([
            {
                "Student ID": s["student_id"],
                "Name": s["name"]
            }
            for s in filtered
        ])

        st.dataframe(df, width="stretch", hide_index=True)
    else:
        st.warning("No matching students found.")



def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns([3, 1], vertical_alignment='center')

    with col1:
        st.header('Manage subjects')

    with col2:
        if st.button(
            'Create subject',
            type='primary',
            icon=':material/add:',
            width='stretch'
        ):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        cols = st.columns(2)

        for i, sub in enumerate(subjects):
            stats = [
                ("Students", sub['total_students']),
                ("Classes", sub['total_classes']),
            ]

            with cols[i % 2]:
                def subject_actions(sub=sub):
                    c1, c2 = st.columns(2)

                    with c1:
                        if st.button(
                            "View Students",
                            key=f"view_students_{sub['subject_id']}",
                            type='secondary',
                            icon=":material/groups:",
                            width='stretch'
                        ):
                            show_subject_students(
                                sub['subject_id'],
                                sub['name']
                            )

                    with c2:
                        if st.button(
                            "Share code",
                            key=f"share_{sub['subject_code']}",
                            type='secondary',
                            icon=":material/share:",
                            width='stretch'
                        ):
                            share_subject_dialog(
                                sub['name'],
                                sub['subject_code']
                            )

                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=stats,
                    footer_callback=subject_actions
                )

    else:
        st.info(
            "No subjects yet. Select Create subject to add your first one."
        )


def teacher_tab_attendance_records():
    st.header('Attendance records')
    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)
    if not records:
        st.info("No attendance has been recorded yet.")
        return
    data = []
    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)
    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance'] = (
        summary['Present_Count'].astype(str) + " / "
        + summary['Total_Count'].astype(str) + " present"
    )

    display_df = (summary.sort_values(by='ts_group', ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance']]
                  )
    st.dataframe(display_df, width='stretch', hide_index=True)


def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


def _auth_top_bar():
    """Brand on the left, 'Back to home' on the right (login and register pages)."""
    c1, c2 = st.columns([3, 2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Back to home", type='secondary', key='loginbackbtn',
                     icon=':material/arrow_back:', width='stretch'):
            st.session_state['login_type'] = None
            st.rerun()
    st.divider()


def teacher_screen_login():
    _auth_top_bar()
    st.header('Teacher login', text_alignment='center')
    st.space()
    teacher_username = st.text_input("Username", placeholder='ananyaroy')
    teacher_pass = st.text_input("Password", type='password', placeholder="Enter password")
    st.space()
    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Login', type='primary', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome back!", icon="👋")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password combo")

    with btnc2:
        if st.button('Register instead', type='secondary', width='stretch'):
            st.session_state.teacher_login_type = 'register'
            st.rerun()  # Fix: switch screens immediately instead of on the next click.
    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"

    if check_teacher_exists(teacher_username):
        return False, "Username already taken"

    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully created! Log in now."

    except Exception:
        return False, "Unexpected Error!"


def teacher_screen_register():
    _auth_top_bar()
    st.header('Create teacher account', text_alignment='center')
    st.space()
    teacher_username = st.text_input("Username", placeholder='ananyaroy')
    teacher_name = st.text_input("Full name", placeholder='Ananya Roy')
    teacher_pass = st.text_input("Password", type='password', placeholder="Enter password")
    teacher_pass_confirm = st.text_input("Confirm password", type='password', placeholder="Re-enter password")
    st.space()
    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Register', type='primary', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()

            else:
                st.error(message)

    with btnc2:
        if st.button('Login instead', type='secondary', width='stretch'):
            st.session_state.teacher_login_type = 'login'
            st.rerun()  # Fix: switch screens immediately instead of on the next click.
    footer_dashboard()
