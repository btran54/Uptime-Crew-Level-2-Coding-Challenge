import pandas as pd
import numpy as np

# Helper Functions

def print_section_header(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

def create_count_summary(counts, total_rows):
    percentages = (counts / total_rows * 100).round(2)
    return pd.DataFrame({
        'Count': counts,
        'Percentage': percentages
    })

def print_formatted_dataframe(df_csv, formatters):
    print(df_csv.to_string(formatters=formatters))

def print_top_n_with_currency(series, title, n=5):
    print(f"\n{title}:")
    top_items = series.nlargest(n)
    for i, (name, value) in enumerate(top_items.items(), 1):
        print(f"{i}. {name}: ${value:,.2f}")

def calculate_group_statistics(df_csv, group_column, value_column, total_value):
    group_sum = df_csv.groupby(group_column, sort=False)[value_column].sum()
    percentages = (group_sum / total_value * 100).round(2)
    
    return pd.DataFrame({
        'Total': group_sum,
        'Percentage': percentages
    })

def analyze_shopping_data(file_path='customer_shopping_data.csv'):
    
    # Task 1: Read CSV with optimized datatypes
    dtypes = {
        'invoice_no': 'string',
        'customer_id': 'string',
        'gender': 'category',
        'age': 'int16',
        'category': 'category',
        'quantity': 'int16',
        'price': 'float32',
        'payment_method': 'category',
        'invoice_date': 'string',
        'shopping_mall': 'category'
    }
    
    df_csv = pd.read_csv(file_path, dtype=dtypes)
    print(f"Successfully loaded {len(df_csv):,} rows\n")
    
    # Pre-calculate values
    df_csv['sales'] = df_csv.eval('quantity * price')
    total_rows = len(df_csv)
    total_revenue = df_csv['sales'].sum()
    
    # Task 2 & 3: Population count AND total sales by gender
    print_section_header("Population Count by Gender")
    
    gender_stats = df_csv.groupby('gender', sort=False, observed=True).agg({
        'customer_id': 'size',
        'sales': 'sum'
    })
    gender_stats.columns = ['Count', 'Total Sales']
    
    gender_stats['Count %'] = (gender_stats['Count'] / total_rows * 100).round(2)
    gender_stats['Sales %'] = (gender_stats['Total Sales'] / total_revenue * 100).round(2)
    
    count_summary = gender_stats[['Count', 'Count %']]
    count_summary.columns = ['Count', 'Percentage']
    
    print_formatted_dataframe(count_summary, {
        'Count': lambda x: f"{x:,}",
        'Percentage': lambda x: f"{x:.2f}%"
    })
    print(f"\nTotal: {total_rows:,}")
    
    # Task 3: Display sales summary
    print_section_header("Total Sales by Gender")
    
    sales_summary = gender_stats[['Total Sales', 'Sales %']]
    sales_summary.columns = ['Total Sales', 'Percentage']
    
    print_formatted_dataframe(sales_summary, {
        'Total Sales': lambda x: f"${x:,.2f}",
        'Percentage': lambda x: f"{x:.2f}%"
    })
    print(f"\nGrand Total: ${total_revenue:,.2f}")
    
    # Task 4: Find most used payment method
    print_section_header("Payment Method Usage")
    
    payment_counts = df_csv['payment_method'].value_counts()
    payment_summary = create_count_summary(payment_counts, total_rows)
    
    print_formatted_dataframe(payment_summary, {
        'Count': lambda x: f"{x:,}",
        'Percentage': lambda x: f"{x:.2f}%"
    })
    print(f"\nMost used payment method: {payment_counts.idxmax()} ({payment_counts.max():,} transactions)")
    
    # Task 5: Find day with the most sales
    print_section_header("Day with Most Sales")
    
    sales_by_date = df_csv.groupby('invoice_date', sort=False)['sales'].sum()
    top_days = sales_by_date.nlargest(7)
    
    print("\nTop 7 days by sales:")
    for i, (date, sales) in enumerate(top_days.items(), 1):
        print(f"{i:2d}. {date}: ${sales:,.2f}")
    
    day_with_most_sales = top_days.idxmax()
    max_sales = top_days.max()
    print(f"\nDay with most sales: {day_with_most_sales} (${max_sales:,.2f})")
    
    print_section_header("Additional Statistics")
    
    stats = df_csv[['sales', 'quantity', 'price', 'customer_id']].agg({
        'sales': 'mean',
        'quantity': 'mean',
        'price': 'mean',
        'customer_id': 'nunique'
    })
    
    print(f"Total transactions: {total_rows:,}")
    print(f"Total revenue: ${total_revenue:,.2f}")
    print(f"Average transaction value: ${stats['sales']:,.2f}")
    print(f"Number of unique customers: {stats['customer_id']:,}")
    print(f"Average items per transaction: {stats['quantity']:.2f}")
    print(f"Average price per item: ${stats['price']:,.2f}")
    
    return df_csv

if __name__ == "__main__":
    df_csv = analyze_shopping_data('customer_shopping_data.csv')
    
    print("\n" + "=" * 50)