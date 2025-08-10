from seat_scraper import get_seat_data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def run_scrape():
    from city_scraper import get_all_cities
    from movie_scraper import get_movies_for_city
    from database import insert_collection

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    cities = get_all_cities()

    for city in cities:
        print(f"\n📍 Scraping city: {city}")
        try:
            movies = get_movies_for_city(driver, city)
        except Exception as e:
            print(f"⚠️ Failed to get movies for {city}: {e}")
            continue

        for movie_name, language in movies:
            print(f"🎬 Movie: {movie_name}")
            seat_data_list = get_seat_data(city, movie_name, driver)

            for seat_data in seat_data_list:
                insert_collection(
                    city=city,
                    language=language,
                    movie_name=movie_name,
                    theater=seat_data["theater"],
                    showtime=seat_data["showtime"],
                    seat_breakdown=seat_data["seat_breakdown"],
                    ticket_prices=seat_data["ticket_prices"],
                    estimated_collection=seat_data["estimated_collection"]
                )
                print(f"✅ {movie_name} @ {seat_data['showtime']}: ₹{seat_data['estimated_collection']:,}")

    driver.quit()
