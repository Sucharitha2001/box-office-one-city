def get_movies_for_city(driver, city):
    driver.get(f"https://in.bookmyshow.com/explore/home/{city}")
    time.sleep(5)

    movie_cards = driver.find_elements(By.CLASS_NAME, "card-title")
    movies = []

    for card in movie_cards:
        title = card.text
        try:
            lang_element = card.find_element(By.XPATH, ".//following-sibling::div")
            language = lang_element.text.split("|")[0].strip()
        except:
            language = "Unknown"
        movies.append((title, language))

    return movies
