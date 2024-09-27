import streamlit as st
import sqlite3
from datetime import datetime, timedelta
from streamlit_calendar import calendar
# Streamlit UI$

st.set_page_config(page_title="Pace my Race", layout="wide")
st.title("Run Session Scheduler")
    # Tab structure
    # tab1, tab2 = st.tabs(["Schedule a Run", "View Sessions"])
    # with tab1:
    #     planner_tab(session_types)
    # with tab2:
        # calendar_tab(session_types)
        # calendar_tab()
session_types = {
    'Endurance fondamentale': '#4BFF4B',  
    'Fractionnée Court': '#FF6347',       
    'Fractionnée Long': '#FF4B4B',        
    'Sortie Longue': '#FF8C00',           
    'Autre': '#4682B4'}

if "events" not in st.session_state:
    st.session_state["events"] = []
