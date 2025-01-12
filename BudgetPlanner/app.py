import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load pre-trained model and pre-processing objects
model = joblib.load("savings_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Define features (the same as in the model training)
features = [
    "annual_income", "age", "Dependents", "Occupation", "city", "Rent", "Loan_Repayment", 
    "Insurance", "Groceries", "Transport", "Eating_Out", "Entertainment", "Utilities", 
    "Healthcare", "Education", "Miscellaneous", "Desired_Savings_Percentage"
]

# Define target columns (what we want to predict)
targets = [
    "Desired_Savings", "Disposable_Income", "Potential_Savings_Groceries", "Potential_Savings_Transport", 
    "Potential_Savings_Eating_Out", "Potential_Savings_Entertainment", "Potential_Savings_Utilities", 
    "Potential_Savings_Healthcare", "Potential_Savings_Education", "Potential_Savings_Miscellaneous"
]

# Function to preprocess input data
def preprocess_input(data):
    # Encode categorical features
    for col in ["Occupation", "city"]:
        if col in data:
            data[col] = label_encoders[col].transform([data[col]])[0]
    
    # Create DataFrame and scale numeric data
    input_df = pd.DataFrame([data], columns=features)
    input_scaled = scaler.transform(input_df)
    return input_scaled

# Loan Eligibility Function
def check_loan_eligibility(annual_income, monthly_expenses, desired_savings_percentage):
    # Loan eligibility based on income, expenses, and desired savings
    # A simple rule-based approach for demonstration: 
    disposable_income = annual_income - monthly_expenses * 12  # Annual disposable income
    required_savings = annual_income * (desired_savings_percentage / 100)
    
    # Check if disposable income is enough to cover savings and monthly expenses
    if disposable_income > required_savings + (monthly_expenses * 12):
        return "Loan Approved"
    else:
        return "Loan Denied"

# Portfolio Manager Function
def portfolio_manager():
    st.subheader("Investment Portfolio Creation")
    st.write("""
        **Investment Terms Explanation:**
        - **Mutual Funds:** A pool of money collected from many investors to invest in stocks, bonds, or other securities.
        - **SIP (Systematic Investment Plan):** A method of investing in mutual funds, where you contribute a fixed amount periodically.
        - **Equity Funds:** Invest in stocks, offering high returns but with more risk.
        - **Debt Funds:** Invest in bonds, offering lower returns but lower risk.
        - **Balanced Funds:** A mix of equity and debt funds, balancing risk and return.
        - **Stocks:** Ownership shares in companies, offering the potential for high returns but higher risk.
    """)

    # Get user investment preferences
    risk_tolerance = st.radio("Select Your Risk Tolerance", options=["Low", "Medium", "High"])
    investment_goals = st.text_input("What are your investment goals?", "e.g., retirement, education, buying a home")

    # Based on input, create a simple portfolio suggestion
    st.subheader("Your Personalized Investment Portfolio")

    if risk_tolerance == "Low":
        st.write(f"- **Investment Type:** Debt Funds, Balanced Funds")
        st.write(f"- **Suggested Contribution:** ₹10,000/month SIP")

    elif risk_tolerance == "Medium":
        st.write(f"- **Investment Type:** Balanced Funds, Equity Funds")
        st.write(f"- **Suggested Contribution:** ₹15,000/month SIP")

    elif risk_tolerance == "High":
        st.write(f"- **Investment Type:** Equity Funds, Stocks")
        st.write(f"- **Suggested Contribution:** ₹20,000/month SIP")

    st.write(f"**Investment Goal:** {investment_goals}")

# Main function for the app
def main():
    st.title("AI Budget Planner")

    # Landing page
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    
    if st.session_state.page == "landing":
        st.subheader("Click Below to Access the AI Budget Planner")
        if st.button("Click Here for AI Budget Planner"):
            st.session_state.page = "intro"
    
    elif st.session_state.page == "intro":
        st.header("What is the AI Budget Planner?")
        st.write("""
            The AI Budget Planner is an intelligent tool designed to help you plan your finances more effectively.
            By analyzing your income, expenses, and financial goals, the AI will suggest the best savings strategies
            and budget allocation for different categories in your life.
            
            **Key Features:**
            - Calculate potential savings in categories like Groceries, Transport, Entertainment, and more.
            - Get personalized suggestions on how to reduce your spending and maximize savings.
            - See a breakdown of your income, expenses, and possible savings based on the data you provide.
            
            **How It Works:**
            - Input your income, age, expenses, and desired savings percentage.
            - The AI model processes this data and suggests the optimal budget plan.
            
            Ready to get started? Click below to proceed with the Budget Planner!
        """)
        
        if st.button("Proceed to Budget Planner"):
            st.session_state.page = "budget_planner"
    
    elif st.session_state.page == "budget_planner":
        st.header("Enter your financial details (in INR)")
        
        # Collect user inputs
        annual_income = st.number_input("Annual Income (in INR):", min_value=0, step=1000)
        age = st.number_input("Age:", min_value=0, max_value=100, step=1)
        dependents = st.number_input("Number of Dependents:", min_value=0, step=1)
        occupation = st.selectbox("Occupation:", label_encoders["Occupation"].classes_)
        city = st.selectbox("City:", label_encoders["city"].classes_)
        rent = st.number_input("Monthly Rent (in INR):", min_value=0, step=100)
        loan_repayment = st.number_input("Monthly Loan Repayment (in INR):", min_value=0, step=100)
        insurance = st.number_input("Monthly Insurance Expense (in INR):", min_value=0, step=100)
        groceries = st.number_input("Monthly Groceries Expense (in INR):", min_value=0, step=100)
        transport = st.number_input("Monthly Transport Expense (in INR):", min_value=0, step=100)
        eating_out = st.number_input("Monthly Eating Out Expense (in INR):", min_value=0, step=100)
        entertainment = st.number_input("Monthly Entertainment Expense (in INR):", min_value=0, step=100)
        utilities = st.number_input("Monthly Utilities Expense (in INR):", min_value=0, step=100)
        healthcare = st.number_input("Monthly Healthcare Expense (in INR):", min_value=0, step=100)
        education = st.number_input("Monthly Education Expense (in INR):", min_value=0, step=100)
        miscellaneous = st.number_input("Monthly Miscellaneous Expense (in INR):", min_value=0, step=100)
        desired_savings_percentage = st.number_input("Desired Savings Percentage (%):", min_value=0, max_value=100, step=1)
        
        # Prevent prediction if income is zero
        if annual_income == 0:
            st.error("Error: Annual income cannot be zero. Please enter a valid income amount to proceed.")
        
        elif annual_income > 0:
            # Prepare input data
            input_data = {
                "annual_income": annual_income,
                "age": age,
                "Dependents": dependents,
                "Occupation": occupation,
                "city": city,
                "Rent": rent,
                "Loan_Repayment": loan_repayment,
                "Insurance": insurance,
                "Groceries": groceries,
                "Transport": transport,
                "Eating_Out": eating_out,
                "Entertainment": entertainment,
                "Utilities": utilities,
                "Healthcare": healthcare,
                "Education": education,
                "Miscellaneous": miscellaneous,
                "Desired_Savings_Percentage": desired_savings_percentage
            }

            if st.button("Generate Budget Plan"):
                try:
                    # Preprocess and predict
                    input_scaled = preprocess_input(input_data)
                    predictions = model.predict(input_scaled)

                    # Display results
                    st.header("Your Unique Budget Plan")
                    st.write(f"### Annual Income: ₹{annual_income:,.2f}")

                    # Extract and display predictions
                    budget_details = {targets[i]: predictions[0][i] for i in range(len(targets))}
                    for category, savings in budget_details.items():
                        st.write(f"- {category}: ₹{savings:,.2f}")
                    
                    # Display savings tips
                    st.subheader("Suggestions to Maximize Savings:")
                    savings_suggestions = {
                        "Groceries": "Consider buying in bulk or choosing local brands to save more.",
                        "Transport": "Look into carpooling or public transport options.",
                        "Eating Out": "Reducing the frequency of dining out can significantly save.",
                        "Entertainment": "Opt for discounted tickets or free events in your city.",
                        "Utilities": "Switch to energy-efficient appliances to lower electricity bills.",
                        "Healthcare": "Consider preventive care and checkups to reduce long-term healthcare costs.",
                        "Education": "Look for scholarships or online courses to reduce education costs.",
                        "Miscellaneous": "Track and reduce unplanned spending in this category."
                    }
                    
                    for category, suggestion in savings_suggestions.items():
                        st.write(f"- **{category}:** {suggestion}")
                    
                    # Check loan eligibility
                    loan_status = check_loan_eligibility(annual_income, rent + loan_repayment, desired_savings_percentage)
                    st.write(f"### Loan Status: {loan_status}")

                except Exception as e:
                    st.error(f"Error: {e}")

        if st.button("Portfolio Manager"):
            portfolio_manager()

if __name__ == "__main__":
    main()
