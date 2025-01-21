#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 13:25:20 2024

@author: Kiran
"""

import pandas as pd
import statsmodels.api as sm
import numpy as np

# Load the matched dataset
try:
    matched_dataset = pd.read_csv('matched_dataset.csv')
except FileNotFoundError:
    print("Error: 'matched_dataset.csv' not found. Please ensure the file is in the working directory.")
    exit()

# Filter dataset based on the condition: Total Spent >= 222
filtered_dataset = matched_dataset[matched_dataset['Total Spent'] >= 100].copy()

# Ensure Email_Marketing_Binary is binary (0 or 1)
filtered_dataset['Email_Marketing_Binary'] = filtered_dataset['Email_Marketing_Binary'].astype(int)

# Add a binary feature for whether a discount was used
filtered_dataset['Used_Discount'] = (filtered_dataset['Discount Amount'] > 0).astype(int)

# Generate dummy variables for categorical columns
categorical_columns = ['Vendor', 'Shipping Method', 'Shipping Province Name']
dummy_variables = pd.get_dummies(filtered_dataset[categorical_columns], drop_first=True)

# Combine dummy variables with other features
X = pd.concat([
    filtered_dataset[['Email_Marketing_Binary', 'Used_Discount']],
    dummy_variables
], axis=1)

# Add an interaction term for Email_Marketing_Binary × Used_Discount
X['Email_Marketing_Discount'] = X['Email_Marketing_Binary'] * X['Used_Discount']

# Apply log transformation to the target variable (Total Spent)
filtered_dataset['Log_Total Spent'] = np.log1p(filtered_dataset['Total Spent'])

# Define the target variable (Y)
Y = filtered_dataset['Log_Total Spent']

# Add a constant to X for the OLS model
X = sm.add_constant(X)

# Ensure all X columns are numeric
X = X.astype(float)

# Drop any rows with missing values in X or Y
if X.isnull().any().any() or Y.isnull().any():
    print("Missing values detected. Dropping rows with missing data.")
    valid_indices = X.dropna().index
    X = X.loc[valid_indices]
    Y = Y.loc[valid_indices]

# Iteratively remove variables with p >= 0.1
ols_model = sm.OLS(Y, X).fit()
while True:
    # Get p-values excluding the constant
    p_values = ols_model.pvalues.drop('const', errors='ignore')

    # Find the maximum p-value
    max_pval = p_values.max()

    if max_pval >= 0.1:
        # Get the variable with the max p-value
        worst_var = p_values.idxmax()
        print(f"Removing variable: {worst_var} with p-value: {max_pval}")

        # Drop the variable from X
        X = X.drop(columns=[worst_var])

        # Rebuild the model
        ols_model = sm.OLS(Y, X).fit()
    else:
        break

# Check data types of the final model variables
print("Data types of variables used in the model:")
print(pd.DataFrame({'Variable': X.columns, 'Data Type': X.dtypes}).set_index('Variable'))

# Display the final OLS model summary
print("\nFinal OLS Model Summary:")
print(ols_model.summary())

# Residual Diagnostics
print("\nPerforming Residual Diagnostics...")
residuals = ols_model.resid

# Residuals vs Fitted Values Plot
import matplotlib.pyplot as plt
plt.scatter(ols_model.fittedvalues, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.title("Residuals vs Fitted Values")
plt.show()

# Histogram of Residuals
plt.hist(residuals, bins=30, edgecolor='black')
plt.xlabel("Residuals")
plt.ylabel("Frequency")
plt.title("Histogram of Residuals")
plt.show()

# Variance Inflation Factor (VIF) for Multicollinearity Check
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data['Variable'] = X.columns
vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print("\nVariance Inflation Factors:")
print(vif_data)


# Find baseline category for Vendor and Shipping Province Name
baseline_vendor = matched_dataset['Vendor'].value_counts().idxmin()
baseline_shipping_region = matched_dataset['Shipping Province Name'].value_counts().idxmin()

print(f"Baseline Vendor: {baseline_vendor}")
print(f"Baseline Shipping Region: {baseline_shipping_region}")

# Calculate bottom 5 categories by average Total Spent for Vendor
vendor_means = matched_dataset.groupby('Vendor')['Total Spent'].mean().sort_values()
bottom_5_vendors = vendor_means.head(5)
print("\nBottom 5 Vendors by Average Total Spent:")
print(bottom_5_vendors)

# Calculate bottom 5 categories by average Total Spent for Shipping Province Name
shipping_region_means = matched_dataset.groupby('Shipping Province Name')['Total Spent'].mean().sort_values()
bottom_5_shipping_regions = shipping_region_means.head(5)
print("\nBottom 5 Shipping Regions by Average Total Spent:")
print(bottom_5_shipping_regions)

# If you prefer total spending instead of average:
# vendor_totals = filtered_dataset.groupby('Vendor')['Total Spent'].sum().sort_values()
# shipping_region_totals = filtered_dataset.groupby('Shipping Province Name')['Total Spent'].sum().sort_values()
