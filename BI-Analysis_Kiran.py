#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 03:04:23 2024

@author: Kiran
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
customer_df = pd.read_csv('matched_dataset.csv')

# Sort customers by Customer Lifetime Value (CLV) in ascending order
customer_df = customer_df.sort_values(by='Customer_Lifetime_Value', ascending=True)

# Step 1: Label the bottom 500 customers as 'Light' users and the rest as 'Heavy' users
customer_df['User_Type'] = ['Light' if i < 500 else 'Heavy' for i in range(len(customer_df))]

# Step 2: Separate light and heavy users for further analysis
light_users = customer_df[customer_df['User_Type'] == 'Light']
heavy_users = customer_df[customer_df['User_Type'] == 'Heavy']

# Step 3: Plot histograms for Light Users and Heavy Users
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Light Users (Bottom 500 CLV)
light_counts, light_bins, _ = ax[0].hist(light_users['Customer_Lifetime_Value'], bins=20, color='skyblue', edgecolor='black')
ax[0].set_title('Customer Lifetime Value - Light Users (Bottom 500)')
ax[0].set_xlabel('Customer Lifetime Value')
ax[0].set_ylabel('Frequency')

# Adding descriptive statistics for Light Users
light_stats = light_users['Customer_Lifetime_Value'].describe()
ax[0].text(0.95, 0.95, f"Mean: {light_stats['mean']:.2f}\nMedian: {light_stats['50%']:.2f}\n"
           f"Min: {light_stats['min']}\nMax: {light_stats['max']}\nN: {int(light_stats['count'])}",
           transform=ax[0].transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')

# Labeling the count above each bar for Light Users
for count, x in zip(light_counts, light_bins):
    if count > 0:
        ax[0].text(x + (light_bins[1] - light_bins[0]) / 2, count, str(int(count)), ha='center', va='bottom')

# Adding descriptive statistics for Heavy Users
heavy_stats = heavy_users['Customer_Lifetime_Value'].describe()
ax[1].text(0.95, 0.95, f"Mean: {heavy_stats['mean']:.2f}\nMedian: {heavy_stats['50%']:.2f}\n"
           f"Min: {heavy_stats['min']}\nMax: {heavy_stats['max']}\nN: {int(heavy_stats['count'])}",
           transform=ax[1].transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right')

plt.tight_layout()
plt.show()

####################################################################################

# Comparison of CLV and Number of Orders for Light and Heavy Users
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# CLV and Number of Orders for Light Users
axes[0].bar(x=['Customer Lifetime Value', 'Number of Orders'], 
            height=[light_users['Customer_Lifetime_Value'].sum(), light_users['Number_of_Orders'].sum()],
            color=['skyblue', 'lightgreen'])
axes[0].set_title('Light Users')
axes[0].set_ylabel('Sum of Values')
for i, v in enumerate([light_users['Customer_Lifetime_Value'].sum(), light_users['Number_of_Orders'].sum()]):
    axes[0].text(i, v + 100, f"{v:.0f}", ha='center')

# CLV and Number of Orders for Heavy Users
axes[1].bar(x=['Customer Lifetime Value', 'Number of Orders'], 
            height=[heavy_users['Customer_Lifetime_Value'].sum(), heavy_users['Number_of_Orders'].sum()],
            color=['orange', 'salmon'])
axes[1].set_title('Heavy Users')
for i, v in enumerate([heavy_users['Customer_Lifetime_Value'].sum(), heavy_users['Number_of_Orders'].sum()]):
    axes[1].text(i, v + 100, f"{v:.0f}", ha='center')

plt.suptitle('CLV and Number of Orders Comparison for Light and Heavy Users')
plt.tight_layout()
plt.show()

###################################################################################

# Scatter Plot: AOV vs Total Revenue
orders_df = pd.read_csv('updated_cleaned_orders_final.csv')
merged_df = pd.merge(customer_df, orders_df[['Email', 'Total']], on='Email', how='inner')

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Average_Order_Value', y='Total', data=merged_df)
plt.title('Scatter Plot of Average Order Value vs Revenue (Total)')
plt.xlabel('Average Order Value (AOV)')
plt.ylabel('Revenue (Total)')
plt.show()

correlation, p_value = pearsonr(merged_df['Average_Order_Value'], merged_df['Total'])
print(f"Correlation between AOV and Revenue: {correlation:.2f}")
print(f"P-value: {p_value:.5f}")
