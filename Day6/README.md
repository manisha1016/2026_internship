# Zoho Careers Job Scraper

A Python and Playwright scraper that collects active job openings from the Zoho Careers portal and exports the results to CSV.

## Features

- Scrapes all job cards from `https://careers.zohocorp.com/jobs/Careers`
- Optionally opens each job page to collect the full description
- Filters openings by a role keyword in the title or description
- Detects common Tamil Nadu and Bengaluru/Hyderabad locations
- Saves results as UTF-8 CSV files
- Prints a summary table in the terminal

## Requirements

- Python 3.9 or newer
- `pandas`
- `playwright` for Python

Install the dependencies:

```powershell
python -m pip install pandas playwright
python -m playwright install chromium
```

## Usage

Run the scraper from the project directory:

```powershell
python job_scraper.py
```

The default output file is:

```text
output/zoho_jobs_<YYYY-MM-DD>.csv
```

## Command-Line Options

| Option | Description |
|---|---|
| `--out <path>` | Save to a custom CSV path |
| `--role <keyword>` | Keep jobs containing the keyword in the title or description |
| `--headed` | Open a visible browser window instead of running headless |
| `--no-description` | Skip opening detail pages for faster extraction |

Examples:

```powershell
# Filter for support roles
python job_scraper.py --role "Support"

# Filter for developer roles and save to a custom file
python job_scraper.py --role "Developer" --out output/developer_jobs.csv

# Run faster without fetching full descriptions
python job_scraper.py --no-description

# Run Chromium in visible/headed mode
python job_scraper.py --headed
```

## Output Columns

The generated CSV contains:

| Column | Description |
|---|---|
| `company` | Company name (`Zoho`) |
| `job_id` | Job identifier extracted from the detail URL |
| `title` | Job title |
| `location` | Detected location information |
| `job_type` | Employment type, such as `Full time` |
| `description` | Card summary or full detail-page description |
| `url` | Link to the job opening |
| `extracted_date` | Date the data was collected in `YYYY-MM-DD` format |

## Notes

- Zoho's website structure or availability can change, which may require selector updates in `job_scraper.py`.
- If no jobs are found, check your internet connection and Zoho Careers portal availability.
- A role filter may match words in either the job title or full description.
- An existing detail page that cannot be loaded is skipped, while the card summary is retained.
