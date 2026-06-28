Markdown
# 📊 Personal Finance Tracker 3.0

An interactive, data-driven web application designed to track, filter, and visualize personal income and expenses. This project evolved from a standard Python command-line utility into an advanced data analytics dashboard leveraging **Pandas** and **Streamlit**.

## 🚀 Key Features

- **Interactive Navigation:** Sidebar-driven web interface replacing legacy terminal menus.
- **Monthly Insights:** Filter data by month to instantly calculate total expenses and view a clear distribution percentage breakdown.
- **Dynamic Data Visualization:** High-quality charts including expense pie charts and income vs. expenses bar charts using **Matplotlib**.
- **Flexible Date Range Analysis:** Custom start and end date pickers to safely monitor net balances over specific periods.
- **Robust Architecture:** Structured codebase with dedicated source, configuration, and data layers.

## 🛠️ Tech Stack & Tools

- **Language:** Python 3.12+
- **Data Analysis:** Pandas
- **Data Visualization:** Matplotlib
- **Web Framework:** Streamlit
- **Environment Management:** `uv` (Fast Python package installer and resolver)

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/andrea-francalanci/Personal-Finance-Tracker.git](https://github.com/andrea-francalanci/Personal-Finance-Tracker.git)
   cd Personal-Finance-Tracker
2.uv run streamlit run src/app.py