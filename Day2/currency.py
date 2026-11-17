
import csv
from pathlib import Path

import requests

COUNTRIES = {
    "India": "INR",
    "United States": "USD",
    "United Kingdom": "GBP",
    "Japan": "JPY",
    "Singapore": "SGD",
    "Australia": "AUD",
    "Canada": "CAD",
    "Germany": "EUR",
    "France": "EUR",
    "UAE": "AED",
    "China": "CNY",
    "Switzerland": "CHF",
    "Malaysia": "MYR",
    "South Korea": "KRW",
    "Saudi Arabia": "SAR",
    "New Zealand": "NZD",
    "Thailand": "THB",
    "South Africa": "ZAR",
    "Brazil": "BRL",
    "Sri Lanka": "LKR",
}

API_URL = "https://api.frankfurter.app/latest"
CSV_PATH = Path(__file__).with_name("currency_rates.csv")
FALLBACK_RATES = {
    "USD": 1.0,
    "AED": 3.6725,
    "SAR": 3.75,
    "LKR": 322.0,
}


def fetch_exchange_rates():
    """Fetch USD-based exchange rates for all supported currencies."""
    codes = list(dict.fromkeys(COUNTRIES.values()))
    response = requests.get(
        API_URL,
        params={"from": "USD", "to": ",".join(codes)},
        timeout=20,
    )
    response.raise_for_status()

    payload = response.json()
    rates = payload.get("rates", {})
    date = payload.get("date")

    merged = {code: {"rate": rates.get(code), "date": date} for code in codes}
    for code, rate in FALLBACK_RATES.items():
        merged.setdefault(code, {"rate": rate, "date": date})
        if merged[code]["rate"] is None:
            merged[code]["rate"] = rate
    return merged


def write_csv(rows):
    with CSV_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Country", "Currency", "One Dollar", "Date"])
        writer.writerows(rows)


def main():
    try:
        rates = fetch_exchange_rates()

        print("\nCURRENCY EXCHANGE RATES")
        print("Base Currency: 1 USD")
        print("-" * 75)
        print(f"{'Country':<18} {'Currency':<12} {'One Dollar':<18} {'Date'}")
        print("-" * 75)

        rows = []
        for country, currency in COUNTRIES.items():
            rate_entry = rates.get(currency, {})
            rate = rate_entry.get("rate")
            date_value = rate_entry.get("date")

            if rate is not None:
                print(f"{country:<18} {currency:<12} {rate:<18.4f} {date_value}")
                rows.append([country, currency, rate, date_value])
            else:
                print(f"{country:<18} {currency:<12} {'N/A':<18} {'N/A'}")
                rows.append([country, currency, "N/A", "N/A"])

        write_csv(rows)
        print("\nCSV file saved successfully!")
        print(f"File name: {CSV_PATH.name}")

    except requests.exceptions.RequestException as error:
        print("API Error:", error)
    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
