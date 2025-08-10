from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from database import insert_collection

def run_scraper():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get("https://in.bookmyshow.com/explore/movies-hyderabad")

    time.sleep(3)

    # Search for Mahavathar
    search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search for Movies, Events, Plays, Sports and Activities']")
    search_box.send_keys("Mahavathar")
    time.sleep(2)

    try:
        movie_link = driver.find_element(By.CSS_SELECTOR, "ul.search-list li a")
        movie_link.click()
    except:
        print("❌ Mahavathar not found")
        driver.quit()
        return

    time.sleep(5)

    # Click on a showtime
    try:
        showtime_button = driver.find_element(By.CSS_SELECTOR, "a.showtime-pill")
        showtime_button.click()
    except:
        print("❌ No showtime found")
        driver.quit()
        return

    time.sleep(5)

    # Extract seat types and prices from legend
    legend_items = driver.find_elements(By.CSS_SELECTOR, "div.legend-item")
    ticket_prices = {}
    for item in legend_items:
        try:
            label = item.find_element(By.CSS_SELECTOR, ".label").text.strip()
            price = item.find_element(By.CSS_SELECTOR, ".price").text.strip().replace("₹", "")
            ticket_prices[label] = int(price)
        except:
            continue

    # Extract seat status
    seat_elements = driver.find_elements(By.CSS_SELECTOR, "div.seat")
    seat_breakdown = {}
    filled_seats = {}

    for seat in seat_elements:
        category = seat.get_attribute("data-seat-type") or "Unknown"
        status = seat.get_attribute("class")

        seat_breakdown[category] = seat_breakdown.get(category, 0) + 1
        if "booked" in status:
            filled_seats[category] = filled_seats.get(category, 0) + 1

    estimated_collection = sum(
        filled_seats.get(cat, 0) * ticket_prices.get(cat, 0)
        for cat in filled_seats
        if cat in ticket_prices
    )

    data = {
        "city": "Hyderabad",
        "language": "Telugu",
        "movie_name": "Mahavathar",
        "theater": "PVR Inorbit",
        "showtime": "7:30 PM",
        "seat_breakdown": seat_breakdown,
        "filled_seats": filled_seats,
        "ticket_prices": ticket_prices,
        "estimated_collection": estimated_collection
    }

    insert_collection(data)
    print(f"✅ Inserted with dynamic pricing: ₹{estimated_collection}")

    driver.quit()
