import streamlit as st
from datetime import datetime, timedelta
from utils import calculate_missing_field,parse_pace
from pacemyrace.database.create_db import add_run_session,get_db_connection
from pacemyrace.app.home import session_types

    
def planner_tab(session_types):
    st.header("Add a New Run Session")

    # Calendar to select a date
    run_date = st.date_input("Select a date", value=datetime.today())


    session_type = st.selectbox("Select the type of session", list(session_types.keys()))

    # Input fields for pace, time, and distance
    pace_target = st.text_input("Enter the target pace (e.g., 5:30 min/km)")
    time_target = st.text_input("Enter the target time (e.g., 45 minutes)")
    distance_target = st.text_input("Enter the target distance (e.g., 10 km)")

    pace_value = parse_pace(pace_target) if pace_target else None
    time_value = float(time_target.split()[0]) if time_target else None  # Time in minutes
    distance_value = float(distance_target.split()[0]) if distance_target else None  # Distance in kilometers

    # Automatically calculate missing field
    if st.button("Add Run Session"):
        if not pace_value or not time_value or not distance_value:
            missing_field = calculate_missing_field(pace_value, time_value, distance_value)

            if missing_field is not None:
                if not distance_value:
                    distance_value = round(missing_field, 2)
                    st.info(f"Calculated distance: {distance_value} km")
                elif not time_value:
                    time_value = round(missing_field, 2)
                    st.info(f"Calculated time: {time_value} minutes")
                elif not pace_value:
                    pace_value = round(missing_field, 2)
                    pace_target = f"{int(pace_value)}:{int((pace_value - int(pace_value)) * 60):02d} min/km"
                    st.info(f"Calculated pace: {pace_target}")
            else:
                st.error("Not enough data to calculate the missing field.")
        else:
            st.info("All fields provided; no calculation needed.")

        # If all values are available, add the session
        if pace_value and time_value and distance_value:
            add_run_session(run_date, session_type, pace_target, f"{time_value} minutes", f"{distance_value} km")
            st.success(f"Run session added for {run_date}")

        st.session_state["events"] = []
planner_tab(session_types=session_types)