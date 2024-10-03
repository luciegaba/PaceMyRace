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


def add_run_session(date, session_type, pace_target, time_target, distance_target, session_description):
    conn, cursor = get_db_connection()
    cursor.execute('''
    INSERT INTO sessions (date, session_type, pace_target, time_target, distance_target, session_description)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, session_type, pace_target, time_target, distance_target, session_description))
    conn.commit()
    conn.close()

    
    
def get_database_rows():
    conn, cursor = get_db_connection()
    try:
        cursor.execute("SELECT id, date, session_type, pace_target, time_target, distance_target, session_description FROM sessions")
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.close()
        return []
    
    rows = cursor.fetchall()
    column_names = [col[0] for col in cursor.description]
    result = [dict(zip(column_names, row)) for row in rows]
    conn.close()

    return result



def remove_run_session(session_id):
    """
    Remove a run session from the database based on the session ID.

    Parameters:
    session_id (int): The ID of the session to be removed.
    """
    # Get a connection to the database
    conn, cursor  = get_db_connection()

    try:
        # Execute the DELETE statement to remove the session with the given ID
        conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        conn.commit()  # Commit the transaction to apply the changes
    except Exception as e:
        # In case of an error, log the exception or handle it as necessary
        print(f"Error removing session with ID {session_id}: {e}")
        conn.rollback()  # Rollback the transaction if an error occurs
    finally:
        # Close the connection after the operation
        conn.close()

def update_run_session(session_id, new_date, new_session_type, new_pace, new_time, new_distance, new_session_description):
    conn, cursor = get_db_connection()
    cursor.execute('''
        UPDATE sessions
        SET date = ?, session_type = ?, pace_target = ?, time_target = ?, distance_target = ?, session_description = ?
        WHERE id = ?
    ''', (new_date, new_session_type, new_pace, new_time, new_distance, new_session_description, session_id))
    conn.commit()
    conn.close()
    
def alter_table_add_description():
    conn, cursor = get_db_connection()
    # Check if the column already exists, if not, add it
    cursor.execute("PRAGMA table_info(sessions)")
    columns = [col[1] for col in cursor.fetchall()]
    if "session_description" not in columns:
        cursor.execute("ALTER TABLE sessions ADD COLUMN session_description TEXT")
        conn.commit()
    conn.close()

# Call this function at the start of your app to ensure the database is updated
alter_table_add_description()
