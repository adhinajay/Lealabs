import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV Data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully")
        return data
    except FileNotFoundError:
        print("Error: The file", file_path, "does not exist.")
        return None

# Process the data
def process_data(data):
    # Handle missing values only in numeric columns
    numeric_cols = data.select_dtypes(include='number').columns
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())
    return data

# Plot the results
def plot_data(data):
    # Plotting a histogram of 'Item_Outlet_Sales'
    if 'Item_Outlet_Sales' in data.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(data['Item_Outlet_Sales'], kde=True, color='blue', bins=20)
        plt.title('Item Outlet Sales Distribution')
        plt.xlabel('Item Outlet Sales')
        plt.ylabel('Frequency')
        plt.show()

# Main function
def main():
    file_path = 'WEEK1/MAY9/final_project/sales_data.csv'
    data = load_data(file_path)

    if data is not None:
        processed_data = process_data(data)
        plot_data(processed_data)

if __name__ == "__main__":
    main()