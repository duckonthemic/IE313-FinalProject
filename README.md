# Vietnam Job Market Analysis

**IE313 Final Project** - Data Mining and Machine Learning Analysis of Vietnam's Job Market

## Overview

This project analyzes **100,000+ job postings** from major Vietnamese recruitment platforms (CareerViet, TopCV, ViecLam24h, JobsGo) to uncover insights about the job market, salary trends, and skill demands.

## Features

- **Web Crawler**: Automated data collection from multiple job sites using Playwright
- **Data Analysis**: Comprehensive EDA with visualizations (salary distribution, skills demand, geographic trends)
- **ML Models**: 
  - Salary prediction (Random Forest Regressor)
  - Job level classification (Logistic Regression)
  - Job clustering (K-Means)
- **Interactive Dashboard**: Streamlit-based visualization dashboard

## Project Structure

```
├── final_notebook.ipynb   # Main analysis notebook
├── crawler.py             # Web crawler script
├── crawler-ref/           # Crawler with site-specific selectors
├── dashboard/             # Streamlit dashboard app
├── datasets/              # Final merged dataset
├── data/clean/            # Cleaned data files
├── baocao.tex             # LaTeX report source
├── baocao.pdf             # Final report (Vietnamese)
└── requirements.txt       # Python dependencies
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the analysis notebook
jupyter notebook final_notebook.ipynb

# Launch dashboard
cd dashboard && streamlit run app.py
```

## Tech Stack

- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly, wordcloud
- **ML/AI**: scikit-learn, statsmodels
- **Crawling**: Playwright, playwright-stealth
- **Dashboard**: Streamlit

## Dataset

| Metric | Value |
|--------|-------|
| Total Jobs | 100,000+ |
| Sources | 4 platforms |
| Features | 11 columns |
| Salary Coverage | ~97% |

## Authors

**IE313 - Data Mining** | University of Information Technology (UIT)

## License

This project is for educational purposes only.
