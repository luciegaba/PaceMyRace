import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
from pacemyrace.app.data.create_db import add_run_session,get_db_connection
from pacemyrace.app.data.googlecalendar import authentificate_googlecalendar,synchronise_planning
from pacemyrace.app.home import session_types

def calendar_tab(session_types):
    
    st.header("Planning")


    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM sessions")
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=["id", "date", "session_type", "pace_target", "time_target", "distance_target","session_description"])
    df['color'] = df['session_type'].map(session_types)
    st.dataframe(df)    

    events = []
    for index, row in df.iterrows():
        event = {
            "title": row['session_type'],
            "color": row['color'],
            "start": pd.to_datetime(row['date']).strftime('%Y-%m-%d'),  # Ensure correct date format
            "end": pd.to_datetime(row['date']).strftime('%Y-%m-%d'),     # End date is the same as start date
            "resourceId": str(index)  # Using the index as the resourceId, converting to string
        }
        events.append(event)

    st.session_state["events"] = events
    calendar_options = {
        "editable": "true",
        "navLinks": "true",
        "selectable": "true",
    }    
    if st.session_state["events"]:
        state = calendar(
            events=st.session_state["events"],
            options=calendar_options,
        custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 700;
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
        """,
            key="daygrid",
        )


    if "eventClick" in state:
        st.write(state["eventClick"]["event"]["title"], state["eventClick"]["event"]["start"])
        session_type_clicked = state["eventClick"]["event"]["title"]  # session_type
        date_clicked = state["eventClick"]["event"]["start"]          # date
        date_clicked = pd.to_datetime(date_clicked).strftime('%Y-%m-%d')
        filtered_df = df[(df['session_type'] == session_type_clicked) & (df['date'] == date_clicked)]
        st.dataframe(filtered_df)
        
      
    if st.button("Synchronise with Google"):  
        service = authentificate_googlecalendar()
        if service is not None:
            st.success("Successfully identified")
                
            synchronise_planning(service,df.to_dict(orient="records"))
        
calendar_tab(session_types)