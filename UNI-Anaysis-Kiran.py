#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 20:03:56 2024

@author: Kiran
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load your datasets
try:
    # Replace with actual paths if necessary
    orders_df = pd.read_csv('updated_cleaned_orders_final.csv')
    customers_df = pd.read_csv('customer_summary_aov_clv.csv')
except FileNotFoundError:
    print("Please ensure the dataset files are in the correct directory.")
    exit()

# Analyze and plot Total Spent (Light Users and Heavy Users)
orders_df_sorted = orders_df.sort_values(by='Total', ascending=True)
light_users = orders_df_sorted.head(500)  # Bottom 500 spenders
heavy_users = orders_df_sorted.iloc[500:]  # Remaining users

# Plot: Light Users Distribution
plt.figure(figsize=(10, 6))
counts, bins, patches = plt.hist(light_users['Total'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Total Spent (Light Users)')
plt.xlabel('Total Spent')
plt.ylabel('Frequency')
for count, x in zip(counts, bins[:-1]):  # Label bars
    if count > 0:
        plt.text(x + (bins[1] - bins[0]) / 2, count, str(int(count)), ha='center', va='bottom')
light_stats = light_users['Total'].describe()
plt.text(0.95, 0.95, f"Mean: {light_stats['mean']:.2f}\nMedian: {light_stats['50%']:.2f}\n"
                     f"Min: {light_stats['min']}\nMax: {light_stats['max']}\nN: {light_stats['count']}",
         transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')
plt.show()

# Plot: Heavy Users Distribution
plt.figure(figsize=(10, 6))
counts, bins, patches = plt.hist(heavy_users['Total'], bins=30, color='orange', edgecolor='black')
plt.title('Distribution of Total Spent (Heavy Users)')
plt.xlabel('Total Spent')
plt.ylabel('Frequency')
for count, x in zip(counts, bins[:-1]):  # Label bars
    if count > 0:
        plt.text(x + (bins[1] - bins[0]) / 2, count, str(int(count)), ha='center', va='bottom')
heavy_stats = heavy_users['Total'].describe()
plt.text(0.95, 0.95, f"Mean: {heavy_stats['mean']:.2f}\nMedian: {heavy_stats['50%']:.2f}\n"
                     f"Min: {heavy_stats['min']}\nMax: {heavy_stats['max']}\nN: {heavy_stats['count']}",
         transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')
plt.show()

# Analyze and plot Average Order Value
plt.figure(figsize=(10, 6))
counts, bins, patches = plt.hist(customers_df['Average_Order_Value'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Average Order Value')
plt.xlabel('Average Order Value')
plt.ylabel('Frequency')
aov_stats = customers_df['Average_Order_Value'].describe()
plt.text(0.95, 0.95, f"Mean: {aov_stats['mean']:.2f}\nMedian: {aov_stats['50%']:.2f}\n"
                     f"Min: {aov_stats['min']:.2f}\nMax: {aov_stats['max']:.2f}\nN: {aov_stats['count']}",
         transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')
plt.show()

# Top 10 Products Sold (Excluding Free/Giveaway Items)
filtered_orders = orders_df[~orders_df['Lineitem name'].str.contains("event|100% off|UNKNOWN", case=False, na=False)]
top_products = filtered_orders['Lineitem name'].value_counts().head(10)

plt.figure(figsize=(12, 6))
top_products.plot(kind='bar', color='skyblue')
plt.title('Top 10 Products Sold (Excluding Free/Giveaway Items)')
plt.xlabel('Product Name')
plt.ylabel('Number of Items Sold')
for index, value in enumerate(top_products):
    plt.text(index, value + 1, str(value), ha='center')
plt.xticks(rotation=45, ha='right')
plt.show()

# Shipping Method Analysis
express_keywords = ['Express', 'Priority', 'Fedex Ficp', 'Fedex IP']
orders_df['Shipping Category'] = orders_df['Shipping Method'].apply(
    lambda x: 'Express' if any(keyword.lower() in x.lower() for keyword in express_keywords) else 'Standard'
)
shipping_counts = orders_df['Shipping Method'].value_counts()
colors = ['orange' if orders_df[orders_df['Shipping Method'] == method]['Shipping Category'].iloc[0] == 'Express' else 'skyblue'
          for method in shipping_counts.index]

plt.figure(figsize=(12, 8))
bars = plt.bar(shipping_counts.index, shipping_counts.values, color=colors, edgecolor='black')
plt.title('Shipping Methods with Express and Standard Colors')
plt.xlabel('Shipping Method')
plt.ylabel('Frequency')
for bar, count in zip(bars, shipping_counts):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, str(count), ha='center', va='bottom')
express_patch = mpatches.Patch(color='orange', label='Express Shipping')
standard_patch = mpatches.Patch(color='skyblue', label='Standard Shipping')
plt.legend(handles=[express_patch, standard_patch], loc='upper right')
plt.xticks(rotation=45, ha='right')
plt.show()
