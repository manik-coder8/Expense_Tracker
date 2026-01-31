import streamlit as st
import requests
import uuid

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💸",
    layout="centered"
)

API_URL = "https://expense-tracker-backend-hst2.onrender.com"

# ---------------- SESSION STATE ----------------
if "show_add_expense" not in st.session_state:
    st.session_state.show_add_expense = False

if "show_expenses" not in st.session_state:
    st.session_state.show_expenses = False

# ---------------- HERO SECTION ----------------
st.markdown(
    """
    <div style="text-align: center; margin-top: 30px;">
        <h1>💸 Expense Tracker</h1>
        <p style="font-size: 18px; color: gray;">
            Track, filter, and understand where your money goes.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- MAIN ACTION BUTTONS ----------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button("➕ Add New Expense", use_container_width=True):
            st.session_state.show_add_expense = True
            st.session_state.show_expenses = False

    with btn_col2:
        if st.button("📄 View Expenses", use_container_width=True):
            st.session_state.show_expenses = True
            st.session_state.show_add_expense = False

st.markdown("---")

# ---------------- EMPTY STATE ----------------
if not st.session_state.show_add_expense and not st.session_state.show_expenses:
    st.info("👆 Start by adding a new expense or view your existing expenses.")

# ---------------- ADD EXPENSE CARD ----------------
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
                    response = requests.post(
                        f"{API_URL}/expenses",
                        json=payload,
                        timeout=5
                    )
                    response.raise_for_status()
                    st.success("✅ Expense added successfully!")
                except Exception:
                    st.error("❌ Failed to save expense. Please try again.")

# ---------------- VIEW EXPENSES CARD ----------------
if st.session_state.show_expenses:
    st.subheader("Expenses")

    # ---- Fetch filters from backend ----
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

    # ---- Filters UI ----
    filter_category = st.selectbox("Filter by category", categories)
    filter_date = st.selectbox("Filter / Sort by date", dates)

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
            st.error("❌ Failed to load expenses")
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
        st.info("No expenses found for the selected filters.")
