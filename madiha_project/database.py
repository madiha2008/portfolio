"""
Madiha Portfolio - Database Module
SQLite operations with visitor tracking
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'portfolio.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Profile table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT,
            email TEXT,
            phone TEXT,
            about TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            emoji TEXT,
            color TEXT,
            proficiency INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            technologies TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Contact messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Visitor counter table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            count INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    insert_default_data(conn)
    conn.close()
    print("🎀 Madiha's Database initialized!")


def insert_default_data(conn):
    cursor = conn.cursor()
    
    # Default profile
    cursor.execute("SELECT COUNT(*) FROM profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO profile (name, title, email, phone, about)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            'J Madiha Firdous',
            'BCA Student | Aspiring Web Developer',
            'madiha13052008@gmail.com',
            '9177702367',
            'I am a passionate BCA student with a deep interest in programming and web development. I love exploring new technologies and building creative solutions. My journey in tech started with curiosity, and now I am on a mission to become a skilled web developer. I believe in continuous learning and pushing boundaries.'
        ))
    
    # Default skills
    cursor.execute("SELECT COUNT(*) FROM skills")
    if cursor.fetchone()[0] == 0:
        skills = [
            ('HTML5', '🌐', '#e34c26', 85),
            ('CSS3', '🎨', '#264de4', 80),
            ('Java', '☕', '#f89820', 75),
            ('Python', '🐍', '#3776ab', 70)
        ]
        cursor.executemany('''
            INSERT INTO skills (name, emoji, color, proficiency)
            VALUES (?, ?, ?, ?)
        ''', skills)
    
    # Default projects
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        projects = [
            ('Portfolio Website 🎨', 'A fun cartoon-themed portfolio with playful animations!', 
             'HTML,CSS,JavaScript,Python', 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400'),
            ('Calculator App 🔢', 'A colorful calculator with basic and scientific operations.',
             'HTML,CSS,JavaScript', 'https://images.unsplash.com/photo-1587145820266-a5951ee6f620?w=400'),
            ('To-Do List 📝', 'A cute task manager to organize daily activities!',
             'HTML,CSS,JavaScript', 'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=400')
        ]
        cursor.executemany('''
            INSERT INTO projects (title, description, technologies, image_url)
            VALUES (?, ?, ?, ?)
        ''', projects)
    
    # Initialize visitor counter
    cursor.execute("SELECT COUNT(*) FROM visitors")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO visitors (count) VALUES (0)")
    
    conn.commit()


# Profile Operations
def get_profile():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile LIMIT 1")
    profile = cursor.fetchone()
    conn.close()
    return dict(profile) if profile else None


# Skills Operations
def get_all_skills():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM skills ORDER BY proficiency DESC")
    skills = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return skills


def add_skill(name, emoji, color, proficiency):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO skills (name, emoji, color, proficiency)
        VALUES (?, ?, ?, ?)
    ''', (name, emoji, color, proficiency))
    conn.commit()
    skill_id = cursor.lastrowid
    conn.close()
    return skill_id


# Projects Operations
def get_all_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    projects = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return projects


def add_project(title, description, technologies, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO projects (title, description, technologies, image_url)
        VALUES (?, ?, ?, ?)
    ''', (title, description, technologies, image_url))
    conn.commit()
    project_id = cursor.lastrowid
    conn.close()
    return project_id


# Contact Messages Operations
def save_contact_message(name, email, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contact_messages (name, email, message)
        VALUES (?, ?, ?)
    ''', (name, email, message))
    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    return message_id


def get_all_messages():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contact_messages ORDER BY created_at DESC")
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return messages


def mark_message_read(message_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contact_messages SET is_read = 1 WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()


def delete_message(message_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contact_messages WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()


# Visitor Counter Operations
def get_visitor_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM visitors LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result['count'] if result else 0


def increment_visitor_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE visitors SET count = count + 1, last_updated = ?", (datetime.now(),))
    conn.commit()
    cursor.execute("SELECT count FROM visitors LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result['count'] if result else 0


if __name__ == '__main__':
    init_database()
    print("✅ Database setup complete!")
