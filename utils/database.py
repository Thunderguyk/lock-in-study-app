"""
Database utilities for Lock-In App
Handles data persistence and SQLite operations
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import streamlit as st

class StudyDatabase:
    """SQLite database for storing study data"""
    
    def __init__(self, db_path: str = "study_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Study sessions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            duration_minutes INTEGER,
            session_type TEXT,
            focus_score INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Documents table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_type TEXT,
            upload_date TIMESTAMP,
            file_size INTEGER,
            word_count INTEGER,
            analysis_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Study goals table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            daily_goal_minutes INTEGER,
            actual_minutes INTEGER,
            goal_achieved BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Settings table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE,
            setting_value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        conn.close()
    
    def add_study_session(self, session_data: Dict[str, Any]) -> int:
        """Add a new study session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO study_sessions 
        (start_time, end_time, duration_minutes, session_type, focus_score, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session_data.get('start_time'),
            session_data.get('end_time'),
            session_data.get('duration_minutes'),
            session_data.get('session_type'),
            session_data.get('focus_score'),
            session_data.get('notes', '')
        ))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return session_id
    
    def get_study_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get study statistics for the last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Total study time
        cursor.execute("""
        SELECT COALESCE(SUM(duration_minutes), 0) as total_minutes
        FROM study_sessions 
        WHERE start_time >= ?
        """, (start_date,))
        
        total_minutes = cursor.fetchone()[0]
        
        # Session count
        cursor.execute("""
        SELECT COUNT(*) as session_count
        FROM study_sessions 
        WHERE start_time >= ?
        """, (start_date,))
        
        session_count = cursor.fetchone()[0]
        
        # Average session length
        avg_session = total_minutes / session_count if session_count > 0 else 0
        
        # Today's study time
        today = datetime.now().date()
        cursor.execute("""
        SELECT COALESCE(SUM(duration_minutes), 0) as today_minutes
        FROM study_sessions 
        WHERE DATE(start_time) = ?
        """, (today,))
        
        today_minutes = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_minutes': total_minutes,
            'total_hours': round(total_minutes / 60, 1),
            'session_count': session_count,
            'avg_session_minutes': round(avg_session, 1),
            'today_minutes': today_minutes,
            'daily_average': round(total_minutes / days, 1)
        }
    
    def save_settings(self, settings: Dict[str, Any]):
        """Save app settings to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        settings_json = json.dumps(settings)
        
        cursor.execute("""
        INSERT OR REPLACE INTO app_settings (setting_key, setting_value)
        VALUES (?, ?)
        """, ('app_config', settings_json))
        
        conn.commit()
        conn.close()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load app settings from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT setting_value FROM app_settings 
        WHERE setting_key = ?
        """, ('app_config',))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return {}

# Initialize database if not exists
def get_database() -> StudyDatabase:
    """Get database instance"""
    if 'database' not in st.session_state:
        st.session_state.database = StudyDatabase()
    return st.session_state.database
