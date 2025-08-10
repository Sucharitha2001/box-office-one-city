import sqlite3
import json
from datetime import datetime

def init_db():
    conn = sqlite3.connect("collections.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie_collections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            language TEXT,
            movie_name TEXT,
            theater TEXT,
            showtime TEXT,
            seat_breakdown TEXT,
            filled_seats TEXT,
            ticket_prices TEXT,
            estimated_collection REAL,
            scraped_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_collection(data):
    conn = sqlite3.connect("collections.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movie_collections (
            city, language, movie_name, theater, showtime,
            seat_breakdown, filled_seats, ticket_prices,
            estimated_collection, scraped_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["city"],
        data["language"],
        data["movie_name"],
        data["theater"],
        data["showtime"],
        json.dumps(data["seat_breakdown"]),
        json.dumps(data["filled_seats"]),
        json.dumps(data["ticket_prices"]),
        data["estimated_collection"],
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
