import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for better visualizations
plt.style.use('default')  # Using default style instead of seaborn
sns.set()  # This will set the seaborn defaults

# Define meaningful labels for axes
axis_labels = {
    'Units': 'Order Unit Count',
    'Unit Cost': 'Cost per Unit ($)',
    'Total': 'Total Sales ($)',
    'Region': 'Sales Region',
    'Rep': 'Sales Representative',
    'Item': 'Product Item'
}

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
    
    # Set figure style
    plt.rcParams['figure.figsize'] = [10, 6]
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['axes.grid'] = True
    
    # 1. Quantitative Variables Analysis
    fig, axes = plt.subplots(2, 3, figsize=(22, 14))
    fig.suptitle('Distribution of Quantitative Variables', fontsize=16, y=1.02)
    
    # Increase spacing between subplots
    plt.subplots_adjust(wspace=0.4, hspace=0.5, bottom=0.1, top=0.9, left=0.1, right=0.95)
    
    # Histograms and Box plots
    for i, column in enumerate(['Units', 'Unit Cost', 'Total']):
        # Histogram
        sns.histplot(data=df, x=column, kde=True, ax=axes[0, i])
        axes[0, i].set_title(f'Histogram of {axis_labels[column]}', pad=10)
        axes[0, i].set_xlabel(axis_labels[column])
        axes[0, i].set_ylabel('Frequency of Orders')
        
        # Adjust label padding
        axes[0, i].tick_params(axis='x', labelrotation=45, pad=10)
        axes[0, i].tick_params(axis='y', pad=10)
        
        # Box plot
        sns.boxplot(data=df, y=column, ax=axes[1, i])
        axes[1, i].set_title(f'Box Plot of {axis_labels[column]}', pad=10)
        axes[1, i].set_ylabel(axis_labels[column])
        axes[1, i].tick_params(axis='y', pad=10)
    
    plt.show()
    
    # 2. Categorical Variables Analysis
    # Bar Charts
    fig, axes = plt.subplots(3, 1, figsize=(6, 8))
    fig.suptitle('Distribution Analysis', fontsize=10, y=1.02)
    
    # Increase spacing between subplots but keep it very compact
    plt.subplots_adjust(hspace=0.6, bottom=0.1, top=0.9, left=0.2, right=0.95)
    
    for i, column in enumerate(['Region', 'Rep', 'Item']):
        # Bar Chart
        counts = df[column].value_counts()
        ax = counts.plot(kind='bar', ax=axes[i], width=0.6)
        axes[i].set_title(f'{axis_labels[column]}', pad=5, fontsize=9)
        axes[i].set_xlabel('', labelpad=5)  # Remove x-label as it's redundant with title
        axes[i].set_ylabel('Count', labelpad=5, fontsize=8)
        
        # Adjust x-axis labels
        if column in ['Rep', 'Item']:
            axes[i].tick_params(axis='x', rotation=45, pad=5, labelsize=7)
            axes[i].set_xticklabels(axes[i].get_xticklabels(), ha='right')
        else:
            axes[i].tick_params(axis='x', rotation=30, pad=5, labelsize=7)
        
        # Adjust y-axis labels
        axes[i].tick_params(axis='y', labelsize=7)
        
        # Add value labels on top of each bar
        for p in ax.patches:
            ax.annotate(str(int(p.get_height())), 
                       (p.get_x() + p.get_width()/2., p.get_height()),
                       ha='center', va='bottom', fontsize=7,
                       xytext=(0, 1), textcoords='offset points')
        
        # Remove grid for cleaner look in small size
        axes[i].grid(False)
        
        # Tighten y-axis range
        axes[i].set_ylim(0, max(counts) * 1.15)  # Add 15% padding for labels
    
    plt.tight_layout()
    plt.show()
    
    # Pie Charts
    fig, axes = plt.subplots(3, 1, figsize=(12, 16))
    fig.suptitle('Percentage Distribution Analysis', fontsize=16, y=1.02)
    
    # Increase spacing between subplots
    plt.subplots_adjust(hspace=0.3, bottom=0.05, top=0.95)
    
    for i, column in enumerate(['Region', 'Rep', 'Item']):
        # Pie Chart
        counts = df[column].value_counts()
        counts.plot(kind='pie', autopct='%1.1f%%', ax=axes[i])
        axes[i].set_title(f'Percentage Distribution by {axis_labels[column]}', pad=20)
        # Add legend to the right side
        axes[i].legend(counts.index, title=axis_labels[column], 
                      bbox_to_anchor=(1.2, 0.5), loc='center left')
    
    plt.show()
    
    # 3. Time Series Analysis
    # Daily Sales Trend
    plt.figure(figsize=(22, 12))
    daily_sales = df.groupby('OrderDate')['Total'].sum()
    daily_sales.plot(kind='line')
    plt.title('Daily Sales Trend Over Time', y=1.05, pad=20)
    plt.xlabel('Order Date', labelpad=15)
    plt.ylabel('Total Sales ($)', labelpad=15)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.2, left=0.1, right=0.95, top=0.9)
    plt.show()
    
    # Monthly trend
    plt.figure(figsize=(22, 12))
    monthly_sales = df.groupby(df['OrderDate'].dt.to_period('M'))['Total'].sum()
    monthly_sales.plot(kind='bar')
    plt.title('Monthly Sales Distribution', y=1.05, pad=20)
    plt.xlabel('Month', labelpad=15)
    plt.ylabel('Total Sales ($)', labelpad=15)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.subplots_adjust(bottom=0.2, left=0.1, right=0.95, top=0.9)
    plt.show()
    
    # 4. Relationship Analysis
    # Scatter plot
    plt.figure(figsize=(16, 12))
    plt.scatter(df['Units'], df['Total'])
    plt.title('Relationship between Order Units and Total Sales', y=1.05, pad=20)
    plt.xlabel('Order Unit Count', labelpad=15)
    plt.ylabel('Total Sales ($)', labelpad=15)
    plt.grid(True)
    plt.subplots_adjust(bottom=0.15, left=0.1, right=0.95, top=0.9)
    plt.show()
    
    # Box plot by Region
    plt.figure(figsize=(16, 12))
    sns.boxplot(data=df, x='Region', y='Total')
    plt.title('Sales Distribution by Region', y=1.05, pad=20)
    plt.xlabel('Sales Region', labelpad=15)
    plt.ylabel('Total Sales ($)', labelpad=15)
    plt.xticks(rotation=30)
    plt.grid(True)
    plt.subplots_adjust(bottom=0.15, left=0.1, right=0.95, top=0.9)
    plt.show()

    # Sales Performance Analysis by Representative
    plt.figure(figsize=(10, 6))
    
    # Calculate total sales for each representative
    rep_sales = df.groupby('Rep')['Total'].sum().sort_values(ascending=True)
    
    # Create bar plot
    ax = rep_sales.plot(kind='barh', width=0.7)
    plt.title('Total Sales by Sales Representative', pad=15, fontsize=12)
    plt.xlabel('Total Sales ($)', labelpad=10, fontsize=10)
    plt.ylabel('Sales Representative', labelpad=10, fontsize=10)
    
    # Adjust labels and ticks
    plt.tick_params(axis='both', labelsize=9)
    
    # Add value labels on the bars
    for i, v in enumerate(rep_sales):
        ax.text(v + (v * 0.01), i,  # Slight offset from end of bar
                f'${v:,.0f}', 
                va='center',
                fontsize=8)
    
    # Remove grid for cleaner look
    plt.grid(False)
    
    # Add some padding to the right for labels
    plt.margins(x=0.2)
    
    # Adjust layout
    plt.tight_layout()
    
    plt.show()

except FileNotFoundError:
    print("Error: File not found. Please check the file path.")
except Exception as e:
    print(f"An error occurred: {str(e)}")