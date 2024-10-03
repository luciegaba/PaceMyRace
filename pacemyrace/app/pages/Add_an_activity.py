import streamlit as st
from datetime import datetime, timedelta
from utils import calculate_missing_field, parse_pace
from pacemyrace.app.data.create_db import add_run_session, get_db_connection, remove_run_session, update_run_session, get_database_rows
from pacemyrace.app.home import session_types

def planner_tab(session_types):
    st.header("Add a New Run Session")

    run_date = st.date_input("Select a date", value=datetime.today())

    session_type = st.selectbox("Select the type of session", list(session_types.keys()))

    if session_type == "Fractionnée Court" or session_type=="Fractionnée Long":
        session_description = st.text_area("Describe the session (fraction nee)")
    else:
        pace_target = st.text_input("Enter the target pace (e.g., 5:30 min/km)")
        time_target = st.text_input("Enter the target time (e.g., 45 minutes)")
        distance_target = st.text_input("Enter the target distance (e.g., 10 km)")

        pace_value = parse_pace(pace_target) if pace_target else None
        time_value = float(time_target.split()[0]) if time_target else None  # Time in minutes
        distance_value = float(distance_target.split()[0]) if distance_target else None  # Distance in kilometers

    if st.button("Add Run Session"):
        if session_type == "Fractionnée Court" or session_type=="Fractionnée Long":
            add_run_session(run_date, session_type, None, None, None, session_description)
            st.success(f"Run session added for {run_date}")
        else:
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

            if pace_value and time_value and distance_value:
                add_run_session(run_date, session_type, pace_target, f"{time_value} minutes", f"{distance_value} km", None)
                st.success(f"Run session added for {run_date}")

    st.header("Modify or Remove an Existing Run Session")

    existing_sessions = get_database_rows()

    if existing_sessions:
        session_options = [f"{s['date']} - {s['session_type']} - {s['pace_target']}" if "Fractionnée" not in s['session_type'] 
                           else f"{s['date']} - {s['session_type']} - {s['session_description']}" 
                           for s in existing_sessions]
        
        selected_session = st.selectbox("Select a session to modify or remove", session_options)
        selected_session_data = existing_sessions[session_options.index(selected_session)]
        selected_session_id = selected_session_data['id']

        st.subheader("Modify the Selected Session")

        new_run_date = st.date_input("Modify the date", value=datetime.strptime(selected_session_data['date'], '%Y-%m-%d'))
        new_session_type = st.selectbox("Modify the type of session", list(session_types.keys()), index=list(session_types.keys()).index(selected_session_data['session_type']))

        if new_session_type == "Fractionnée Court" or new_session_type=="Fractionnée Long":
            new_session_description = st.text_area("Modify the session description", value=selected_session_data['session_description'])
            if st.button("Modify Selected Session"):
                update_run_session(selected_session_id, new_run_date, new_session_type, None, None, None, new_session_description)
                st.success(f"Run session {selected_session} modified successfully.")
        else:
            new_pace_target = st.text_input("Modify the target pace (e.g., 5:30 min/km)", value=selected_session_data['pace_target'])
            new_time_target = st.text_input("Modify the target time (e.g., 45 minutes)", value=selected_session_data['time_target'])
            new_distance_target = st.text_input("Modify the target distance (e.g., 10 km)", value=selected_session_data['distance_target'])

            if st.button("Modify Selected Session"):
                update_run_session(selected_session_id, new_run_date, new_session_type, new_pace_target, new_time_target, new_distance_target, None)
                st.success(f"Run session {selected_session} modified successfully.")

        if st.button("Remove Selected Session"):
            remove_run_session(selected_session_id)
            st.success(f"Run session {selected_session} removed successfully.")
    else:
        st.info("No run sessions available to modify or remove.")


planner_tab(session_types)
