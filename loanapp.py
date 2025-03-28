import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("💳 Advanced Loan Calculator")

st.sidebar.header("Loan Details")
loan_amount = st.sidebar.number_input("Loan Amount (PKR)", min_value=10000, max_value=10000000, value=500000, step=10000)
interest_rate = st.sidebar.slider("Annual Interest Rate (%)", min_value=1.0, max_value=30.0, value=12.0, step=0.1)
loan_tenure = st.sidebar.slider("Loan Tenure (Years)", min_value=1, max_value=30, value=5, step=1)

monthly_rate = (interest_rate / 100) / 12
num_payments = loan_tenure * 12
emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)

total_payment = emi * num_payments
total_interest = total_payment - loan_amount

st.write(f"### 📌 Monthly EMI: **PKR {emi:,.2f}**")
st.write(f"💰 **Total Payment (Loan + Interest):** PKR {total_payment:,.2f}")
st.write(f"📈 **Total Interest Paid:** PKR {total_interest:,.2f}")

st.sidebar.header("Early Payment Options")
extra_payment = st.sidebar.number_input("Extra Monthly Payment (PKR)", min_value=0, max_value=int(loan_amount), value=0, step=5000)

months = np.arange(1, num_payments + 1)
remaining_balance = loan_amount
principal_paid = []
interest_paid = []
balances = []
extra_months_saved = 0

for _ in months:
    if remaining_balance <= 0:
        break  
    interest = remaining_balance * monthly_rate
    principal = emi - interest
    if extra_payment > 0:
        principal += extra_payment
    remaining_balance -= principal

    interest_paid.append(interest)
    principal_paid.append(principal)
    balances.append(max(remaining_balance, 0))  

    if remaining_balance <= 0:
        break  

extra_months_saved = num_payments - len(principal_paid)

if extra_payment > 0:
    st.write(f"🚀 **With Extra Payment of PKR {extra_payment:,.2f}, You Save {extra_months_saved} Months!**")

fig, ax = plt.subplots(figsize=(8, 4))
ax.stackplot(range(1, len(principal_paid) + 1), principal_paid, interest_paid, labels=["Principal", "Interest"], colors=["#2ecc71", "#e74c3c"])
ax.set_title("Loan Payment Breakdown")
ax.set_xlabel("Month")
ax.set_ylabel("Amount (PKR)")
ax.legend()
st.pyplot(fig)

df = pd.DataFrame({
    "Month": range(1, len(principal_paid) + 1),
    "Principal Paid": np.round(principal_paid, 2),
    "Interest Paid": np.round(interest_paid, 2),
    "Remaining Balance": np.round(balances, 2),
})

st.write("### 📊 Loan Amortization Schedule")
st.dataframe(df)

csv = df.to_csv(index=False).encode()
st.download_button(label="📥 Download Amortization Schedule", data=csv, file_name="loan_schedule.csv", mime="text/csv")
