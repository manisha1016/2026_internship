# Book Data Scraper

This project scrapes book listings from [Books to Scrape](https://books.toscrape.com/)
and saves the collected information in an Excel file.

## What the scraper does

The script in [scraping.py](scraping.py):

- Connects to the Books to Scrape website
- Retrieves all book categories
- Visits every listing page in each category
- Visits each book's individual page
- Extracts the book name, category, price, rating, and available quantity
- Saves the collected records to `Books_Data.xlsx`
- Prints progress and summary information in the terminal

## Data columns

The generated Excel file contains these columns:

- `Category`
- `Book Name`
- `Price`
- `Rating`
- `Availability`

## Requirements

Install the required Python packages:

```bash
python -m pip install requests beautifulsoup4 pandas openpyxl
```

## Run the scraper

From this directory, run:

```bash
python scraping.py
```

The script creates or updates:

```text
Books_Data.xlsx
```

## Notes

- The script is intended for the public training website [Books to Scrape](https://books.toscrape.com/).
- Network availability and website changes can affect scraping.
- Short delays are included between requests to reduce the request rate.