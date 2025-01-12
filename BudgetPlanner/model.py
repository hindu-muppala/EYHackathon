import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error

# Load and preprocess the data
data = pd.read_csv('data/financial_data.csv')

# Define feature and target columns
features = [
    "annual_income", "age", "Dependents", "Occupation", "city", "Rent", "Loan_Repayment", 
    "Insurance", "Groceries", "Transport", "Eating_Out", "Entertainment", "Utilities", 
    "Healthcare", "Education", "Miscellaneous", "Desired_Savings_Percentage"
]

targets = [
    "Desired_Savings", "Disposable_Income", "Potential_Savings_Groceries", "Potential_Savings_Transport", 
    "Potential_Savings_Eating_Out", "Potential_Savings_Entertainment", "Potential_Savings_Utilities", 
    "Potential_Savings_Healthcare", "Potential_Savings_Education", "Potential_Savings_Miscellaneous"
]

# Encode categorical variables
label_encoders = {}
for col in ['Occupation', 'city']:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Split data into features (X) and targets (y)
X = data[features]
y = data[targets]

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
multi_output_model = MultiOutputRegressor(rf_model)

# Train the model
print("Training the Random Forest model with MultiOutputRegressor...")
multi_output_model.fit(X_train_scaled, y_train)

# Evaluate the model
y_pred = multi_output_model.predict(X_test_scaled)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred, multioutput='uniform_average')
print(f"Mean Squared Error: {mse:.4f}")

# Feature importance analysis
importances = rf_model.feature_importances_
feature_importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("Feature Importances:")
print(feature_importance_df)

# Save the model and scalers
import joblib
joblib.dump(multi_output_model, 'multi_output_rf_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')
print("Model, scaler, and encoders saved successfully.")
