# Sales Data Cleaning

`SalesData.ipynb` cleans the sales records in `messy_sales_data.csv` using
Pandas and saves the result as `cleaned_sales_data.csv`.

## Requirements

- Python
- Jupyter Notebook
- pandas

Install pandas with:

```bash
python -m pip install pandas
```

## Run

1. Place `messy_sales_data.csv` in this directory.
2. Open `SalesData.ipynb` in Jupyter and run the cells in order.

The notebook inspects the data, removes duplicate rows and records missing a
customer name or order date, fills selected missing values, standardizes city
names, parses order dates, and writes the cleaned data to
`cleaned_sales_data.csv`.