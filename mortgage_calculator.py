import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
import base64

def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/webp;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="Mortgage Repayments Calculator", page_icon="🏠", layout="centered")

set_background("/Users/aayushlshrestha/Documents/Projects/MorCalc/images/ai.webp")

st.title("🏠 Mortgage Repayments Calculator")
st.write("### Calculate your monthly mortgage repayments and view your payment schedule.")

st.sidebar.header("Input Data")
home_value = st.sidebar.number_input("Home Value ($)", min_value=0, value=500000, step=1000)
deposit = st.sidebar.number_input("Deposit ($)", min_value=0, value=100000, step=1000)
interest_rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, value=5.5, step=0.1)
loan_term = st.sidebar.number_input("Loan Term (years)", min_value=1, value=30, step=1)

loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments Summary")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")

# Create a data-frame with the payment schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)

st.write("### Interactive Payment Breakdown")
chart_type = st.selectbox("Select chart type", ["Line Chart", "Bar Chart", "Area Chart"])

payment_breakdown_df = df[["Month", "Principal", "Interest"]].set_index("Month")

if chart_type == "Line Chart":
    st.line_chart(payment_breakdown_df)
elif chart_type == "Bar Chart":
    st.bar_chart(payment_breakdown_df)
else:
    st.area_chart(payment_breakdown_df)

st.write("### Full Payment Schedule")
st.dataframe(df)
