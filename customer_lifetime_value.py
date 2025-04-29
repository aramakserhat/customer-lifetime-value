#####################################################
# CUSTOMER LIFETIME VALUE ANALYSIS AND SEGMENTATION
#####################################################

# 1. Business Problem
# 2. Data Preparation
# 3. CLTV Calculation Steps
# 4. Creating of Segments
# 5. Functionalisation of the Whole Process (Script)

##################################################
# 1. Business Problem
##################################################

# The company wants to identify high-value customers and segment them using CLTV metrics.
# This information will be used to prioritize customer relationship management and marketing investments.

# Dataset Story
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# The dataset named "Online Retail II" includes transactions
# from a UK-based online retail store between 01/12/2009 - 09/12/2011.

# Variables
# InvoiceNo: Invoice number. Unique identifier for each transaction. Starts with 'C' if canceled.
# StockCode: Product code. Unique for each product.
# Description: Product name.
# Quantity: Quantity of the product purchased.
# InvoiceDate: Date and time of the invoice.
# UnitPrice: Price of the product (in GBP).
# CustomerID: Unique customer number.
# Country: Country of the customer.

##################################################
# 2. Data Preparation
##################################################

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x )

df_ = pd.read_excel("datasets/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df =df_.copy()

# Initial observations
df.head()
df.shape
df.info()
df.isnull().sum()

# Remove canceled transactions
df["Invoice"] = df["Invoice"].astype(str)
df = df[~df["Invoice"].str.contains("C", na=False)]

df.describe().T

# Removing observation units with a quantity value less than 0 from the dataset
df = df[df["Quantity"] > 0]

# Drop missing values
df.dropna(inplace=True)

# Calculate total price per invoice
df["Total_Price"] = df["Quantity"] * df["Price"]

# Total number of invoices, quantity of products and spending amount on customer basis
cltv_c = df.groupby("Customer ID").agg({"Invoice": lambda x: x.nunique(),
                                        "Quantity": lambda x: x.sum(),
                                        "Total_Price": lambda x: x.sum()})

cltv_c.columns = ["total_transaction", "total_unit", "total_price"]
cltv_c.head()

##################################################
# 3. CLTV Calculation Steps
##################################################

# Average order value (average_order_value = total_price / total_transaction)
cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]

# Purchase frequency (total_transaction / total_number_of_customers)
cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]

# Repeat rate & churn rate (number of customers making more than one purchase / all customers)
repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0]
churn_rate = 1 - repeat_rate

# Profit margin (profit_margin =  total_price * 0.10)
cltv_c["profit_margin"] = cltv_c["total_price"] * 0.10

# Customer value (customer_value = average_order_value * purchase_frequency)
cltv_c["customer_value"] = cltv_c["average_order_value"] * cltv_c["purchase_frequency"]

# Customer lifetime value (CLTV = (customer_value / churn_rate) x profit_margin)
cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]
cltv_c.sort_values(by="cltv", ascending=False).head()

###############################
# 4. Creating of Segments
###############################

cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])
cltv_c.sort_values(by="cltv", ascending=False).head()

# Analysis of segments
cltv_c.groupby("segment").agg({"count", "mean", "sum"})

# Export of analysis results as .csv
cltv_c.to_csv("cltv_c.csv")

##################################################
# 5. Functionalisation of the Whole Process (Script)
##################################################

def create_cltv_c(dataframe, csv=False):

    # Data preparation
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe.dropna(inplace=True)
    dataframe["Total_Price"] = dataframe["Quantity"] * dataframe["Price"]
    cltv_c = dataframe.groupby("Customer ID").agg({"Invoice": lambda x: x.nunique(),
                                            "Quantity": lambda x: x.sum(),
                                            "Total_Price": lambda x: x.sum(), })
    cltv_c.columns = ["total_transaction", "total_unit", "total_price"]

    # Average order value
    cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]

    # Purchase frequency
    cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]

    # Repeat rate & churn rate
    repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate

    # Profit margine
    cltv_c["profit_margin"] = cltv_c["total_price"] * 0.10

    # Customer value
    cltv_c["customer_value"] = cltv_c["average_order_value"] * cltv_c["purchase_frequency"]

    # Customer lifetime value
    cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]

    # Creating of segments
    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

    if csv:
        cltv_c.to_csv("cltv_c.csv")

    return cltv_c

df = df_.copy()
create_cltv_c(df)
cltv_c.head()
