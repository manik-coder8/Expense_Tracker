import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.title("💸 Expense Tracker")

# ---------------- SESSION STATE ----------------
if "show_add_expense" not in st.session_state:
    st.session_state.show_add_expense = False

if "show_expenses" not in st.session_state:
    st.session_state.show_expenses = False

# ---------------- ACTION BUTTONS ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Add New Expense"):
        st.session_state.show_add_expense = True
        st.session_state.show_expenses = False

with col2:
    if st.button("📄 View Expenses"):
        st.session_state.show_expenses = True
        st.session_state.show_add_expense = False

st.divider()

# ---------------- ADD EXPENSE ----------------
if st.session_state.show_add_expense:
    st.subheader("Add New Expense")

    with st.form("add_expense_form", clear_on_submit=True):
        amount = st.number_input("Amount (₹)", min_value=0.01)
        category = st.text_input("Category")
        description = st.text_input("Description")
        date = st.date_input("Date")

        submit = st.form_submit_button("Save Expense")

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
                    r = requests.post(
                        f"{API_URL}/expenses",
                        json=payload,
                        timeout=5
                    )
                    r.raise_for_status()
                    st.success("Expense added successfully!")
                except Exception:
                    st.error("Failed to save expense. Please try again.")

# ---------------- VIEW EXPENSES ----------------
if st.session_state.show_expenses:
    st.subheader("Expenses")

    # ---- Fetch available filters from backend ----
    try:
        filters_response = requests.get(
            f"{API_URL}/expenses/filters",
            timeout=5
        )
        filters_response.raise_for_status()
        filters = filters_response.json()

        categories = ["All"] + filters.get("categories", [])
        dates = ["All"] + filters.get("dates", [])
    except Exception:
        st.error("Failed to load filters")
        categories = ["All"]
        dates = ["All"]

    # ---- Filters ----
    filter_category = st.selectbox("Filter by category", categories)
    filter_date = st.selectbox("Sort / Filter by date", dates)

    params = {"sort": "date_desc"}

    if filter_category != "All":
        params["category"] = filter_category

    if filter_date != "All":
        params["date"] = filter_date

    # ---- Fetch expenses ----
    with st.spinner("Loading expenses..."):
        try:
            response = requests.get(
                f"{API_URL}/expenses",
                params=params,
                timeout=5
            )
            response.raise_for_status()
            expenses = response.json()
        except Exception:
            st.error("Failed to load expenses")
            expenses = []

    # ---- Display ----
    if expenses:
        total = sum(e["amount"] for e in expenses)
        st.markdown(f"## Total: ₹{total}")

        st.table([
            {
                "Date": e["date"],
                "Category": e["category"],
                "Description": e["description"],
                "Amount (₹)": f"{e['amount']:.2f}"
            }
            for e in expenses
        ])
    else:
        st.info("No expenses found.")
