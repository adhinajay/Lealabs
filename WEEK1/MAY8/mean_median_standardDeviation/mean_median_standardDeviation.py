# Import necessary libraries
import numpy as np
import pandas as pd

#Load dataset
df = pd.read_csv("WEEK1/MAY8/mean_median_standardDeviation/sales_data.csv")  

# Converts to NumPy array
sales_data = df['Item_Outlet_Sales'].values  

# Calculate statistics
mean_sales = np.mean(sales_data)
median_sales = np.median(sales_data)
std_sales = np.std(sales_data)

# Print results
print("Mean:", mean_sales)
print("Median:", median_sales)
print("Standard Deviation:", std_sales)