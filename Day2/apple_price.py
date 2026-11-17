
import csv
from datetime import date, timedelta
from pathlib import Path
from statistics import median

import requests

BASE_URL = "https://mandi-api.onrender.com/v1/prices/history"
STATES = [
    "Maharashtra",
    "Uttar Pradesh",
    "Punjab",
    "Madhya Pradesh",
    "Karnataka",
]
CSV_PATH = Path(__file__).with_name("apple_3months.csv")


def fetch_apple_prices():
    """Collect apple price data from the Mandi API across supported states."""
    today = date.today()
    from_date = today - timedelta(days=90)
    all_prices = {}

    print("Fetching Apple price history...")

    for state in STATES:
        params = {
            "state": state,
            "commodity": "Apple",
            "from": from_date.isoformat(),
            "to": today.isoformat(),
        }

        try:
            response = requests.get(
                BASE_URL,
                params=params,
                headers={"Accept": "application/json"},
                timeout=(10, 60),
            )
            response.raise_for_status()
            body = response.json()

            if body.get("success") is not True:
                print(state, "API returned an error")
                continue

            records = body.get("data", [])
            print(state, "- Records:", len(records))

            for item in records:
                date_text = item.get("arrival_date") or item.get("date")
                price = (
                    item.get("avg_modal_price")
                    or item.get("average_modal_price")
                    or item.get("modal_price")
                    or item.get("avg_price")
                    or item.get("price")
                )

                if not date_text or price is None:
                    continue

                try:
                    record_date = date.fromisoformat(str(date_text)[:10])
                    price_value = float(price)

                    if price_value <= 0:
                        continue

                    if from_date <= record_date <= today:
                        all_prices.setdefault(record_date.isoformat(), []).append(price_value)
                except (TypeError, ValueError):
                    continue

        except requests.RequestException as error:
            print(state, "Error:", error)

    results = []
    for date_text, prices in all_prices.items():
        median_price = median(prices)
        results.append({
            "Date": date_text,
            "Apple Price (Rs/kg)": round(median_price / 100, 2),
        })

    results.sort(key=lambda item: item["Date"])
    return results


def write_csv(results):
    with CSV_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Apple Price (Rs/kg)"])
        writer.writeheader()
        writer.writerows(results)


def main():
    results = fetch_apple_prices()

    print("\n       APPLE DAILY PRICE")
    print("------------------------------------")
    print("Date             Apple Price (Rs/kg)")
    print("------------------------------------")

    for row in results:
        print(f"{row['Date']}          {row['Apple Price (Rs/kg)']:.2f}")

    print("------------------------------------")

    if results:
        write_csv(results)
        print("CSV file saved successfully!")
    else:
        print("No usable history data found.")
        print("Please check the API response.")

    print("Total days:", len(results))


if __name__ == "__main__":
    main()
