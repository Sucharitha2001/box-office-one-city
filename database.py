import sqlite3

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
            ticket_prices TEXT,
            estimated_collection INTEGER,
            scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_collection(city, language, movie_name, theater, showtime, seat_breakdown, ticket_prices, estimated_collection):
    conn = sqlite3.connect("collections.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movie_collections (city, language, movie_name, theater, showtime, seat_breakdown, ticket_prices, estimated_collection)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        city, language, movie_name, theater, showtime,
        json.dumps(seat_breakdown),
        json.dumps(ticket_prices),
        estimated_collection
    ))
    conn.commit()
    conn.close()
