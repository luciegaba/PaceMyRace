import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
from pacemyrace.database.create_db import add_run_session,get_db_connection
from pacemyrace.app.home import session_types
# # st.set_page_config(page_title="Demo for streamlit-calendar", page_icon="📆")




def calendar_tab(session_types):
    
    st.header("Planning")


    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM sessions")
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=["id", "date", "session_type", "pace_target", "time_target", "distance_target"])
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

    st.write(state)
        
calendar_tab(session_types)