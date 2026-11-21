# Customer Orders Data Cleaning and Visualization

## 1. Project Overview

This project focuses on cleaning customer order data using Python Pandas and analyzing the cleaned dataset through different data visualizations.

The project helps to understand customer age groups, monthly order trends, order status, customer age distribution, email providers, and payment methods.

## 2. Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn

## 3. Libraries Used

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

## 4. Dataset

**Input Dataset:** `cleaned_orders.csv`

**Updated Dataset:** `cleaned_orders_updated1.csv`

The dataset contains customer and order-related information such as:

- Customer Age
- Order ID
- Order Date
- Order Status
- Payment Method
- Product Category
- Customer Email

## 5. Data Cleaning

The following data cleaning operations were performed:

1. Loaded the CSV dataset using Pandas.
2. Replaced `cod` with `cash on delivery` in payment methods.
3. Converted product categories into uppercase.
4. Converted payment methods into uppercase.
5. Saved the updated dataset as `cleaned_orders_updated1.csv`.

## 6. Data Visualization

The following visualizations were created using Matplotlib and Seaborn.

### 1. Customer Age Group Distribution – Bar Chart

- Divided customers into four age groups:
  - Young (18–25)
  - Middle (26–40)
  - Adult (41–60)
  - Old (61–100)
- Displayed the number of customers in each age group.

### 2. Monthly Order Trend – Line Chart

- Converted order dates into datetime format.
- Grouped orders by month and year.
- Displayed monthly order trends using a line chart.
- Added order counts above each data point.

### 3. Order Status Distribution – Pie Chart

- Counted orders based on their status.
- Displayed the percentage of each order status.
- Visualized the results using a pie chart.

### 4. Customer Age Distribution – Histogram

- Analyzed customer age distribution.
- Used 10 bins to group customer ages.
- Displayed frequency values above the bars.

### 5. Email Provider Count – Count Plot

- Extracted email providers from customer email addresses.
- Counted customers based on email providers.
- Visualized the results using Seaborn Count Plot.

## 7. Project Folder Structure

```text
Customer_Order_Analysis/
│
├── cleaned_orders.csv
├── cleaned_orders_updated1.csv
├── data_cleaning.py
├── data_visualization.py
└── README.md
```

## 8. Installation

Install the required Python libraries:

```bash
pip install pandas matplotlib seaborn
```

## 9. How to Run the Project

**Step 1:** Open the project folder in VS Code.

**Step 2:** Run the data cleaning program.

```bash
python data_cleaning.py
```

**Step 3:** Run the data visualization program.

```bash
python data_visualization.py
```

**Step 4:** View the generated charts.

## 10. Expected Output

The project generates the following visualizations:

1. Customer Age Group Distribution
2. Monthly Order Trend
3. Order Status Distribution
4. Customer Age Distribution
5. Email Provider Count

## 11. Conclusion

This project demonstrates how Python can be used for data cleaning and exploratory data analysis.

Pandas helps to clean and organize customer order data, while Matplotlib and Seaborn help to visualize the data and understand useful patterns and trends.

## 12. Skills Learned

- Data Cleaning using Pandas
- Data Transformation
- Data Analysis
- Data Visualization
- CSV File Handling
- Python Programming
