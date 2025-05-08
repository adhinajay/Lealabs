# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df=pd.read_csv('WEEK1\MAY8\plot_bar_chart\sales_data.csv')

# Group data by 'Item_Type' and calculate the average sales for each type
avg_sales_per_item=df.groupby('Item_Type')['Item_Outlet_Sales'].mean().sort_values(ascending=False)

# Set the figure size for the plot
plt.figure(figsize=(12,6))

# Plot the bar chart
avg_sales_per_item.plot(kind='bar' ,color='skyblue', edgecolor='black') 

# Set chart title and labels
plt.title('Average Sales per Item Type')
plt.xlabel('Item Type')
plt.ylabel('Average Sales')

# Rotate x-axis labels to avoid overlap and align right
plt.xticks(rotation=45, ha='right') 

# Add grid lines on the y-axis
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust layout to prevent clipping of tick labels
plt.tight_layout()

# Display the plot
plt.show()