from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import insert_collection

def run_scraper():
    # Setup Chrome options
    options = Options()
    options.add_argument("--headless")  # Set to False for debugging
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        print("🌐 Opening BookMyShow Hyderabad...")
        driver.get("https://in.bookmyshow.com/explore/movies-hyderabad")

        # Wait for search box
        print("🔍 Waiting for search box...")
        search_box = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder*='Search']")
        ))
        search_box.send_keys("Mahavathar")

        # Wait for search results
        print("🔎 Looking for Mahavathar in search results...")
        movie_link = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "ul.search-list li a")
        ))
        movie_link.click()

        # Wait for showtime button
        print("🎬 Waiting for showtime button...")
        showtime_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.showtime-pill")
        ))
        showtime_button.click()

        # Wait for seat map to load
        print("🪑 Extracting seat and pricing info...")
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.legend-item")
        ))

        # Extract ticket prices
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

        # Estimate collection
        estimated_collection = sum(
            filled_seats.get(cat, 0) * ticket_prices.get(cat, 0)
            for cat in filled_seats
            if cat in ticket_prices
        )

        # Prepare data
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

    except Exception as e:
        print(f"❌ Scraper failed: {e}")

    finally:
        driver.quit()
