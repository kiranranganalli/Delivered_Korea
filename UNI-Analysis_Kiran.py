#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 23:00:09 2024
@author: Kiran
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry

# Load the datasets
df_orders = pd.read_csv('updated_cleaned_orders_final.csv')
df_customers = pd.read_csv('customer_summary_aov_clv.csv')

# Function to get full country names from country codes
def get_country_name(country_code):
    try:
        return pycountry.countries.get(alpha_2=country_code).name
    except:
        return country_code  # Return code if not found


# Descriptive Analysis: Distribution of Total Spent
def plot_total_spent_distribution():
    """Plot the distribution of Total Spent with descriptive statistics."""
    total_spent_stats = df_orders['Total'].describe()
    plt.figure(figsize=(12, 6))
    counts, bins, patches = plt.hist(df_orders['Total'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Total Spent')
    plt.xlabel('Total Spent')
    plt.ylabel('Frequency')
    
    # Add count labels
    for count, x in zip(counts, bins):
        if count > 0:
            plt.text(x + (bins[1] - bins[0]) / 2, count, str(int(count)), ha='center', va='bottom')

    # Add descriptive statistics
    plt.text(
        0.95, 0.95,
        f"Mean: {total_spent_stats['mean']:.2f}\nMedian: {total_spent_stats['50%']:.2f}\n"
        f"Min: {total_spent_stats['min']}\nMax: {total_spent_stats['max']}\nN: {int(total_spent_stats['count'])}",
        transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right'
    )
    plt.show()


# Descriptive Analysis: Distribution of Average Order Value (AOV)
def plot_aov_distribution():
    """Plot the distribution of Average Order Value (AOV) with descriptive statistics."""
    aov_stats = df_customers['Average_Order_Value'].describe()
    plt.figure(figsize=(10, 6))
    hist = sns.histplot(df_customers['Average_Order_Value'], bins=30, kde=True, color='blue')
    plt.title('Distribution of Average Order Value')
    plt.xlabel('Average Order Value')
    plt.ylabel('Frequency')

    # Add count labels
    for patch in hist.patches:
        height = patch.get_height()
        if height > 0:
            plt.text(patch.get_x() + patch.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')

    # Add descriptive statistics
    plt.text(
        0.95, 0.95,
        f"Mean: {aov_stats['mean']:.2f}\nMedian: {aov_stats['50%']:.2f}\n"
        f"Min: {aov_stats['min']}\nMax: {aov_stats['max']}\nN: {int(aov_stats['count'])}",
        transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right'
    )
    plt.show()


# AOV Range Categorization
def plot_aov_ranges():
    """Categorize AOV into ranges and plot the number of users in each range."""
    ranges = [0, 200, 400, 600, 800, 1000, 1200]
    labels = ['0-200', '200-400', '400-600', '600-800', '800-1000', '1000-1200']
    df_customers['AOV_Range'] = pd.cut(df_customers['Average_Order_Value'], bins=ranges, labels=labels)
    aov_counts = df_customers['AOV_Range'].value_counts().sort_index()

    # Plotting
    plt.figure(figsize=(10, 6))
    aov_counts.plot(kind='bar', color='skyblue')
    plt.title('Number of Users in Each AOV Range')
    plt.xlabel('AOV Range')
    plt.ylabel('Number of Users')

    # Add count labels
    for index, value in enumerate(aov_counts):
        plt.text(index, value + 5, str(value), ha='center')
    plt.show()


# Shipping Analysis: Most Used Shipping Method
def plot_shipping_methods():
    """Analyze the most used shipping methods."""
    shipping_counts = df_orders['Shipping Method'].value_counts()
    plt.figure(figsize=(10, 6))
    shipping_counts.plot(kind='bar', color='skyblue')
    plt.title('Most Used Shipping Methods')
    plt.xlabel('Shipping Method')
    plt.ylabel('Number of Users')

    # Add count labels
    for index, value in enumerate(shipping_counts):
        plt.text(index, value + 5, str(value), ha='center')
    plt.show()


# Sales Analysis: Top 10 Items Sold
def plot_top_items_sold():
    """Plot the top 10 items sold."""
    top_items_sold = df_orders[df_orders['Lineitem name'] != 'UNKNOWN']['Lineitem name'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    top_items_sold.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Items Sold')
    plt.xlabel('Item Name')
    plt.ylabel('Number of Items Sold')

    # Add count labels
    for index, value in enumerate(top_items_sold):
        plt.text(index, value + 5, str(value), ha='center')
    plt.show()


# Regional Analysis: Top 10 Countries and States by Sales
def plot_sales_by_region():
    """Analyze top 10 countries and states generating the most sales."""
    df_orders['Shipping Province Name'] = df_orders['Shipping Country'].apply(get_country_name)
    df_orders['State_Country'] = df_orders['Shipping Province'] + ', ' + df_orders['Shipping Province Name']

    # Top states
    top_states = df_orders['State_Country'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    top_states.plot(kind='bar', color='lightblue')
    plt.title('Top 10 States/Provinces by Sales with Country Names')
    plt.xlabel('State, Country')
    plt.ylabel('Number of Sales')
    for index, value in enumerate(top_states):
        plt.text(index, value + 5, str(value), ha='center')
    plt.xticks(rotation=45, ha='right')
    plt.show()

    # Top countries
    top_countries = df_orders['Shipping Province Name'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    top_countries.plot(kind='bar', color='coral')
    plt.title('Top 10 Countries by Sales')
    plt.xlabel('Country')
    plt.ylabel('Number of Sales')
    for index, value in enumerate(top_countries):
        plt.text(index, value + 5, str(value), ha='center')
    plt.xticks(rotation=45, ha='right')
    plt.show()


# Customer Analysis: Top 25 Customers with Multiple Orders
def plot_top_customers():
    """Plot top 25 customers with multiple orders."""
    top_customers = df_orders['Email'].value_counts().head(25)
    plt.figure(figsize=(12, 6))
    top_customers.plot(kind='bar', color='skyblue')
    plt.title('Top 25 Customers with Multiple Orders')
    plt.xlabel('Customer')
    plt.ylabel('Number of Orders')
    for index, value in enumerate(top_customers):
        plt.text(index, value + 1, str(value), ha='center')
    plt.xticks(rotation=45, ha='right')
    plt.show()


# Run desired functions
plot_total_spent_distribution()
plot_aov_distribution()
plot_aov_ranges()
plot_shipping_methods()
plot_top_items_sold()
plot_sales_by_region()
plot_top_customers()
