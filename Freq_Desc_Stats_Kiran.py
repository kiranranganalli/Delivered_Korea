#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 13:25:20 2024

@author: Kiran
"""

import pandas as pd
import numpy as np

# Load the aggregated dataset
try:
    aggregated_output_path = 'merged_customers_orders_dataset.csv'
    aggregated_df = pd.read_csv(aggregated_output_path)
except FileNotFoundError:
    print("Error: File not found. Ensure 'merged_customers_orders_dataset.csv' is in the correct directory.")
    exit()

# Prepare the Y variable (target)
y = pd.to_numeric(aggregated_df['Total Spent'], errors='coerce').fillna(0)

# Prepare the X variables (features)
x_columns = [
    'Email_Marketing_Binary',
    'SMS_Marketing_Binary',
    'Default Address Country Code',
    'Shipping Method',
    'Vendor',
    'Discount Code',
    'Shipping Province Name'
]

# Extract relevant columns for X variables
x_combined = aggregated_df[x_columns].copy()

# Convert 'Discount Code' to binary (1 if a code is used, 0 otherwise)
x_combined['Discount Code'] = np.where(x_combined['Discount Code'].notna(), 1, 0)

# For categorical variables, retain only top 10 values based on 'Total Spent'
categorical_columns = ['Default Address Country Code', 'Shipping Method', 'Vendor', 'Shipping Province Name']
for col in categorical_columns:
    top_10_values = aggregated_df.groupby(col)['Total Spent'].sum().nlargest(10).index
    x_combined[col] = np.where(x_combined[col].isin(top_10_values), x_combined[col], 'Other')

# Calculate and print descriptive statistics for the Y variable
print("Descriptive Statistics for Y Variable (Total Spent):")
print(y.describe())

# Calculate and print descriptive statistics for X variables
print("\nDescriptive Statistics for X Variables:")
for col in x_combined.columns:
    print(f"\nDescriptive Statistics for {col}:")
    if x_combined[col].dtype == 'object':
        # Print value counts for categorical variables
        print(x_combined[col].value_counts())
    else:
        # Print summary stats for numeric variables
        print(x_combined[col].describe())

# Calculate and print frequencies for the Y variable
print("\nFrequencies for Y Variable (Total Spent):")
print(y.value_counts(bins=10))

# Calculate and print frequencies for each X variable
print("\nFrequencies for X Variables:")
for col in x_combined.columns:
    print(f"\nFrequencies for {col}:")
    print(x_combined[col].value_counts())
    
    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 13:25:20 2024

@author: Kiran
"""

import pandas as pd
import sys

# Load the matched dataset
try:
    matched_dataset = pd.read_csv('matched_dataset.csv')
except FileNotFoundError:
    print("Error: 'matched_dataset.csv' not found. Please ensure the file is in the working directory.")
    sys.exit()  # Exit the program if the file is not found

# Filter dataset based on the condition: Total Spent >= 100
filtered_dataset = matched_dataset[matched_dataset['Total Spent'] >= 100].copy()

# Ensure 'Vendor' and 'Shipping Province Name' columns exist
if 'Vendor' not in filtered_dataset.columns or 'Shipping Province Name' not in filtered_dataset.columns:
    print("Error: Required columns ('Vendor', 'Shipping Province Name') are missing from the dataset.")
    sys.exit()

# Frequency table for 'Vendor'
print("\nFrequency Table for Vendor:")
vendor_freq = filtered_dataset['Vendor'].value_counts()
print(vendor_freq)

# Save Vendor frequency to a CSV for review
vendor_freq.to_csv('vendor_frequency.csv', header=['Frequency'])

# Frequency table for 'Shipping Province Name'
print("\nFrequency Table for Shipping Province Name:")
province_freq = filtered_dataset['Shipping Province Name'].value_counts()
print(province_freq)

# Save Shipping Province Name frequency to a CSV for review
province_freq.to_csv('shipping_province_frequency.csv', header=['Frequency'])

print("\nFrequency tables saved to 'vendor_frequency.csv' and 'shipping_province_frequency.csv'.")


###########Graph Plot##############Vendor


import pandas as pd
import matplotlib.pyplot as plt

# Load the matched dataset
matched_dataset = pd.read_csv('matched_dataset.csv')

# Count the frequency of each vendor
vendor_counts = matched_dataset['Vendor'].value_counts().head(10)  # Top 10 vendors

# Create a DataFrame for the top 10 vendors
vendor_freq = vendor_counts.reset_index()
vendor_freq.columns = ['Vendor', 'Frequency']

# Calculate descriptive statistics
mean_freq = vendor_freq['Frequency'].mean()
median_freq = vendor_freq['Frequency'].median()
min_freq = vendor_freq['Frequency'].min()
max_freq = vendor_freq['Frequency'].max()
count_freq = vendor_freq['Frequency'].sum()

# Plotting the bar chart for vendor frequencies
plt.figure(figsize=(12, 6))
bars = plt.bar(vendor_freq['Vendor'], vendor_freq['Frequency'], color='skyblue', edgecolor='black')

# Adding annotations for each bar
for bar, freq in zip(bars, vendor_freq['Frequency']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10, str(freq), ha='center', fontsize=9)

# Adding descriptive statistics as text in the top-right corner
descriptive_stats = (
    f"Mean: {mean_freq:.2f}\n"
    f"Median: {median_freq:.2f}\n"
    f"Min: {min_freq}\n"
    f"Max: {max_freq}\n"
    f"Total: {count_freq}"
)

plt.text(
    len(vendor_freq) - 2.5, 0.9 * max_freq,  # Position the text at the top-right
    descriptive_stats,
    fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
)

# Adding titles and labels
plt.title('Frequency Distribution of Top 10 Vendors', fontsize=14)
plt.xlabel('Vendors', fontsize=12)
plt.ylabel('Frequency', fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()



#Graph Regions#################

import pandas as pd
import matplotlib.pyplot as plt

# Load the matched dataset
matched_dataset = pd.read_csv('matched_dataset.csv')

# Count the frequency of each shipping province name
province_counts = matched_dataset['Shipping Province Name'].value_counts().head(10)  # Top 10 provinces

# Create a DataFrame for the top 10 provinces
province_freq = province_counts.reset_index()
province_freq.columns = ['Shipping Province Name', 'Frequency']

# Calculate descriptive statistics
mean_freq = province_freq['Frequency'].mean()
median_freq = province_freq['Frequency'].median()
min_freq = province_freq['Frequency'].min()
max_freq = province_freq['Frequency'].max()
count_freq = province_freq['Frequency'].sum()

# Plotting the bar chart for shipping province frequencies
plt.figure(figsize=(12, 6))
bars = plt.bar(province_freq['Shipping Province Name'], province_freq['Frequency'], color='skyblue', edgecolor='black')

# Adding annotations for each bar
for bar, freq in zip(bars, province_freq['Frequency']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10, str(freq), ha='center', fontsize=9)

# Adding descriptive statistics as text in the top-right corner
descriptive_stats = (
    f"Mean: {mean_freq:.2f}\n"
    f"Median: {median_freq:.2f}\n"
    f"Min: {min_freq}\n"
    f"Max: {max_freq}\n"
    f"Total: {count_freq}"
)

plt.text(
    len(province_freq) - 2.5, 0.9 * max_freq,  # Position the text at the top-right
    descriptive_stats,
    fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
)

# Adding titles and labels
plt.title('Frequency Distribution of Top 10 Shipping Provinces', fontsize=14)
plt.xlabel('Shipping Provinces', fontsize=12)
plt.ylabel('Frequency', fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()

