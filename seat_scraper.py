# seat_scraper.py

from selenium.webdriver.common.by import By
import time

def get_seat_data(city, movie_name, driver):
    seat_data_list = []

    try:
        movie = driver.find_element(By.XPATH, f"//h4[contains(text(), '{movie_name}')]")
        movie.click()
        time.sleep(5)

        showtimes = driver.find_elements(By.CLASS_NAME, "showtime-pill")
        for show in showtimes:
            try:
                showtime = show.text
                show.click()
                time.sleep(5)

                seats = driver.find_elements(By.CLASS_NAME, "seat")
                filled_seats = {}
                ticket_price = {}

                for seat in seats:
                    seat_type = seat.get_attribute("data-seat-type")
                    price = int(seat.get_attribute("data-price"))
                    status = seat.get_attribute("class")

                    if seat_type not in filled_seats:
                        filled_seats[seat_type] = 0
                        ticket_price[seat_type] = price

                    if "booked" in status:
                        filled_seats[seat_type] += 1

                estimated_collection = sum(
                    ticket_price[stype] * filled_seats[stype]
                    for stype in filled_seats
                )

                seat_data_list.append({
                    "theater": "Unknown Theater",  # You can improve this later
                    "showtime": showtime,
                    "seat_breakdown": filled_seats,
                    "ticket_prices": ticket_price,
                    "estimated_collection": estimated_collection
                })

                driver.back()
                time.sleep(3)
            except Exception as e:
                print(f"⚠️ Error scraping showtime: {e}")
                continue

        driver.back()
        time.sleep(3)
    except Exception as e:
        print(f"⚠️ Error with movie {movie_name}: {e}")

    return seat_data_list
