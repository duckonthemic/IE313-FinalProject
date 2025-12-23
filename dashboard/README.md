# 📊 Vietnam Job Market Dashboard

Real-time interactive dashboard for Vietnam Job Market Analysis.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd dashboard
pip install -r requirements.txt
```

### 2. Run Dashboard
```bash
streamlit run app.py
```

Or from project root:
```bash
streamlit run dashboard/app.py
```

### 3. Open in Browser
Dashboard will automatically open at: `http://localhost:8501`

## 📋 Features

- **🔍 Interactive Filters**: Region, Position, Salary Range, Experience
- **📊 KPI Metrics**: Total jobs, Median salary, City count, etc.
- **🗺️ Geographic Analysis**: Top cities, Regional distribution
- **💰 Salary Analysis**: Distribution, by position, by region
- **📈 Trend Analysis**: Salary vs Experience correlation
- **🏭 Industry Analysis**: Top industries and required skills
- **📋 Data Explorer**: Paginated data table with search

## 🛠️ Tech Stack

- **Streamlit**: Web framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data processing
- **NumPy**: Numerical operations

## 📁 Data Source

Dashboard reads from:
- `data/clean/jobs_clean.csv` (preferred)
- `datasets/dataset_final.csv` (fallback)

Make sure to run the Jupyter notebook first to generate cleaned data.

## 📸 Screenshots

![Dashboard Preview](preview.png)

---
*Built with ❤️ for IE313 Final Project*
