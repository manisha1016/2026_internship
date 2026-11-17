# Data Fetching Project

This project collects and stores market data from public APIs and saves it as CSV files in the project root.

## Included Scripts

- `currency.py` — fetches live USD-based exchange rates for major world currencies and saves them to `currency_rates.csv`.
- `apple_price.py` — collects daily apple price data from the Mandi API for the last 90 days and saves the results to `apple_3months.csv`.

## Requirements

Install the required Python package:

```bash
pip install requests
```

## Run the scripts

```bash
python currency.py
python apple_price.py
```

## Output files

- `currency_rates.csv` — country, currency, one-dollar conversion value, and rate date.
- `apple_3months.csv` — date and median apple price in Rs/kg.

## Notes

- The scripts rely on external APIs and may fail if the remote services are unavailable or rate-limited.
- The CSV files are generated in the same directory as the Python scripts.
