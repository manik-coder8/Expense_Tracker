📘 Expense Tracker Application
==============================

A simple full-stack **Expense Tracker** application built using **FastAPI** (backend) and **Streamlit** (frontend).The app allows users to add expenses, view them in a table, filter by category or date, sort by newest entries, and see the total amount of visible expenses.

👉 Live Links
-----------

API docs will run at:

 [https://expense-tracker-backend-hst2.onrender.com/docs](https://expense-tracker-backend-hst2.onrender.com/docs)

Application available at:

 [https://expensetracker-1.streamlit.app/](https://expensetracker-1.streamlit.app/)

🚀 Features
-----------

### Backend (FastAPI)

*   Create a new expense
    
*   Prevent duplicate submissions using request\_id (idempotency)
    
*   Store data in SQLite database
    
*   List all expenses
    
*   Filter expenses by category
    
*   Filter expenses by date
    
*   Sort expenses by newest date
    
*   Provide distinct categories and dates for frontend filters
    

### Frontend (Streamlit)

*   Simple and clean UI
    
*   Add new expense form
    
*   View expenses in a table
    
*   Filter by category
    
*   Filter/sort by date
    
*   Display total amount of visible expenses
    
*   Handles:
    
    *   Multiple submit clicks
        
    *   Slow or failed API responses
        
*   Minimal styling with focus on clarity and correctness
    

🧱 Tech Stack
-------------

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Database:** SQLite
- **Language:** Python
- **HTTP Client:** Requests

📂 Project Structure
--------------------
```text
project-root/
├── backend/
│   ├── main.py
│   └── expenses.db
├── frontend/
│   └── app.py
├── requirements.txt
└── README.md
```

⚙️ Setup Instructions
---------------------

### 1️⃣ Install Dependencies

Make sure Python 3.9+ is installed.

```   pip install -r requirements.txt   ```

### 2️⃣ Run Backend (FastAPI)

```cd backend  uvicorn main:app --reload   ```

Backend will run at:

```   http://localhost:8000  ```

API docs available at:

```   http://localhost:8000/docs   ```

### 3️⃣ Run Frontend (Streamlit)

Open a new terminal:

```   cd frontend  streamlit run app.py   ```

Frontend will run at:

```   http://localhost:8501   ```

🔄 Application Workflow
-----------------------

1.  User opens the Streamlit app.
    
2.  User chooses:
    
    *   **Add New Expense** → fills the form and saves expense.
        
    *   **View Expenses** → sees existing expenses.
        
3.  Frontend sends API requests to FastAPI backend.
    
4.  Backend:
    
    *   Stores data in SQLite.
        
    *   Returns filtered/sorted data as requested.
        
5.  Frontend displays:
    
    *   Expense table
        
    *   Total amount
        
    *   Filters populated dynamically from backend.
        

🗃 Database Design
------------------

## 🗃 Database Design

The application uses a single SQLite table to store expense records.

### Table: `expenses`

| Column | Type | Description |
|------|------|-------------|
| `id` | TEXT | Unique expense ID (UUID) |
| `amount` | INTEGER | Expense amount stored as integer (amount × 100) |
| `category` | TEXT | Expense category |
| `description` | TEXT | Expense description |
| `date` | TEXT | Expense date (YYYY-MM-DD) |
| `created_at` | TEXT | Record creation timestamp (UTC) |
| `request_id` | TEXT | Unique request identifier for idempotency |

**Note:**  
The `amount` is stored as an integer to avoid floating-point precision issues.


🔐 Idempotency Handling
-----------------------

Each expense submission includes a request\_id. If the same request is submitted multiple times, the backend safely returns the existing record instead of creating duplicates.

🧪 Error Handling
-----------------

*   Graceful handling of API failures
    
*   Loading spinners for slow responses
    
*   Safe fallback for empty data
    
*   User-friendly messages
    

🔮 Future Improvements
----------------------

If extended further, the application could include:

*   User authentication & multiple users
    
*   Edit / delete expense functionality
    
*   Monthly / yearly expense summaries
    
*   Charts and visual analytics
    
*   Export expenses as CSV or PDF
    
*   Category management (dropdown instead of free text)
    
*   Dockerization for easier deployment

*   Can integrate UPI apps for seamless expense recording and payments.
    

✅ Assignment Checklist
----------------------

✔ Backend API implemented

✔ Frontend UI implemented

✔ Filtering & sorting supported

✔ Total amount displayed

✔ Handles multiple submissions & refresh

✔ Clean code and clear workflow

👤 Made By: Manik
---------