import sqlite3
import streamlit as st
from datetime import date

def init_db():
    conn, cursor = get_db_connection()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        session_type TEXT,
        pace_target TEXT,
        time_target TEXT,
        distance_target TEXT
    )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('run_sessions.db', check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


init_db()


def get_session_types():
    return  


def add_run_session(date, session_type, pace_target, time_target, distance_target):
    conn, cursor = get_db_connection()
    cursor.execute('''
    INSERT INTO sessions (date, session_type, pace_target, time_target, distance_target)
    VALUES (?, ?, ?, ?, ?)
    ''', (date, session_type, pace_target, time_target, distance_target))
    conn.commit()
    conn.close()
    
    