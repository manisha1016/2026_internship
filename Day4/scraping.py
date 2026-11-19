
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import re
import time

# STEP 1: Website URL
base_url = "https://books.toscrape.com/"

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

response = session.get(base_url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

print("Website Connected Successfully!")

# STEP 2: Get all categories
category_tags = soup.select("ul.nav-list ul li a")

categories = []

for tag in category_tags:

    category_name = tag.get_text(strip=True)
    category_url = urljoin(base_url, tag["href"])

    categories.append({
        "Category": category_name,
        "URL": category_url
    })

print("Total Categories:", len(categories))

# STEP 3: Create empty list
all_books = []

# STEP 4: Visit each category
for category in categories:

    category_name = category["Category"]
    current_url = category["URL"]

    print("\nCategory:", category_name)

    # STEP 5: Visit all pages
    while current_url:

        response = session.get(current_url)
        response.raise_for_status()

        soup = BeautifulSoup(
            response.text, "html.parser"
        )

        books = soup.find_all(
            "article", class_="product_pod"
        )

        # STEP 6: Extract book details
        for book in books:

            # Book name
            name = book.h3.a["title"]

            # Price with £ symbol
            price = book.find(
                "p", class_="price_color"
            ).get_text(strip=True)

            price = price.replace("Â", "")

            # Rating
            rating = book.find(
                "p", class_="star-rating"
            )["class"][1]

            # Individual book page
            book_url = urljoin(
                current_url,
                book.h3.a["href"]
            )

            detail_response = session.get(book_url)
            detail_response.raise_for_status()

            detail_soup = BeautifulSoup(
                detail_response.text,
                "html.parser"
            )

            # STEP 7: Extract available quantity
            availability = detail_soup.find(
                "p", class_="instock availability"
            )

            if availability:

                availability_text = availability.get_text(
                    " ", strip=True
                )

                match = re.search(
                    r"\((\d+)\s+available\)",
                    availability_text
                )

                if match:
                    quantity = int(match.group(1))
                else:
                    quantity = 0

            else:
                quantity = 0

            # STEP 8: Store data
            all_books.append({

                "Category": category_name,
                "Book Name": name,
                "Price": price,
                "Rating": rating,
                "Availability": quantity

            })

            print(name, price, quantity)

            time.sleep(0.2)

        # STEP 9: Next page
        next_page = soup.find(
            "li", class_="next"
        )

        if next_page:

            next_link = next_page.a["href"]

            current_url = urljoin(
                current_url, next_link
            )

        else:
            current_url = None

        time.sleep(0.2)

# STEP 10: Convert to DataFrame
df = pd.DataFrame(all_books)

# STEP 11: Save Excel
df.to_excel(
    "Books_Data.xlsx",
    index=False
)

# STEP 12: Final output
print("\n========================")
print("SCRAPING COMPLETED!")
print("========================")

print("Total Books:", len(df))

print(
    "Total Categories:",
    df["Category"].nunique()
)

print("\nFirst 10 Records:")
print(df.head(10))

print("\nExcel file saved successfully!")
