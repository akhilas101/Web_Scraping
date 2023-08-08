import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.flipkart.com/watches/pr?sid=r18"

headers = {
    "User-Agent": "Your User Agent String"
}

max_retries = 5
retry_delay = 5  # seconds

watch_data = []

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
watch_cards = soup.find_all("div", class_="_1AtVbE")

for watch_card in watch_cards:
    try:
        watch_name_elem = watch_card.find("div", class_="_4rR01T")
        watch_name = watch_name_elem.text.strip() if watch_name_elem else "N/A"
        
        watch_price_elem = watch_card.find("div", class_="_30jeq3")
        watch_price = watch_price_elem.text.strip() if watch_price_elem else "N/A"
        
        watch_rating_elem = watch_card.find("div", class_="_3LWZlK")
        watch_rating = watch_rating_elem.text.strip() if watch_rating_elem else "N/A"
        
        watch_data.append({
            "Name": watch_name,
            "Price": watch_price,
            "Rating": watch_rating
        })
    except Exception as e:
        print("Error in extracting watch data:", e)

df = pd.DataFrame(watch_data)
df.to_csv("flipkart_watches.csv", index=False)

print("Data successfully extracted and CSV saved.")
