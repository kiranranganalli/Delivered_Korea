import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Load the matched dataset
matched_dataset = pd.read_csv('matched_dataset.csv')

# Filter dataset based on the condition: Total Spent >= 222
filtered_dataset = matched_dataset[matched_dataset['Total Spent'] >= 222]

# Ensure Email_Marketing_Binary is binary (0 or 1)
filtered_dataset.loc[:, 'Email_Marketing_Binary'] = filtered_dataset['Email_Marketing_Binary'].astype(int)

# Add a binary feature for whether a discount was used
filtered_dataset['Used_Discount'] = (filtered_dataset['Discount Amount'] > 0).astype(int)

# Generate dummy variables for all categories in Vendor, Shipping Method, and Shipping Province Name
dummy_variables = pd.get_dummies(
    filtered_dataset[['Vendor', 'Shipping Method', 'Shipping Province Name']],
    drop_first=True
)

# Combine dummy variables with Email_Marketing_Binary, Used_Discount, and the target variable
X = pd.concat([
    filtered_dataset[['Email_Marketing_Binary', 'Used_Discount']],
    dummy_variables
], axis=1)

# Add an interaction term for Email_Marketing_Binary × Used_Discount
X['Email_Marketing_Discount'] = X['Email_Marketing_Binary'] * X['Used_Discount']

# Apply log transformation to the target variable (Total Spent)
Y = np.log1p(filtered_dataset['Total Spent'])  # log(1 + Total Spent) to handle zero values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize the Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Fit the model to the training data
rf_model.fit(X_train_scaled, y_train)

# Make predictions on the test data
y_pred = rf_model.predict(X_test_scaled)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Random Forest Model Performance:")
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Feature Importances
feature_importances = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("Feature Importances:")
print(feature_importances.head(10))

# Display top 10 features for each main variable group
categories = ['Vendor', 'Shipping Method', 'Shipping Province Name']
for category in categories:
    category_features = feature_importances[feature_importances['Feature'].str.contains(category)].head(10)
    print(f"Top 10 Features for {category}:")
    print(category_features)

# Save full feature importances to a CSV for reporting
feature_importances.to_csv('random_forest_feature_importances.csv', index=False)

# Save feature importances to a CSV for reporting
feature_importances.to_csv('random_forest_feature_importances.csv', index=False)
