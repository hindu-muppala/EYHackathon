import pandas as pd

# Load datasets
credit_loan_df = pd.read_csv("data/credit_loan_dataset.csv")
financial_data_df = pd.read_csv("data/financial_data.csv")

# Perform data cleaning steps (e.g., drop columns, handle missing values)
credit_loan_df = credit_loan_df.drop(columns=['column_name_to_remove'])
financial_data_df = financial_data_df.drop(columns=['column_name_to_remove'])

# Handle missing values (example: fill with mean)
credit_loan_df['column_name'] = credit_loan_df['column_name'].fillna(credit_loan_df['column_name'].mean())
financial_data_df['column_name'] = financial_data_df['column_name'].fillna(financial_data_df['column_name'].mean())

# Convert data types (e.g., to numeric)
credit_loan_df['amount_column'] = pd.to_numeric(credit_loan_df['amount_column'], errors='coerce')
financial_data_df['income_column'] = pd.to_numeric(financial_data_df['income_column'], errors='coerce')

# Drop duplicates
credit_loan_df = credit_loan_df.drop_duplicates()
financial_data_df = financial_data_df.drop_duplicates()

# Save cleaned datasets
credit_loan_df.to_csv("data/cleaned_credit_loan_dataset.csv", index=False)
financial_data_df.to_csv("data/cleaned_financial_data.csv", index=False)

print("Data cleaning complete and files saved.")
