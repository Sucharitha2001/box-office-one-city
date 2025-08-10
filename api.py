from flask import Flask, jsonify
import sqlite3
import json
import os
from database import init_db
from run_scrapper import run_scrape
import threading
import logging

app = Flask(__name__)
init_db()  # 👈 Ensure table is created before handling requests

@app.route('/')
def home():
    return "Welcome to Box Office Analytics API! Visit /collections to see data."

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
            "ticket_prices": json.loads(row[7]),
            "estimated_collection": row[8],
            "scraped_at": row[9]
        })

    return jsonify(data)

@app.route('/scrape', methods=['GET','POST'])
def scrape_data():
    threading.Thread(target=run_scraper).start()
    return jsonify({"status": "Scraping started in background"}), 202
    
def run_scraper():
    logging.info("Scraper started")
    try:
        run_scrape()
        logging.info("Data inserted")
        return jsonify({"status": "success", "message": "Scraping completed and data inserted."})
    except Exception as e:
        logging.error("Scraper error: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's assigned port
    app.run(host='0.0.0.0', port=port, debug=True)
