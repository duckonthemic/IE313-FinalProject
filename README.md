# 🇻🇳 Vietnam IT Jobs - Data Merge & Analysis Pipeline

> **Enterprise-grade data science pipeline for merging and analyzing Vietnamese IT job market datasets**

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Jobs](https://img.shields.io/badge/Jobs-3,985-orange.svg)](data/)
[![Accuracy](https://img.shields.io/badge/Model_Accuracy-77.46%25-success.svg)](data/clean/models/)

## 📊 Project Overview

This project implements a complete **15-step data merge and machine learning pipeline** for analyzing Vietnam's IT job market. It combines data from **Kaggle** (ITViec) and **GitHub** (multi-source) repositories to create a comprehensive master dataset with advanced normalization, deduplication, and ML classification.

### 🎯 Key Features

- 🔄 **Smart Data Merging**: Combines 2 datasets with priority-based deduplication (11.7% dedup rate)
- 🧹 **Advanced Normalization**: City names, job levels, categories, skills standardization
- 📊 **Master Schema**: 19-column unified schema covering all job attributes
- 🤖 **ML Classification**: XGBoost classifier for 10 job categories (77.46% accuracy)
- 📈 **EDA Visualizations**: 4+ interactive charts analyzing market trends
- 📁 **Multiple Formats**: CSV, Parquet, and DuckDB exports
- 📓 **Complete Notebook**: Step-by-step pipeline with detailed documentation

### 📊 Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Unique Jobs** | 3,985 |
| **Kaggle Source (ITViec)** | 1,412 jobs |
| **GitHub Source (Multi-site)** | 3,101 jobs |
| **Deduplication Rate** | 11.7% |
| **Job Sites Covered** | ITViec, LinkedIn, TopCV |
| **Valid ML Categories** | 10 categories |
| **ML Dataset Size** | 3,859 jobs (96.8%) |
| **Model Accuracy** | 77.46% (XGBoost) |

> ⚠️ **Lưu ý về Salary Data**: Cả 2 nguồn dữ liệu hiện tại (Kaggle và GitHub) **không cung cấp thông tin lương**. Pipeline đã chuẩn bị sẵn các trường salary trong schema (salary_min, salary_max, salary_avg, salary_currency) nhưng hiện đang **100% NULL**. Các trường này sẵn sàng được sử dụng khi có nguồn dữ liệu mới có thông tin lương (ví dụ: VietnamWorks, TopCV). Xem chi tiết tại [docs/schema.md - Salary Fields](docs/schema.md#-salary-fields---current-status).

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- pip package manager
- 2GB+ RAM (for ML training)
- pandas, scikit-learn, xgboost (see requirements.txt)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/duckonthemic/IE313-FinalProject.git
cd IE313-FinalProject-main
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 🎯 Usage - Run Complete Pipeline

Open and execute the **Jupyter Notebook** with all 15 steps:

```bash
jupyter notebook vietnam_it_jobs_merge_analysis.ipynb
```

**Execute cells sequentially** to run the complete pipeline:

1. **Import Libraries** - Load all required packages
2. **Load Raw Datasets** - Load Kaggle and GitHub data
3. **Schema Design** - Define 19-column master schema
4. **Column Mapping** - Map both datasets to master schema
5. **Normalization Functions** - Define city, salary, level, category normalizers
6. **Apply Normalization** - Clean and standardize both datasets
7. **Merge & Deduplicate** - Combine datasets with priority-based deduplication
8. **Data Quality Check** - Comprehensive quality report
9. **Save Processed Data** - Export master table and intermediate files
10. **EDA** - Generate 4 visualizations (categories, levels, cities, salaries)
11. **Feature Engineering** - Create TF-IDF + encoded features (505 total)
12. **Model Training** - Train Random Forest and XGBoost
13. **Model Evaluation** - Classification reports and confusion matrices
14. **Save Models** - Export best model with transformers
15. **Final Summary** - Complete pipeline report

### ⚡ Alternative: Run Individual Steps

If you prefer command-line execution:

```bash
# View the processed master data
python -c "import pandas as pd; df = pd.read_csv('data/final/jobs_master.csv'); print(df.info()); print(df.head())"

# Check model results
python -c "import pickle; m = pickle.load(open('data/final/best_model.pkl', 'rb')); print(f'Model: {m[\"model_name\"]}'); print(f'Accuracy: {m[\"accuracy\"]:.2%}')"
```

---

## 📁 Project Structure

```
IE313-FinalProject-main/
├── data/
│   ├── raw/
│   │   ├── kaggle/
│   │   │   ├── jobs.csv              # 1,412 jobs from Kaggle
│   │   │   └── companies.csv         # 2,041 companies info
│   │   └── github/
│   │       └── job_descriptions.csv  # 3,101 jobs from GitHub
│   ├── processed/
│   │   ├── jobs_kaggle_clean.csv     # Normalized Kaggle data
│   │   └── jobs_github_clean.csv     # Normalized GitHub data
│   └── final/
│       ├── jobs_master.csv           # 3,985 unique jobs (12.1 MB)
│       ├── jobs_master.parquet       # Compressed format (6.05 MB)
│       └── best_model.pkl            # XGBoost model + transformers (1.49 MB)
├── vietnam_it_jobs_merge_analysis.ipynb  # Main pipeline notebook
├── requirements.txt                   # Python dependencies
├── README.md                         # This file
└── IMPROVEMENTS.md                   # Project changelog
```

### 📂 Data Files Description

**Raw Data** (unchanged source data):
- `kaggle/jobs.csv`: ITViec jobs with company_id references
- `kaggle/companies.csv`: Company information and metadata
- `github/job_descriptions.csv`: Multi-source jobs (ITViec, LinkedIn, TopCV)

**Processed Data** (normalized, not merged):
- `jobs_kaggle_clean.csv`: Kaggle data mapped to master schema
- `jobs_github_clean.csv`: GitHub data mapped to master schema

**Final Data** (merged and deduplicated):
- `jobs_master.csv`: Complete master table with 3,985 unique jobs
- `jobs_master.parquet`: Same data in compressed Parquet format
- `best_model.pkl`: Trained XGBoost model with all transformers (TF-IDF, LabelEncoders)

---

## 🔧 Pipeline Details - 15 Steps

### Step 1-3: Schema Design & Column Mapping

**Master Schema** (19 columns):
```
job_id, source_dataset, job_site, job_title, company_name, 
city, job_category, job_level, salary_min, salary_max, 
location_raw, job_description, skills, country, province, 
salary_avg, salary_currency, employment_type, url
```

**Column Mapping**:
- **Kaggle**: Joins jobs.csv with companies.csv to get company names
- **GitHub**: Maps title, company, location, description, skills, url directly
- **Standardization**: Both datasets mapped to identical schema

### Step 4-6: Data Normalization

**City Normalization**:
- Maps variations → Standard names: `Ha Noi`, `Ho Chi Minh`, `Da Nang`, `Remote`, `Other`
- Examples: "hà nội" → "Ha Noi", "hcm" → "Ho Chi Minh", "đà nẵng" → "Da Nang"

**Salary Parsing** (if available):
- Extracts min/max from salary strings
- Converts USD to VND (rate: 24,000)
- Handles "triệu" (millions) in Vietnamese text
- Calculates average: `(min + max) / 2`

**Job Level Extraction** (from title):
- `intern`: intern, fresher, graduate
- `junior`: junior, jr
- `mid`: default (no specific keywords)
- `senior`: senior, sr, lead, principal, staff
- `manager`: manager, head, director, chief, VP, CTO, CEO

**Job Category Classification** (12 categories):
- Backend Developer, Frontend Developer, Fullstack Developer
- Mobile Developer, DevOps Engineer, Data Engineer, Data Scientist
- QA/Tester, Security Engineer, Software Engineer
- Product Manager, Business Analyst
- Other (default if no keywords match)

**Skills Normalization**:
- Converts to pipe-separated format: `python|sql|docker`
- Cleans brackets, quotes, and whitespace

### Step 7: Merge and Deduplicate

**Merging Strategy**:
1. Align columns between both datasets (add missing columns as None)
2. Concatenate vertically: `Kaggle + GitHub`
3. Remove rows with empty title or company_name
4. **Deduplication**: Based on `title + company + city` (case-insensitive)
5. **Priority**: Kaggle data kept first (sort by source_dataset)
6. Generate unique `job_id`: `job_000000`, `job_000001`, etc.

**Results**:
- Before merge: 4,513 jobs (1,412 + 3,101)
- After dedup: **3,985 unique jobs** (11.7% reduction)

### Step 8-9: Data Quality & Export

**Quality Metrics**:
- Source distribution: Kaggle vs GitHub
- Job site distribution: ITViec, LinkedIn, TopCV
- City distribution: Ha Noi (35.9%), Ho Chi Minh (51.7%), Other
- Category distribution: Top 10 categories
- Level distribution: intern, junior, mid, senior, manager
- Missing values: Comprehensive report per column

**Export Formats**:
- CSV: `jobs_master.csv` (12.1 MB)
- Parquet: `jobs_master.parquet` (6.05 MB, compressed)
- Intermediate: `jobs_kaggle_clean.csv`, `jobs_github_clean.csv`

### Step 10: Exploratory Data Analysis (EDA)

**4 Key Visualizations**:

1. **Job Category Distribution** (Bar Chart)
   - Top 15 categories ranked by count
   - Shows market demand for each role type

2. **Job Level Distribution** (Pie Chart)
   - Breakdown: intern, junior, mid, senior, manager
   - Reveals seniority distribution in market

3. **City Distribution** (Bar Chart)
   - Top 10 cities by job count
   - Geographic job concentration analysis

4. **Salary Distribution** (Histogram)
   - Only if salary data available (>100 jobs)
   - Salary ranges in Million VND/month

### Step 11: Feature Engineering for ML

**Text Features** (TF-IDF):
- Combines: `job_title + job_description + skills`
- TF-IDF Vectorizer: 500 features, bigrams (1,2), English stopwords
- Output: Sparse matrix (3,859 × 500)

**Encoded Features** (5 additional):
- `level_encoded`: LabelEncoded job_level
- `city_encoded`: LabelEncoded city
- `has_salary`: Binary (0/1)
- `title_length`: Character count of job_title
- `desc_length`: Character count of job_description

**Total Features**: 505 (500 TF-IDF + 5 encoded)

**ML Dataset**:
- Filtered categories with ≥50 samples: **10 categories**
- Total ML jobs: **3,859 (96.8%)**
- Train/Test split: 80/20 (stratified by category)

### Step 12-13: Model Training & Evaluation

**Models Trained**:

1. **Random Forest** (100 trees)
   - Accuracy: 69.17%
   - Baseline ensemble model

2. **XGBoost** (100 estimators)
   - Accuracy: **77.46%** ⭐ Best
   - Gradient boosting classifier

**Evaluation Outputs**:
- Classification report (precision, recall, F1-score per category)
- Confusion matrix heatmap
- Model accuracy comparison bar chart

### Step 14-15: Model Export & Summary

**Model Save** (`best_model.pkl`):
```python
{
    'model': XGBClassifier,
    'tfidf': TfidfVectorizer,
    'le_target': LabelEncoder (categories),
    'le_level': LabelEncoder (job_levels),
    'le_city': LabelEncoder (cities),
    'feature_cols': ['level_encoded', 'city_encoded', ...],
    'accuracy': 0.7746,
    'model_name': 'XGBoost'
}
```

**Final Summary Report**:
- Data merge statistics
- Source/city/category distributions
- ML dataset composition
- Best model performance
- Top 5 job categories
- All output file locations

---

## 📊 Model Performance

### Classification Results

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| **XGBoost** ⭐ | **77.46%** | **78%** | **77%** | **77%** |
| Random Forest | 69.17% | 70% | 69% | 69% |

### Per-Category Performance (XGBoost)

| Category | Precision | Recall | F1-Score | Support |
|----------|-----------|--------|----------|---------|
| **Backend Developer** | 0.69 | 0.65 | 0.67 | 75 |
| **Business Analyst** | 0.81 | 0.59 | 0.69 | 37 |
| **Data Engineer** | 0.79 | 0.79 | 0.79 | 14 |
| **DevOps Engineer** | 0.62 | 0.76 | 0.68 | 17 |
| **Frontend Developer** | 0.85 | 0.76 | 0.80 | 58 |
| **Fullstack Developer** | 0.77 | 0.48 | 0.59 | 69 |
| **Mobile Developer** | 0.85 | 0.85 | 0.85 | 61 |
| **Other** | 0.75 | 0.87 | 0.80 | 323 |
| **QA/Tester** | 0.96 | 0.94 | 0.95 | 68 |
| **Software Engineer** | 0.70 | 0.60 | 0.65 | 50 |

**Best Performing Categories**: QA/Tester (F1: 0.95), Mobile Developer (F1: 0.85), Frontend Developer (F1: 0.80)

**Challenging Categories**: Fullstack Developer (F1: 0.59) - likely due to overlap with Backend/Frontend roles

### Market Insights

#### Top 5 Job Categories
1. **Other**: 1,615 jobs (40.5%) - Diverse specialized roles
2. **Backend Developer**: 374 jobs (9.4%)
3. **Fullstack Developer**: 345 jobs (8.7%)
4. **QA/Tester**: 338 jobs (8.5%)
5. **Mobile Developer**: 303 jobs (7.6%)

#### Geographic Distribution
- **Ho Chi Minh City**: 2,060 jobs (51.7%) - Tech hub dominates
- **Ha Noi**: 1,431 jobs (35.9%) - Second largest market
- **Da Nang**: 115 jobs (2.9%) - Growing tech scene
- **Other cities**: 379 jobs (9.5%)

#### Seniority Distribution
- **Mid-level**: 2,618 jobs (65.7%) - Largest demand
- **Senior**: 928 jobs (23.3%)
- **Junior**: 198 jobs (5.0%)
- **Manager**: 131 jobs (3.3%)
- **Intern**: 110 jobs (2.8%)

#### Data Sources
- **GitHub (Multi-source)**: 2,574 jobs (64.6%) - LinkedIn, ITViec, TopCV
- **Kaggle (ITViec)**: 1,411 jobs (35.4%) - Pure ITViec data

#### Data Quality
- **Salary Data**: 0% available (not collected in source datasets)
- **Job Description**: 100% complete
- **Skills**: 100% complete
- **Location**: 100% complete with normalization
- **Company Name**: 100% complete (1,901 unique companies)

---

## 📈 Visualizations

The Jupyter notebook generates **4 key visualizations**:

### 1. Job Category Distribution (Horizontal Bar Chart)
- Shows top 15 job categories by count
- Highlights market demand across different roles
- "Other" category shows diversity of specialized positions

### 2. Job Level Distribution (Pie Chart)
- Breakdown of seniority levels: intern, junior, mid, senior, manager
- Mid-level positions dominate (65.7%)
- Visual representation of career level distribution

### 3. City Distribution (Bar Chart)
- Top 10 cities ranked by job postings
- Ho Chi Minh leads (51.7%), followed by Ha Noi (35.9%)
- Shows geographic concentration of IT jobs

### 4. Salary Distribution (Histogram)
- Only generated if salary data available (>100 jobs with salary)
- Distribution of salary ranges in Million VND/month
- Note: Current dataset has no salary data (0% availability)

---

## 🛠️ Technical Stack

### Core Libraries

**Data Processing**:
- `pandas` (2.2.3) - Data manipulation and analysis
- `numpy` (2.1.3) - Numerical computing
- `pyarrow` - Parquet file format support

**Machine Learning**:
- `scikit-learn` (1.6.1) - ML algorithms and evaluation
  - TfidfVectorizer, LabelEncoder
  - RandomForestClassifier, train_test_split
  - Classification metrics
- `xgboost` (3.0.1) - Gradient boosting classifier
- `scipy` (1.15.3) - Sparse matrix operations

**Visualization**:
- `matplotlib` (3.10.0) - Static plotting
- `seaborn` (0.13.2) - Statistical visualizations

**Utilities**:
- `re` (regex) - Pattern matching for normalization
- `pickle` - Model serialization
- `warnings` - Warning suppression

### System Requirements

- **Python**: 3.13+ (tested on 3.13.5)
- **RAM**: 2GB+ recommended for ML training
- **Storage**: 100MB for data + models
- **OS**: Windows, macOS, Linux (cross-platform)

See `requirements.txt` for complete dependency list with exact versions.

---

## 📚 Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

**Core Dependencies** (see requirements.txt for exact versions):
```
pandas>=2.2.0          # Data manipulation
numpy>=2.1.0           # Numerical computing
scikit-learn>=1.6.0    # Machine learning
xgboost>=3.0.0         # Gradient boosting
matplotlib>=3.10.0     # Plotting
seaborn>=0.13.0        # Statistical plots
scipy>=1.15.0          # Scientific computing
pyarrow>=19.0.0        # Parquet format
jupyter>=1.1.0         # Notebook environment
```

---

## 🔍 Data Schema

### Master Table Schema (`jobs_master.csv`)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `job_id` | string | Unique identifier | `job_000000` |
| `source_dataset` | string | Data source | `kaggle_itviec`, `github_it_job_posting` |
| `job_site` | string | Job posting site | `itviec`, `LinkedIn`, `TopCV` |
| `job_title` | string | Job position title | `Senior Backend Engineer` |
| `company_name` | string | Company name | `Vinova`, `FPT Software` |
| `city` | string | Normalized city | `Ha Noi`, `Ho Chi Minh`, `Da Nang` |
| `job_category` | string | Job role category | `Backend Developer`, `Frontend Developer` |
| `job_level` | string | Seniority level | `intern`, `junior`, `mid`, `senior`, `manager` |
| `salary_min` | float | Minimum salary (VND) | `None` (not available in source) |
| `salary_max` | float | Maximum salary (VND) | `None` (not available in source) |
| `location_raw` | string | Original location string | `Hồ Chí Minh`, `Ha Noi, Vietnam` |
| `job_description` | text | Full job description | Long text... |
| `skills` | string | Skills (pipe-separated) | `python\|sql\|docker` |
| `country` | string | Country | `Vietnam` |
| `province` | string | Province/City | Same as `city` |
| `salary_avg` | float | Average salary | `None` (not available) |
| `salary_currency` | string | Currency | `None` (not available) |
| `employment_type` | string | Employment type | `full_time` (default) |
| `url` | string | Job posting URL | GitHub source only |

**Total**: 19 columns × 3,985 rows

### Key Notes

- **City Normalization**: All location variations mapped to standard names
- **Job Category**: 13 total categories (10 valid for ML with ≥50 samples)
- **Job Level**: Extracted from job titles using keyword matching
- **Skills**: Normalized to lowercase, pipe-separated format
- **Salary**: Not available in source datasets (100% NULL)
- **Deduplication**: Based on `job_title + company_name + city` (case-insensitive)

---

## 🚀 Future Enhancements

### Data Collection & Quality
- [ ] Add salary information from additional sources
- [ ] Include company ratings and reviews
- [ ] Expand to more job boards (VietnamWorks, CareerBuilder)
- [ ] Implement real-time data updates (weekly/monthly)
- [ ] Add job benefits and perks information
- [ ] Collect application deadline dates

### Advanced ML & NLP
- [ ] Implement PhoBERT for Vietnamese text understanding
- [ ] Build job-candidate matching recommendation system
- [ ] Add salary prediction model (when data available)
- [ ] Skill extraction using NER (Named Entity Recognition)
- [ ] Career path recommendation based on skill progression
- [ ] Handle class imbalance with SMOTE/oversampling

### Feature Engineering
- [ ] Extract tech stack from job descriptions
- [ ] Company size and industry classification
- [ ] Job posting recency as feature
- [ ] Geographic proximity features
- [ ] Company reputation scores

### Deployment & Production
- [ ] Build REST API with FastAPI
- [ ] Create interactive web dashboard (Streamlit)
- [ ] Deploy on cloud (AWS/GCP/Azure)
- [ ] Set up CI/CD pipeline
- [ ] Add automated testing suite
- [ ] Implement data versioning (DVC)

### Analytics & Insights
- [ ] Time-series trend analysis (job market changes over time)
- [ ] Skill demand forecasting
- [ ] Regional salary benchmarking
- [ ] Company hiring pattern analysis
- [ ] Job posting competition metrics
- [ ] Career transition pathway mapping

---

## 📖 Documentation

### Main Notebook

**`vietnam_it_jobs_merge_analysis.ipynb`** - Complete interactive pipeline:

- **15 sequential steps** with detailed explanations
- **Inline visualizations** (4 charts)
- **Code comments** explaining each function
- **Output displays** showing results at each step
- **Markdown cells** with methodology descriptions

### Additional Files

- **`README.md`** - This comprehensive project documentation
- **`IMPROVEMENTS.md`** - Project changelog and improvement log
- **`requirements.txt`** - Python package dependencies with versions

### Learning Resources

**Key Concepts Demonstrated**:
1. **Data Merging**: Priority-based deduplication strategy
2. **Normalization**: Multi-field standardization techniques
3. **Feature Engineering**: TF-IDF + encoded categorical features
4. **Classification**: Multi-class prediction with imbalanced data
5. **Evaluation**: Comprehensive metrics (accuracy, precision, recall, F1)

**Best Practices Applied**:
- Modular function design (reusable normalization functions)
- Comprehensive error handling (missing data, edge cases)
- Memory-efficient processing (sparse matrices for TF-IDF)
- Clear documentation (docstrings, markdown cells)
- Reproducible results (random_state=42)

---

## 🤝 Contributing

Contributions welcome! Areas for contribution:

### 1. Data Enhancement
- Add new data sources (VietnamWorks, LinkedIn)
- Implement salary data collection
- Add company information scraping

### 2. Model Improvement
- Experiment with advanced NLP models (PhoBERT, BERT)
- Implement deep learning architectures
- Handle class imbalance (SMOTE, class weights)

### 3. Feature Engineering
- Extract tech stacks from descriptions
- Add company size/industry features
- Implement skill taxonomy

### 4. Visualization
- Create interactive dashboards (Plotly, Dash)
- Build geographic heat maps
- Add time-series trend plots

### 5. Documentation
- Improve code comments
- Add usage examples
- Create video tutorials

**Contribution Process**:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 IE313 Final Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full MIT License text...]
```

---

## 📚 Documentation

This project includes comprehensive documentation covering all aspects of the pipeline:

### Core Documentation Files

1. **📖 [README.md](README.md)** (This file)
   - Project overview and quick start guide
   - Complete pipeline description (15 steps)
   - Usage instructions and examples
   - Installation and dependencies

2. **📋 [docs/schema.md](docs/schema.md)**
   - **Master Schema**: Complete 19-column specification
   - **City Normalization**: Reference table strategy and patterns
   - **Salary Fields**: Current status (0% data) and future logic
   - **Data Types**: All columns with examples and validation rules
   - **Design Philosophy**: Forward compatibility and ML-readiness

3. **🗺️ [docs/column_mapping.md](docs/column_mapping.md)**
   - **Kaggle → Master**: Mapping rules with join strategy
   - **GitHub → Master**: Multi-source mapping details
   - **5 Transformation Functions**: City, salary, level, category, skills
   - **Merge Strategy**: Priority-based deduplication (11.7%)
   - **Future Sources**: Guide for adding new data sources

4. **🔄 [docs/pipeline_overview.md](docs/pipeline_overview.md)**
   - **15 Steps as 7 Logical Blocks** (A-G):
     - Block A: Data Ingestion (Load CSV files)
     - Block B: Schema & Mapping (Define + Map columns)
     - Block C: Normalization (5 functions)
     - Block D: Merge & Deduplicate (Priority-based)
     - Block E: Data Quality & Export (Metrics + Files)
     - Block F: EDA (4 visualizations)
     - Block G: ML Pipeline (Feature engineering + XGBoost)
   - **Data Flow Diagram**: ASCII visual representation
   - **Input/Output Specifications**: Each block documented
   - **Deduplication Strategy**: Complete explanation with examples
     - Dedup key: title + company + city (case-insensitive)
     - 528 duplicates removed (11.7%)
     - Priority: Kaggle > GitHub (alphabetical sort)
     - 5 real examples with edge cases
     - 4 future improvement ideas
   - **Extensibility Guide**: How to add new features/sources

5. **🏷️ [docs/categorization_rules.md](docs/categorization_rules.md)**
   - **Job Level Rules** (5 levels):
     - Complete keyword list for each level (intern, junior, mid, senior, manager)
     - Priority order and conflict handling
     - Implementation code with examples
     - Distribution statistics (65.7% mid, 23.3% senior, etc.)
   - **Job Category Rules** (13 categories):
     - Detailed keywords for each category (Backend, Frontend, Fullstack, Mobile, etc.)
     - Priority order (Fullstack → Backend → Frontend → ...)
     - Conflict resolution (6 scenarios documented)
     - 40.5% "Other" (no match) analysis
   - **Testing & Validation**: Test cases with expected outputs
   - **Future Enhancements**: Skills-based, multi-label, confidence scores, ML-based

6. **📍 [data/reference/README.md](data/reference/README.md)**
   - **City/Province Reference Table**: 90+ patterns documented
   - **Normalization Strategy**: 3-step process (pre-process, match, fallback)
   - **Coverage Statistics**: 99.8% normalization rate
   - **Testing Guide**: Test cases and validation
   - **Extension Guide**: How to add new cities/districts

7. **🗂️ [data/reference/city_province_mapping.csv](data/reference/city_province_mapping.csv)**
   - **90+ Location Patterns**: Covers Ha Noi, Ho Chi Minh, Da Nang, etc.
   - **4 Columns**: pattern, city_standard, province_standard, notes
   - **Easy to Extend**: Add new patterns without code changes
   - **Usage**: Loaded by `normalize_city_v2()` function

8. **🤖 [docs/ml_pipeline.md](docs/ml_pipeline.md)**
   - **Complete ML Pipeline**: Steps 11-15 documented in detail
   - **Feature Engineering**: TF-IDF (500 features) + 5 numeric features
   - **Model Training**: Random Forest (69%) vs XGBoost (77%) comparison
   - **Evaluation Metrics**: Accuracy, precision, recall, F1-score per category
   - **Error Analysis**: Common misclassifications and root causes
   - **Planned Improvements** (3 groups):
     - Group 1: Baseline models (Logistic Regression, Linear SVM) + macro metrics
     - Group 2: Class imbalance solutions (undersampling, class weights, SMOTE)
     - Group 3: Feature enhancements (skill count, skill stacks, BERT embeddings)
   - **Success Criteria**: Defined metrics for each improvement
   - **Implementation Roadmap**: 4-phase plan with priorities

9. **📓 [vietnam_it_jobs_merge_analysis.ipynb](vietnam_it_jobs_merge_analysis.ipynb)**
   - **Executable Pipeline**: All 15 steps implemented
   - **Inline Documentation**: Comments and markdown explanations
   - **Code Examples**: Working functions with real data
   - **Visualizations**: 4+ charts with interpretations

### Documentation Coverage

| Topic | Documentation File | Status |
|-------|-------------------|--------|
| Project Overview | README.md | ✅ Complete |
| Master Schema (19 cols) | docs/schema.md | ✅ Complete |
| Column Mapping Rules | docs/column_mapping.md | ✅ Complete |
| Pipeline Flow (15 steps) | docs/pipeline_overview.md | ✅ Complete |
| Categorization Rules | docs/categorization_rules.md | ✅ Complete |
| Deduplication Strategy | docs/pipeline_overview.md (Block D section) | ✅ Complete |
| City Normalization | docs/schema.md + data/reference/README.md | ✅ Complete |
| Salary Strategy | docs/schema.md (Salary Fields section) | ✅ Complete |
| **ML Pipeline (Steps 11-15)** | **docs/ml_pipeline.md** | ✅ Complete |
| Implementation | vietnam_it_jobs_merge_analysis.ipynb | ✅ Complete |
| City Reference Table | data/reference/city_province_mapping.csv | ✅ Complete |

### Quick Navigation

**Want to understand...**
- **Overall project?** → Start with this [README.md](README.md)
- **Data structure?** → Read [docs/schema.md](docs/schema.md)
- **How sources are mapped?** → See [docs/column_mapping.md](docs/column_mapping.md)
- **Pipeline flow?** → Check [docs/pipeline_overview.md](docs/pipeline_overview.md)
- **Categorization rules?** → View [docs/categorization_rules.md](docs/categorization_rules.md)
- **Deduplication strategy?** → See [docs/pipeline_overview.md](docs/pipeline_overview.md#-deduplication-strategy---detailed-explanation)
- **City normalization?** → View [data/reference/README.md](data/reference/README.md)
- **ML pipeline details?** → Read [docs/ml_pipeline.md](docs/ml_pipeline.md)
- **Code implementation?** → Open [vietnam_it_jobs_merge_analysis.ipynb](vietnam_it_jobs_merge_analysis.ipynb)

---

## 👥 Team & Acknowledgments

### Project Team
- **Course**: IE313 - Data Science & Machine Learning
- **Institution**: [Your University Name]
- **Semester**: Fall 2025

### Data Sources
- **Kaggle**: [IT Jobs Dataset](https://www.kaggle.com/halhuynh/it-jobs-dataset) by halhuynh
  - 1,412 ITViec jobs with company information
- **GitHub**: [IT-Job-Posting](https://github.com/SonPhatTranDeveloper/IT-Job-Posting) by SonPhatTranDeveloper
  - 3,101 multi-source jobs (ITViec, LinkedIn, TopCV)

### Technologies & Libraries
- **Python Community**: Incredible open-source libraries
- **Scikit-learn**: Machine learning toolkit
- **XGBoost**: Gradient boosting framework
- **Pandas**: Data manipulation library
- **Jupyter**: Interactive notebook environment

### Special Thanks
- **Vietnamese Tech Community**: Inspiration and support
- **Data Contributors**: For publicly sharing job market datasets
- **Open Source Projects**: For tools and libraries used in this project

---

## 📧 Contact & Support

### Questions or Issues?
- **GitHub Issues**: [Open an issue](https://github.com/duckonthemic/IE313-FinalProject/issues)
- **Email**: [Contact via GitHub profile](https://github.com/duckonthemic)

### Connect
- **GitHub**: [@duckonthemic](https://github.com/duckonthemic)
- **Project Repository**: [IE313-FinalProject](https://github.com/duckonthemic/IE313-FinalProject)

---

## 📊 Project Status

### ✅ Completed Milestones

| Milestone | Status | Completion Date |
|-----------|--------|-----------------|
| Data Collection & Merging | ✅ Complete | Nov 14, 2025 |
| Data Normalization | ✅ Complete | Nov 14, 2025 |
| Feature Engineering | ✅ Complete | Nov 14, 2025 |
| Model Training | ✅ Complete | Nov 14, 2025 |
| Model Evaluation | ✅ Complete | Nov 14, 2025 |
| Documentation | ✅ Complete | Nov 14, 2025 |

### 📈 Project Metrics

- **Total Jobs Analyzed**: 3,985 unique jobs
- **Data Quality**: 100% complete (critical fields)
- **Model Accuracy**: 77.46% (XGBoost)
- **Code Coverage**: 15 pipeline steps documented
- **Visualization**: 4 exploratory charts
- **Documentation**: Comprehensive README + Notebook

### 🎯 Next Phase

- [ ] Deploy as web application (Streamlit dashboard)
- [ ] Add real-time data collection
- [ ] Implement salary prediction model
- [ ] Build job recommendation system

---

## ⭐ Star this Repository!

If you find this project useful for:
- 📚 Learning data science and ML pipelines
- 💼 Understanding Vietnamese IT job market
- 🔧 Reference for data merging techniques
- 📊 Inspiration for similar projects

**Please give it a star ⭐ on GitHub!**

---

## 📅 Version History

### Version 1.0.0 (November 14, 2025)
- ✅ Initial release with complete 15-step pipeline
- ✅ Data merge from Kaggle + GitHub sources
- ✅ XGBoost classification model (77.46% accuracy)
- ✅ Comprehensive documentation and notebook
- ✅ 3,985 unique jobs from Vietnam IT market

### Upcoming (Version 1.1.0)
- 🔜 Web dashboard deployment
- 🔜 Additional data sources
- 🔜 Salary prediction model
- 🔜 API for job search and recommendations

---

**🇻🇳 Made with ❤️ for the Vietnamese Tech Community**

*Last Updated: November 14, 2025*
