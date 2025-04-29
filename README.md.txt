# Customer Lifetime Value (CLTV) Analysis and Segmentation

## Overview

This project involves calculating **Customer Lifetime Value (CLTV)** to identify and segment high-value customers for a UK-based e-commerce company. By estimating the long-term value a customer brings, businesses can develop more informed strategies around customer retention, loyalty programs, and marketing investment.

The analysis is based on transactional data from the "Online Retail II" dataset, covering a period from **2009 to 2010**. It includes customer purchase behavior such as frequency, monetary value, and repeat rate, which are used to estimate CLTV and assign customer segments accordingly.

## Table of Contents

1. [Business Problem](#business-problem)  
2. [Data Understanding](#data-understanding)  
3. [Data Preparation](#data-preparation)  
4. [CLTV Metrics Calculation](#cltv-metrics-calculation)  
5. [Customer Segmentation](#customer-segmentation)  
6. [Functions](#functions)

---

## Business Problem

An e-commerce company wants to prioritize customer retention efforts by understanding which customers are the most valuable in the long term. The goal is to **calculate CLTV** using historical transaction data and segment customers into quartiles (A to D) based on their estimated value.

---

## Data Understanding

The dataset "Online Retail II" contains online transactions made by customers between 2009 and 2010. It includes the following fields:

- `Invoice`: Invoice number, uniquely identifying each transaction (prefix 'C' denotes a cancellation)  
- `StockCode`: Product identifier  
- `Description`: Product name  
- `Quantity`: Number of units purchased  
- `InvoiceDate`: Date and time of transaction  
- `Price`: Unit price (in GBP)  
- `Customer ID`: Unique identifier for each customer  
- `Country`: Country of customer  

---

## Data Preparation

To prepare the data for CLTV analysis, the following steps were applied:

- Canceled transactions (`Invoice` starting with 'C') were removed  
- Negative or zero `Quantity` values were filtered out  
- Rows with missing values were dropped  
- A new feature `Total_Price` was calculated as `Quantity * Price`  

The resulting dataset represents clean transaction records for valid customer purchases.

---

## CLTV Metrics Calculation

The CLTV model was computed in several stages:

1. **Total Transactions, Quantity, and Spending per Customer**  
   Aggregated using the number of invoices, sum of quantities, and total price

2. **Average Order Value (AOV)**  
   `AOV = total_price / total_transaction`

3. **Purchase Frequency**  
   `purchase_frequency = total_transaction / total_number_of_customers`

4. **Repeat Rate and Churn Rate**  
   - `repeat_rate = # of customers with >1 purchase / total customers`  
   - `churn_rate = 1 - repeat_rate`

5. **Profit Margin**  
   Estimated as 10% of `total_price`  

6. **Customer Value**  
   `customer_value = average_order_value * purchase_frequency`

7. **Customer Lifetime Value (CLTV)**  
   `CLTV = (customer_value / churn_rate) * profit_margin`

---

## Customer Segmentation

To facilitate actionable insights, customers were segmented into four groups using **quantile-based segmentation**:

- **Segment A**: Top 25% CLTV customers  
- **Segment B**: Upper-middle 25%  
- **Segment C**: Lower-middle 25%  
- **Segment D**: Bottom 25%

Segment-level analysis enables targeted marketing strategies by focusing efforts on high-value groups.

---

## Functions

Reusable functions were created to automate the CLTV calculation and segmentation process.

### `create_cltv_c(dataframe, csv=False)`

Calculates CLTV and assigns segments. Optionally exports results to CSV.

**Parameters**:  
- `dataframe`: Cleaned transactional dataset  
- `csv`: Boolean flag to export output  

**Returns**:  
- DataFrame containing CLTV metrics and segment labels

---

## Example Usage

```python
# Load dataset
import pandas as pd
df = pd.read_excel("datasets/online_retail_II.xlsx", sheet_name="Year 2009-2010")

# Run CLTV pipeline
cltv_results = create_cltv_c(df, csv=True)

# View high-value customers
cltv_results[cltv_results["segment"] == "A"].head()
