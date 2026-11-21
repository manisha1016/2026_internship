#!/usr/bin/env python3
"""Standalone scraper for Zoho Corporation job openings (careers.zohocorp.com).

Usage:
    python extract_zoho.py
    python extract_zoho.py --headed
    python extract_zoho.py --role "Support"
    python extract_zoho.py --out output/my_zoho_jobs.csv
"""
import argparse
import html
import os
import re
from datetime import date, datetime
import pandas as pd
from playwright.sync_api import sync_playwright

ZOHO_CAREERS_URL = "https://careers.zohocorp.com/jobs/Careers"
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def clean_text(text: str) -> str:
    """Strip HTML tags and convert block tags to clean whitespace/newlines."""
    if not text:
        return ""
    s = html.unescape(str(text))
    s = re.sub(r"<(?:br|p|div|li|tr|h\d)\b[^>]*>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", " ", s)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in s.splitlines()]
    return "\n".join(l for l in lines if l).strip()


def extract_zoho_jobs(headed: bool = False, fetch_details: bool = True, role_filter: str = "") -> list:
    """Scrape all job postings from Zoho careers portal."""
    jobs = []
    today_iso = date.today().isoformat()

    print(f"Connecting to Zoho Careers: {ZOHO_CAREERS_URL} ...")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)
        context = browser.new_context(user_agent=USER_AGENT)
        page = context.new_page()

        try:
            page.goto(ZOHO_CAREERS_URL, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_selector(".joblist-card", timeout=15000)
        except Exception as exc:
            print(f"Error loading page: {exc}")
            browser.close()
            return []

        cards = page.query_selector_all(".joblist-card")
        print(f"Found {len(cards)} active job opening(s) on Zoho Careers.")

        for idx, card in enumerate(cards, start=1):
            t_el = card.query_selector("a.cw-2-title")
            title = (t_el.inner_text() if t_el else "").strip()
            href = t_el.get_attribute("href") if t_el else ""

            # Check role filter early if title doesn't match
            if role_filter and role_filter.lower() not in title.lower():
                # We will check description as well if details are fetched
                pass

            # Extract job ID from URL
            m_id = re.search(r"/(\d{10,})", href)
            job_id = m_id.group(1) if m_id else ""

            # Fallback summary text from card
            card_text_el = card.query_selector(".card-text")
            card_desc = card_text_el.inner_text().strip() if card_text_el else ""

            # Type indicator (e.g. Full time)
            type_el = card.query_selector(".cw-full-time, .clearfix span")
            job_type = type_el.inner_text().strip() if type_el else "Full time"

            description = card_desc
            location = "India"
            industry = "Technology"

            if fetch_details and href:
                print(f"[{idx}/{len(cards)}] Fetching details: {title} ...")
                try:
                    det_page = context.new_page()
                    det_page.goto(href, wait_until="domcontentloaded", timeout=15000)

                    # Extract full description
                    d_el = det_page.query_selector(".cw-jobdescription, [class*='jobdesc'], [class*='description']")
                    if d_el:
                        description = clean_text(d_el.inner_text().strip())

                    # Extract detailed metadata (country/location)
                    info_el = det_page.query_selector(".cw-jobheader-information")
                    if info_el:
                        info_text = info_el.inner_text().strip()
                        if "India" in info_text:
                            location = "India"

                    # Check for specific cities mentioned in description
                    cities = ["Chennai", "Coimbatore", "Tenkasi", "Salem", "Tirunelveli", "Madurai", "Bengaluru", "Hyderabad"]
                    found_cities = [c for c in cities if c.lower() in description.lower()]
                    if found_cities:
                        location = f"India ({', '.join(found_cities)})"

                    det_page.close()
                except Exception as exc:
                    print(f"   Warning: could not fetch details for {title}: {exc}")

            # Apply role filter if specified
            if role_filter:
                r_lower = role_filter.lower()
                if r_lower not in title.lower() and r_lower not in description.lower():
                    continue

            job_entry = {
                "company": "Zoho",
                "job_id": job_id,
                "title": title,
                "location": location,
                "job_type": job_type,
                "description": description,
                "url": href,
                "extracted_date": today_iso,
            }
            jobs.append(job_entry)

        browser.close()

    return jobs


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="", help="output CSV file path (default: output/zoho_jobs_<date>.csv)")
    parser.add_argument("--role", default="", help="filter by role keyword (e.g. 'Support', 'Sales', 'Developer')")
    parser.add_argument("--headed", action="store_true", help="run browser in visible/headed mode")
    parser.add_argument("--no-description", action="store_true", help="skip opening detail pages for faster extraction")
    args = parser.parse_args()

    today_iso = date.today().isoformat()
    default_out = os.path.join("output", f"zoho_jobs_{today_iso}.csv")
    out_path = args.out or default_out
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    jobs = extract_zoho_jobs(
        headed=args.headed,
        fetch_details=not args.no_description,
        role_filter=args.role
    )

    if not jobs:
        print("\nNo jobs extracted. (If filtering by role, try a broader keyword).")
        return

    df = pd.DataFrame(jobs)
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"\nSuccessfully extracted {len(df)} job(s) from Zoho.")
    print(f"Saved to: {out_path}\n")

    # Display clean summary table in console
    display_df = df[["job_id", "title", "location", "job_type", "url"]].copy()
    print(display_df.to_string(index=False))


if __name__ == "__main__":
    main()