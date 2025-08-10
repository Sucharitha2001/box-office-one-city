from flask import Flask, jsonify
import sqlite3
import json
from database import init_db
from scraper import run_scraper
import threading

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    return "🎬 Welcome to Mahavathar Box Office API"

@app.route('/collections')
def get_collections():
    conn = sqlite3.connect("collections.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movie_collections ORDER BY scraped_at DESC")
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "city": row[1],
            "language": row[2],
            "movie_name": row[3],
            "theater": row[4],
            "showtime": row[5],
            "seat_breakdown": json.loads(row[6]),
            "filled_seats": json.loads(row[7]),
            "ticket_prices": json.loads(row[8]),
            "estimated_collection": row[9],
            "scraped_at": row[10]
        })

    return jsonify(data)

@app.route('/scrape', methods=['GET'])
def scrape():
    threading.Thread(target=run_scraper).start()
    return jsonify({"status": "Scraping started"}), 202

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's assigned port
    app.run(host='0.0.0.0', port=port, debug=True)
