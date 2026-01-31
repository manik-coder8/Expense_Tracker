import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.title("💸 Expense Tracker")

# ---------------- ADD EXPENSE ----------------
st.subheader("Add New Expense")

with st.form("add_expense_form", clear_on_submit=True):
    amount = st.number_input("Amount (₹)", min_value=0.01)
    category = st.text_input("Category")
    description = st.text_input("Description")
    date = st.date_input("Date")

    submit = st.form_submit_button("Add Expense")

    if submit:
        payload = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": str(date),
            "request_id": str(uuid.uuid4())
        }

        with st.spinner("Saving expense..."):
            try:
                r = requests.post(f"{API_URL}/expenses", json=payload, timeout=5)
                r.raise_for_status()
                st.success("Expense added successfully!")
            except Exception:
                st.error("Failed to save expense. Please try again.")

# ---------------- FILTER & SORT ----------------
st.subheader("Expenses")

filter_category = st.selectbox(
    "Filter by category",
    ["All"]
)

sort_option = st.selectbox(
    "Sort by date",
    ["Newest first"]
)

params = {"sort": "date_desc"}
if filter_category != "All":
    params["category"] = filter_category

with st.spinner("Loading expenses..."):
    try:
        response = requests.get(f"{API_URL}/expenses", params=params, timeout=5)
        response.raise_for_status()
        expenses = response.json()
    except Exception:
        st.error("Failed to load expenses")
        expenses = []

# ---------------- DISPLAY ----------------
if expenses:
    total = sum(e["amount"] for e in expenses)
    st.markdown(f"### Total: ₹{total}")

    st.table([
        {
            "Date": e["date"],
            "Category": e["category"],
            "Description": e["description"],
            "Amount (₹)": e["amount"]
        }
        for e in expenses
    ])
else:
    st.info("No expenses to show.")
