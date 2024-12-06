import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import time
def submitted():
    st.session_state.submitted = True
def reset():
    st.session_state.submitted = False
if 'selected_times' not in st.session_state:
    st.session_state.selected_times = []
if 'selected_ids' not in st.session_state:
    st.session_state.selected_ids = []
# st.write(st.button("Sắp xếp và Lưu Lịch trình")) 
if st.button("Sắp xếp và Lưu Lịch trình"):
# Create a table with time and ID selection for each location
    with st.form("schedule_form"):
        st.write("### Lịch trình cho các địa điểm")
        # Clear previous values to avoid duplicates on reruns
        st.session_state.selected_times.clear()
        st.session_state.selected_ids.clear()
        for i in range(2):
            col1, col2 = st.columns([2, 2])

            # Time input selection for each location
            selected_time = col1.time_input(
                f"Chọn thời gian cho địa điểm {i+1}",
                value=datetime.strptime("0:0",'%H:%M').time(),
                key=f"time_{i}"
            )

            # ID selection for each location
            selected_id = col2.selectbox(
                f"Chọn ID cho địa điểm {i+1}",
                key=f"id_{i}"
            )
            st.session_state.selected_times.append(selected_time)
            st.session_state.selected_ids.append(selected_id)
        # Submit button
        # st.write(st.form_submit_button("chao trong minh"))
        submit= st.form_submit_button("lưu lịch trình", on_click= submitted) 
    if 'submitted' in st.session_state:
        if st.session_state.submitted==True:
            if 'schedule' not in st.session_state.scenarios[selected_scenario]:
                st.session_state.scenarios[selected_scenario]['schedule'] = []
            for get_time,id in zip(st.session_state.selected_times, st.session_state.selected_ids):
                st.session_state.scenarios[selected_scenario]['schedule'].append({
                    'time':get_time.strftime("%-H:%-M"),
                    'id':id
                })
            st.session_state.scenarios[selected_scenario]['schedule'].sort(key=lambda x: x['time'])
            st.success("Lịch trình đã được lưu và sắp xếp theo thứ tự tăng dần thời gian!")
    reset()