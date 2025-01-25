import pandas as pd
import numpy as np
import os

# Read the CSV file from desktop
# You can adjust the path according to your file location
# Using your specific file path
base_path = r"C:\Users\malitha\Desktop\CursorAI\resources"
file_path = os.path.join(base_path, "salesOrders.csv")# Replace with your actual file path

try:
    # Read the CSV file and specify string columns
    df = pd.read_csv(file_path, dtype={
        'Unit Cost': str,
        'Total': str
    })
    
    # Clean and convert data types
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], format='%m/%d/%y')  # Changed from %Y to %y for 2-digit year
    df['Units'] = pd.to_numeric(df['Units'])
    
    # Clean monetary columns by removing spaces, commas and converting to numeric
    df['Unit Cost'] = pd.to_numeric(df['Unit Cost'].str.strip().str.replace(',', ''))
    df['Total'] = pd.to_numeric(df['Total'].str.strip().str.replace(',', ''))
    
    # 1. Descriptive statistics for numeric variables
    print("\nDescriptive Statistics for Numeric Variables:")
    print(df[['Units', 'Unit Cost', 'Total']].describe())
    
    # 2. Frequency distributions and relative frequency for categorical variables
    def print_distribution_stats(df, column):
        freq = df[column].value_counts()
        rel_freq = df[column].value_counts(normalize=True)
        cumulative_freq = freq.cumsum()
        cumulative_rel_freq = rel_freq.cumsum()
        
        stats_df = pd.DataFrame({
            'Frequency': freq,
            'Relative Frequency': rel_freq.round(4),
            'Cumulative Frequency': cumulative_freq,
            'Cumulative Relative Frequency': cumulative_rel_freq.round(4)
        })
        
        print(f"\n{column} Distribution Statistics:")
        print(stats_df)
        print(f"\nTotal {column} Categories: {len(freq)}")
        print(f"Most Common {column}: {freq.index[0]} ({freq.iloc[0]} occurrences)")
        print(f"Least Common {column}: {freq.index[-1]} ({freq.iloc[-1]} occurrences)")
    
    print_distribution_stats(df, 'Region')
    print_distribution_stats(df, 'Rep')
    print_distribution_stats(df, 'Item')
    
    # 3. Time-based statistics
    print("\nTime Period Analysis:")
    print(f"Start Date: {df['OrderDate'].min()}")
    print(f"End Date: {df['OrderDate'].max()}")
    print(f"Total Days: {(df['OrderDate'].max() - df['OrderDate'].min()).days}")
    
    # 4. Additional Analysis
    print("\nSales Analysis by Region:")
    region_analysis = df.groupby('Region').agg({
        'Total': ['sum', 'mean', 'count'],
        'Units': ['sum', 'mean'],
        'Unit Cost': 'mean'
    }).round(2)
    region_analysis.columns = ['Total Sales', 'Avg Sale', 'Number of Orders', 
                             'Total Units', 'Avg Units', 'Avg Unit Cost']
    print(region_analysis)
    
    # Monthly trend analysis
    df['Month'] = df['OrderDate'].dt.to_period('M')
    monthly_sales = df.groupby('Month')['Total'].agg(['sum', 'count']).round(2)
    monthly_sales.columns = ['Monthly Sales', 'Number of Orders']
    print("\nMonthly Sales Trend:")
    print(monthly_sales)
    
except FileNotFoundError:
    print("Error: File not found. Please check the file path.")
except Exception as e:
    print(f"An error occurred: {str(e)}")