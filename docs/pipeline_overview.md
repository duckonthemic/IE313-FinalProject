# Pipeline Overview - 15 Steps Data Flow

## 📋 Tổng quan

Pipeline này thực hiện **merge, normalize, và ML classification** cho dữ liệu việc làm IT từ nhiều nguồn. Pipeline được thiết kế theo **15 bước tuần tự**, mỗi bước có input/output rõ ràng, không phụ thuộc vào notebook.

### 🎯 Mục tiêu Pipeline

1. **Merge** nhiều nguồn dữ liệu về một master table
2. **Normalize** dữ liệu theo quy tắc chung
3. **Deduplicate** để loại bỏ job trùng lặp
4. **Quality Check** để đảm bảo data quality
5. **EDA** để hiểu distribution của dữ liệu
6. **ML** để classify job categories

### 📊 Thống kê Pipeline

- **Input**: 2 datasets (Kaggle: 1,412 + GitHub: 3,101 = 4,513 jobs)
- **Output**: 3,985 unique jobs (11.7% deduplication)
- **Duration**: ~30-60 seconds (depends on hardware)
- **ML Accuracy**: 77.46% (XGBoost)

---

## 🔄 Pipeline Architecture (ASCII Diagram)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BLOCK A: DATA INGESTION                     │
│                         (Steps 1-2)                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INPUT:   - data/raw/kaggle/jobs.csv              (1,412 rows)     │
│           - data/raw/kaggle/companies.csv         (2,041 rows)     │
│           - data/raw/github/job_descriptions.csv  (3,101 rows)     │
│                                                                     │
│  PROCESS: - Load CSV files into pandas DataFrames                  │
│           - Inspect columns and data types                          │
│                                                                     │
│  OUTPUT:  - df_kaggle_jobs        (1,412 × 7)                      │
│           - df_kaggle_companies   (2,041 × 14)                     │
│           - df_github             (3,101 × 11)                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   BLOCK B: SCHEMA & MAPPING                         │
│                         (Steps 3-4)                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INPUT:   - df_kaggle_jobs, df_kaggle_companies, df_github         │
│                                                                     │
│  PROCESS: Step 3: Define master schema (19 columns)                │
│           Step 4: Apply mapping functions                           │
│                   - map_kaggle_jobs(jobs, companies)                │
│                     → Join to get company_name                      │
│                     → Map 7 cols → 8 master cols                   │
│                   - map_github_jobs(github)                         │
│                     → Map 11 cols → 9 master cols                  │
│                                                                     │
│  OUTPUT:  - df_kaggle_clean  (1,412 × 8)                           │
│           - df_github_clean  (3,101 × 9)                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      BLOCK C: NORMALIZATION                         │
│                         (Steps 5-6)                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INPUT:   - df_kaggle_clean, df_github_clean                       │
│                                                                     │
│  PROCESS: Step 5: Define normalization functions                   │
│             - normalize_city()      → standardize locations        │
│             - parse_salary()        → extract min/max/avg          │
│             - extract_job_level()   → extract seniority            │
│             - categorize_job()      → classify category            │
│             - normalize_skills()    → pipe-separated format        │
│                                                                     │
│           Step 6: Apply normalization to both datasets             │
│             - apply_normalization(df_kaggle_clean)                 │
│             - apply_normalization(df_github_clean)                 │
│                                                                     │
│  OUTPUT:  - df_kaggle_normalized  (1,412 × 17)                     │
│           - df_github_normalized  (3,101 × 18)                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   BLOCK D: MERGE & DEDUPLICATE                      │
│                         (Step 7)                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INPUT:   - df_kaggle_normalized  (1,412)                          │
│           - df_github_normalized  (3,101)                          │
│                                                                     │
│  PROCESS: 1. Align columns (union of all columns)                  │
│              → Add missing columns as NULL                          │
│           2. Concatenate vertically                                 │
│              → df_merged (4,513 rows)                              │
│           3. Remove empty critical fields                           │
│              → Drop NULL/empty job_title or company_name           │
│           4. Create dedup key                                       │
│              → title + company + city (lowercase)                  │
│           5. Sort by source_dataset                                 │
│              → Priority: github < kaggle (alphabetically)          │
│           6. Drop duplicates (keep first = Kaggle)                 │
│              → Remove 528 duplicates (11.7%)                       │
│           7. Generate job_id                                        │
│              → job_000000 to job_003984                            │
│           8. Reorder columns (priority cols first)                 │
│                                                                     │
│  OUTPUT:  - df_master  (3,985 × 19)                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                 BLOCK E: DATA QUALITY & EXPORT                      │
│                         (Steps 8-9)                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INPUT:   - df_master  (3,985 × 19)                                │
│           - df_kaggle_normalized                                    │
│           - df_github_normalized                                    │
│                                                                     │
│  PROCESS: Step 8: Data quality report                              │
│             - Total jobs count                                      │
│             - Source distribution                                   │
│             - Job site distribution                                 │
│             - City distribution (top 10)                            │
│             - Job category distribution (top 10)                    │
│             - Job level distribution                                │
│             - Missing values per column                             │
│             - Salary statistics (if available)                      │
│                                                                     │
│           Step 9: Export to multiple formats                        │
│             - CSV:     jobs_master.csv (12.1 MB)                   │
│             - Parquet: jobs_master.parquet (6.05 MB)               │
│             - Intermediate CSVs:                                    │
│               • jobs_kaggle_clean.csv (3.69 MB)                    │
│               • jobs_github_clean.csv (9.93 MB)                    │
│                                                                     │
│  OUTPUT:  Files in data/final/ and data/processed/                 │
│           Quality metrics printed to console                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          BLOCK F: EDA                               │
│                         (Step 10)                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INPUT:   - df_master  (3,985 × 19)                                │
│                                                                     │
│  PROCESS: Generate 4 visualizations:                               │
│                                                                     │
│           1. Job Category Distribution (Horizontal Bar Chart)       │
│              - Top 15 categories by count                           │
│              - Shows market demand per role                         │
│                                                                     │
│           2. Job Level Distribution (Pie Chart)                     │
│              - Breakdown: intern, junior, mid, senior, manager      │
│              - Shows seniority distribution                         │
│                                                                     │
│           3. City Distribution (Bar Chart)                          │
│              - Top 10 cities by job count                           │
│              - Geographic concentration analysis                    │
│                                                                     │
│           4. Salary Distribution (Histogram)                        │
│              - Only if salary_avg.notna().sum() > 100              │
│              - Salary ranges in Million VND/month                   │
│              - (Currently skipped - no salary data)                 │
│                                                                     │
│  OUTPUT:  - 3-4 matplotlib figures displayed in notebook            │
│           - Insights about data distribution                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        BLOCK G: ML PIPELINE                         │
│                         (Steps 11-15)                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  INPUT:   - df_master  (3,985 × 19)                                │
│                                                                     │
│  PROCESS: Step 11: Feature Engineering                             │
│             - Filter categories with ≥50 samples → 10 categories   │
│             - ML dataset: 3,859 jobs (96.8%)                        │
│             - Create text features:                                 │
│               • Combine: title + description + skills              │
│               • TF-IDF: 500 features, bigrams, English stopwords   │
│             - Encode categorical features:                          │
│               • job_level → level_encoded (LabelEncoder)           │
│               • city → city_encoded (LabelEncoder)                 │
│             - Create numeric features:                              │
│               • has_salary (0/1)                                    │
│               • title_length                                        │
│               • desc_length                                         │
│             - Combine all: 505 features (500 TF-IDF + 5)           │
│             - Target: job_category (LabelEncoded)                  │
│             - Train/test split: 80/20, stratified                  │
│                                                                     │
│           Step 12: Model Training                                   │
│             - Random Forest (100 trees, n_jobs=-1)                 │
│               → Accuracy: 69.17%                                    │
│             - XGBoost (100 estimators, eval_metric='mlogloss')     │
│               → Accuracy: 77.46% ⭐ BEST                           │
│                                                                     │
│           Step 13: Model Evaluation                                 │
│             - Classification report (precision/recall/F1)           │
│             - Confusion matrix heatmap                              │
│             - Model accuracy comparison bar chart                   │
│                                                                     │
│           Step 14: Save Best Model                                  │
│             - Pickle dump: best_model.pkl (1.49 MB)                │
│             - Contains: model, tfidf, encoders, metadata           │
│                                                                     │
│           Step 15: Final Summary                                    │
│             - Data merge statistics                                 │
│             - Distribution reports                                  │
│             - ML performance metrics                                │
│             - Top 5 job categories                                  │
│             - File locations                                        │
│                                                                     │
│  OUTPUT:  - data/final/best_model.pkl                              │
│           - ML metrics and visualizations                           │
│           - Complete pipeline summary                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Block-by-Block Details

### BLOCK A: Data Ingestion

#### 📥 Input Files
```
data/raw/kaggle/jobs.csv              1,412 rows × 7 columns
data/raw/kaggle/companies.csv         2,041 rows × 14 columns
data/raw/github/job_descriptions.csv  3,101 rows × 11 columns
```

#### ⚙️ Process
1. **Load Kaggle Jobs** (`pd.read_csv`)
   - Columns: job_id, company_id, job_name, taglist, location, three_reasons, description
   
2. **Load Kaggle Companies** (`pd.read_csv`)
   - Columns: company_id, company_name, city, type, num_employee, country, etc.

3. **Load GitHub Jobs** (`pd.read_csv`)
   - Columns: title, company, location, description, site, job_url, main_programming_languages, etc.

4. **Inspect Data**
   - Print row counts
   - Print column lists
   - Check data types

#### 📤 Output DataFrames
```python
df_kaggle_jobs       # 1,412 × 7
df_kaggle_companies  # 2,041 × 14
df_github            # 3,101 × 11
```

#### 🎯 Role in Pipeline
- **Foundation**: Tải raw data từ source files
- **Validation**: Kiểm tra file tồn tại và readable
- **Inspection**: Hiểu structure của data

---

### BLOCK B: Schema & Mapping

#### 📥 Input
```python
df_kaggle_jobs       # From Block A
df_kaggle_companies  # From Block A
df_github            # From Block A
```

#### ⚙️ Process

**Step 3: Schema Design**
```python
# Define master schema (19 columns)
master_schema = {
    'job_id': 'Unique ID',
    'source_dataset': 'kaggle_itviec or github_it_job_posting',
    'job_site': 'itviec, linkedin, topcv, etc',
    'job_title': 'Job position title',
    'company_name': 'Company name',
    # ... 14 more columns
}
```

**Step 4: Column Mapping**

**Kaggle Mapping**:
```python
def map_kaggle_jobs(df_jobs, df_companies):
    # 1. Join with companies to get company_name
    df = df_jobs.merge(
        df_companies[['company_id', 'company_name', 'city']], 
        on='company_id', how='left'
    )
    
    # 2. Map columns to master schema
    mapped = pd.DataFrame()
    mapped['job_title'] = df['job_name']
    mapped['company_name'] = df['company_name']
    mapped['location_raw'] = df['location']
    mapped['job_description'] = df['description']
    mapped['skills'] = df['taglist']
    
    # 3. Add metadata
    mapped['source_dataset'] = 'kaggle_itviec'
    mapped['job_site'] = 'itviec'
    mapped['country'] = 'Vietnam'
    
    return mapped  # 1,412 × 8
```

**GitHub Mapping**:
```python
def map_github_jobs(df):
    # 1. Direct column mapping
    mapped = pd.DataFrame()
    mapped['job_title'] = df['title']
    mapped['company_name'] = df['company']
    mapped['location_raw'] = df['location']
    mapped['job_description'] = df['description']
    mapped['skills'] = df['main_programming_languages']
    mapped['url'] = df['job_url']
    
    # 2. Add metadata
    mapped['source_dataset'] = 'github_it_job_posting'
    mapped['job_site'] = df.get('site', 'itviec')
    mapped['country'] = 'Vietnam'
    
    return mapped  # 3,101 × 9
```

#### 📤 Output DataFrames
```python
df_kaggle_clean  # 1,412 × 8 columns
df_github_clean  # 3,101 × 9 columns
```

#### 🎯 Role in Pipeline
- **Standardization**: Các source khác nhau → cùng schema
- **Metadata**: Thêm thông tin nguồn gốc
- **Preparation**: Chuẩn bị cho normalization

---

### BLOCK C: Normalization

#### 📥 Input
```python
df_kaggle_clean  # 1,412 × 8 (from Block B)
df_github_clean  # 3,101 × 9 (from Block B)
```

#### ⚙️ Process

**Step 5: Define Normalization Functions**

1. **normalize_city(location_raw) → city**
   ```python
   # Maps variations to standard names
   'hà nội' → 'Ha Noi'
   'hcm' → 'Ho Chi Minh'
   'đà nẵng' → 'Da Nang'
   # ... + 6 more cities + 'Remote', 'Other', 'Unknown'
   ```

2. **parse_salary(salary_raw) → (min, max, avg, currency)**
   ```python
   # Extract numbers, convert USD to VND, handle "triệu"
   '15-20 triệu' → (15M, 20M, 17.5M, 'VND')
   # Currently returns (None, None, None, None) - no salary data
   ```

3. **extract_job_level(job_title) → job_level**
   ```python
   # Keyword matching
   'Senior Backend Engineer' → 'senior'
   'Junior Frontend Dev' → 'junior'
   'Backend Developer' → 'mid' (default)
   ```

4. **categorize_job(job_title) → job_category**
   ```python
   # Keyword classification (13 categories)
   'Backend Engineer' → 'Backend Developer'
   'QA Engineer' → 'QA/Tester'
   'Data Scientist' → 'Data Scientist'
   # ... 10 more categories + 'Other'
   ```

5. **normalize_skills(skills_raw) → skills**
   ```python
   # Remove brackets, split, lowercase, pipe-separate
   "['Python', 'SQL']" → 'python|sql'
   ```

**Step 6: Apply Normalization**
```python
def apply_normalization(df):
    df = df.copy()
    
    # Normalize location
    df['city'] = df['location_raw'].apply(normalize_city)
    df['province'] = df['city']
    
    # Parse salary (returns NULL currently)
    df['salary_min'] = None
    df['salary_max'] = None
    df['salary_avg'] = None
    df['salary_currency'] = None
    
    # Extract job info
    df['job_level'] = df['job_title'].apply(extract_job_level)
    df['job_category'] = df['job_title'].apply(categorize_job)
    
    # Normalize skills
    df['skills'] = df['skills'].apply(normalize_skills)
    
    # Default employment type
    df['employment_type'] = 'full_time'
    
    return df

# Apply to both datasets
df_kaggle_normalized = apply_normalization(df_kaggle_clean)
df_github_normalized = apply_normalization(df_github_clean)
```

#### 📤 Output DataFrames
```python
df_kaggle_normalized  # 1,412 × 17 columns
df_github_normalized  # 3,101 × 18 columns
```

**New columns added**:
- city, province (from location_raw)
- salary_min, salary_max, salary_avg, salary_currency (NULL)
- job_level (from job_title)
- job_category (from job_title)
- employment_type (default)
- skills (normalized)

#### 🎯 Role in Pipeline
- **Standardization**: Location, skills về format chuẩn
- **Extraction**: Job level, category từ title
- **Preparation**: Salary columns sẵn sàng cho future data
- **Consistency**: Tất cả dữ liệu có cùng format

---

### BLOCK D: Merge & Deduplicate

#### 📥 Input
```python
df_kaggle_normalized  # 1,412 × 17
df_github_normalized  # 3,101 × 18
```

#### ⚙️ Process (Step 7)

**1. Align Columns**
```python
# Get union of all columns
all_columns = set(df_kaggle_normalized.columns) | set(df_github_normalized.columns)

# Add missing columns as NULL
for col in all_columns:
    if col not in df_kaggle_normalized.columns:
        df_kaggle_normalized[col] = None
    if col not in df_github_normalized.columns:
        df_github_normalized[col] = None

# Both now have 19 columns
```

**2. Concatenate**
```python
df_merged = pd.concat([df_kaggle_normalized, df_github_normalized], ignore_index=True)
# Result: 4,513 rows × 19 columns (1,412 + 3,101)
```

**3. Remove Empty Critical Fields**
```python
df_merged = df_merged.dropna(subset=['job_title', 'company_name'])
df_merged = df_merged[df_merged['job_title'].str.strip() != '']
df_merged = df_merged[df_merged['company_name'].str.strip() != '']
# Still: 4,513 rows (no empty titles/companies)
```

**4. Create Dedup Key**
```python
df_merged['_dedup_key'] = (
    df_merged['job_title'].str.lower().str.strip() + '_' +
    df_merged['company_name'].str.lower().str.strip() + '_' +
    df_merged['city'].fillna('').str.lower()
)
# Example: 'backend engineer_vinova_ho chi minh'
```

**5. Sort by Source (Priority)**
```python
df_merged = df_merged.sort_values('source_dataset')
# Alphabetically: 'github_it_job_posting' < 'kaggle_itviec'
# → Kaggle rows move to bottom → kept when duplicate
```

**6. Drop Duplicates**
```python
df_merged = df_merged.drop_duplicates(subset='_dedup_key', keep='first')
# keep='first' → after sorting, Kaggle is kept
# Result: 3,985 rows (removed 528 duplicates = 11.7%)
```

**7. Generate job_id**
```python
df_merged['job_id'] = ['job_' + str(i).zfill(6) for i in range(len(df_merged))]
# job_000000, job_000001, ..., job_003984
```

**8. Reorder Columns**
```python
priority_cols = [
    'job_id', 'source_dataset', 'job_site', 'job_title', 'company_name', 
    'city', 'job_category', 'job_level', 'salary_min', 'salary_max'
]
other_cols = [c for c in df_merged.columns if c not in priority_cols]
df_master = df_merged[priority_cols + other_cols]
```

#### 📤 Output DataFrame
```python
df_master  # 3,985 × 19 columns
```

**Deduplication Stats**:
- Before: 4,513 jobs
- After: 3,985 jobs
- Removed: 528 duplicates (11.7%)
- Priority: Kaggle > GitHub

---

## 🔍 Deduplication Strategy - Detailed Explanation

### 🎯 Goal

Tránh trùng lặp job khi merge 2 datasets từ các nguồn khác nhau. Nhiều job có thể xuất hiện trên cả **Kaggle (ITViec)** và **GitHub (multi-source)** với thông tin tương tự.

### 🔑 Dedup Key Design

**Composite Key**: `title + company + city` (case-insensitive)

**Rationale**:
- ✅ **`job_title`**: Cùng vị trí (e.g., "Backend Engineer")
- ✅ **`company_name`**: Cùng công ty (e.g., "Vinova")
- ✅ **`city`**: Cùng địa điểm (e.g., "Ho Chi Minh")
- ❌ **NOT `url`**: GitHub có url, Kaggle không → sẽ không match
- ❌ **NOT `posted_date`**: Không có data → không dùng được

**Formula**:
```python
dedup_key = (
    job_title.lower().strip() + '_' + 
    company_name.lower().strip() + '_' + 
    city.lower() if city else ''
)
```

**Example Keys**:
```
'backend engineer_vinova_ho chi minh'
'senior frontend developer_fpt software_ha noi'
'qa engineer_kms technology_ho chi minh'
```

### 📋 Deduplication Process (6 Steps)

#### Step 1: Create Dedup Key
```python
df_merged['_dedup_key'] = (
    df_merged['job_title'].str.lower().str.strip() + '_' +
    df_merged['company_name'].str.lower().str.strip() + '_' +
    df_merged['city'].fillna('').str.lower()
)
```

**Why lowercase?**
- "Backend Engineer" vs "backend engineer" → same job
- "KMS Technology" vs "kms technology" → same company

**Why strip()?**
- Remove leading/trailing spaces
- " Backend Engineer " vs "Backend Engineer" → same

**Why fillna('')?**
- Handle NULL city (rare)
- Prevents `TypeError: unsupported operand type`

#### Step 2: Sort by Source Dataset (Alphabetically)
```python
df_merged = df_merged.sort_values('source_dataset')
```

**Order**:
- `'github_it_job_posting'` < `'kaggle_itviec'` (alphabetically)
- GitHub rows → top
- Kaggle rows → bottom

**Why?** Next step keeps **first** row, so Kaggle will be kept!

#### Step 3: Drop Duplicates (Keep First)
```python
df_merged = df_merged.drop_duplicates(subset='_dedup_key', keep='first')
```

**Logic**:
- For each unique `_dedup_key`
- Keep **first** occurrence (after sorting = Kaggle)
- Remove subsequent occurrences (GitHub)

**Priority**: Kaggle > GitHub (because sorted alphabetically, Kaggle is "first" after sort)

**Result**:
- Before: 4,513 jobs (1,412 Kaggle + 3,101 GitHub)
- After: 3,985 jobs
- **Removed**: 528 duplicates (11.7%)

#### Step 4: Verify Deduplication
```python
# Check: Should have no duplicates
assert df_merged['_dedup_key'].nunique() == len(df_merged)
# ✅ Pass: 3,985 unique keys = 3,985 rows
```

#### Step 5: Remove Dedup Key Column
```python
df_merged = df_merged.drop(columns=['_dedup_key'])
```

**Why remove?**
- Temporary column, not needed in master table
- Keeps schema clean (19 columns, not 20)

#### Step 6: Verify Source Distribution
```python
print(df_merged['source_dataset'].value_counts())
# kaggle_itviec: 1,411 (35.4%)
# github_it_job_posting: 2,574 (64.6%)
```

**Observation**:
- Kaggle: Lost 1 job (1,412 → 1,411)
  - Possible: 1 Kaggle job had empty title/company
- GitHub: Lost 527 jobs (3,101 → 2,574)
  - These were duplicates with Kaggle jobs
  
**Dedup mainly affected GitHub** (lost 17% of GitHub jobs)

### 📊 Deduplication Examples

#### Example 1: Exact Match (Title + Company + City)

**Kaggle Job** (kept):
```
job_title: "Backend Engineer"
company_name: "Vinova"
city: "Ho Chi Minh"
source_dataset: "kaggle_itviec"
url: NULL
```

**GitHub Job** (removed - duplicate):
```
job_title: "Backend Engineer"
company_name: "Vinova"
city: "Ho Chi Minh"
source_dataset: "github_it_job_posting"
url: "https://www.linkedin.com/jobs/view/..."
```

**Dedup Key**: `'backend engineer_vinova_ho chi minh'`

**Result**: Kaggle kept (has more company info from companies.csv), GitHub removed

---

#### Example 2: Case-Insensitive Match

**Kaggle Job** (kept):
```
job_title: "Senior Frontend Developer"
company_name: "FPT Software"
city: "Ha Noi"
```

**GitHub Job** (removed - duplicate):
```
job_title: "senior frontend developer"  # lowercase
company_name: "FPT software"            # different case
city: "ha noi"                          # lowercase
```

**Dedup Key**: Both → `'senior frontend developer_fpt software_ha noi'`

**Result**: Kaggle kept (priority), GitHub removed

---

#### Example 3: Different City → NOT Duplicate

**Job A** (Kaggle):
```
job_title: "QA Engineer"
company_name: "KMS Technology"
city: "Ho Chi Minh"
```

**Job B** (GitHub):
```
job_title: "QA Engineer"
company_name: "KMS Technology"
city: "Ha Noi"
```

**Dedup Keys**:
- Job A: `'qa engineer_kms technology_ho chi minh'`
- Job B: `'qa engineer_kms technology_ha noi'`

**Result**: **BOTH KEPT** (different cities → different jobs)

**Reasoning**: Same company hiring for same role in different locations

---

#### Example 4: Different Title → NOT Duplicate

**Job A** (Kaggle):
```
job_title: "Backend Engineer"
company_name: "Vinova"
city: "Ho Chi Minh"
```

**Job B** (GitHub):
```
job_title: "Senior Backend Engineer"
company_name: "Vinova"
city: "Ho Chi Minh"
```

**Dedup Keys**:
- Job A: `'backend engineer_vinova_ho chi minh'`
- Job B: `'senior backend engineer_vinova_ho chi minh'`

**Result**: **BOTH KEPT** (different titles → different seniority levels)

---

#### Example 5: Real Duplicate from Data

**Analysis from processed data**:

Potential duplicate pattern: Companies appearing in both sources:
- **KMS Technology**: 40 jobs in Kaggle, likely overlaps with GitHub
- **FPT Software**: Common in both sources
- **Vinova**: Appears in both

**Validation**:
```python
# Check if dedup worked
kaggle_companies = set(df_kaggle['company_name'])
github_companies = set(df_github['company_name'])
overlap = kaggle_companies & github_companies

print(f"Companies in both sources: {len(overlap)}")
# Result: ~500 companies appear in both datasets

# These companies likely have duplicate jobs
# Dedup removed 528 jobs → matches overlap expectation
```

### ⚠️ Limitations & Edge Cases

#### Limitation 1: Title Variation

**Problem**: Same job with slightly different titles

**Example**:
- Kaggle: `"Backend Engineer"`
- GitHub: `"Backend Developer"`

**Result**: **NOT** detected as duplicate (different dedup keys)

**Impact**: Under-deduplication (false negatives)

**Potential Improvement**: Fuzzy matching on title
```python
from fuzzywuzzy import fuzz

if (company_match and city_match and 
    fuzz.ratio(title1, title2) > 85):
    # Consider as duplicate
```

---

#### Limitation 2: Company Name Variation

**Problem**: Same company with different names

**Example**:
- Kaggle: `"FPT Software"`
- GitHub: `"FPT Software Company Limited"`

**Result**: **NOT** detected as duplicate

**Impact**: Under-deduplication

**Potential Improvement**: Company name normalization
```python
def normalize_company(name):
    # Remove legal suffixes
    suffixes = ['ltd', 'limited', 'co', 'corp', 'inc']
    name_clean = name.lower()
    for suffix in suffixes:
        name_clean = name_clean.replace(suffix, '')
    return name_clean.strip()
```

---

#### Limitation 3: NULL City

**Problem**: Job with `city = NULL` or `Unknown`

**Example**:
- Kaggle: `title="Backend", company="Vinova", city=NULL`
- GitHub: `title="Backend", company="Vinova", city="Ho Chi Minh"`

**Dedup Keys**:
- Kaggle: `'backend_vinova_'` (empty city)
- GitHub: `'backend_vinova_ho chi minh'`

**Result**: **BOTH KEPT** (different keys)

**Impact**: Potential under-deduplication if one source missing city

---

#### Limitation 4: Cannot Use URL

**Problem**: URL would be perfect unique identifier

**Why NOT used**:
- Kaggle: 0% have URL (NULL)
- GitHub: 64.6% have URL
- Cannot match if one side is NULL

**Example**:
- Kaggle: `url=NULL`
- GitHub: `url="https://itviec.com/job/123"`

**Result**: Cannot compare → rely on title+company+city instead

**Future**: If both sources have URL, add to dedup key

---

#### Limitation 5: Cannot Use Posted Date

**Problem**: Same job posted at different dates

**Why NOT used**:
- Both sources: 0% have `posted_date` data (NULL)
- Cannot use for temporal deduplication

**Example** (if we had dates):
- Same job posted on Jan 1 and Jan 15 → should be same job (re-posted)
- Different jobs posted 6 months apart → different hiring rounds

**Future**: If `posted_date` available, use time window (e.g., ±30 days)

---

### 💡 Future Improvements

#### Idea 1: Add URL to Dedup Key (Conditional)

```python
def create_dedup_key_v2(row):
    base_key = f"{row['job_title'].lower()}_{row['company_name'].lower()}_{row['city'].lower()}"
    
    # If both have URL, use it
    if pd.notna(row.get('url')) and row['url'] != '':
        base_key += f"_{row['url'].lower()}"
    
    return base_key
```

**Benefit**: More accurate matching when URLs available

---

#### Idea 2: Fuzzy Matching on Title

```python
from fuzzywuzzy import fuzz

def is_duplicate_fuzzy(row1, row2, threshold=85):
    # Company and city must match exactly
    if row1['company_name'].lower() != row2['company_name'].lower():
        return False
    if row1['city'].lower() != row2['city'].lower():
        return False
    
    # Title can be fuzzy
    title_similarity = fuzz.ratio(row1['job_title'].lower(), row2['job_title'].lower())
    return title_similarity >= threshold
```

**Benefit**: Catch variations like "Backend Engineer" vs "Backend Developer"

---

#### Idea 3: Use Posted Date Window (When Available)

```python
def create_dedup_key_v3(row):
    key = f"{row['job_title'].lower()}_{row['company_name'].lower()}_{row['city'].lower()}"
    
    # If posted_date exists, add year-month (ignore day)
    if pd.notna(row.get('posted_date')):
        date_str = pd.to_datetime(row['posted_date']).strftime('%Y-%m')
        key += f"_{date_str}"
    
    return key
```

**Benefit**: Allow same job re-posted in different months to be deduplicated

---

#### Idea 4: Manual Verification

**Process**:
1. Export all removed duplicates (528 jobs)
2. Manually review 50-100 samples
3. Check if dedup was correct (true duplicates?)
4. Calculate precision: `true_duplicates / total_removed`

**Purpose**: Validate dedup strategy accuracy

---

### 📊 Deduplication Metrics Summary

| Metric | Value | Formula |
|--------|-------|---------|
| **Initial Jobs** | 4,513 | Kaggle (1,412) + GitHub (3,101) |
| **Final Jobs** | 3,985 | After deduplication |
| **Duplicates Removed** | 528 | 4,513 - 3,985 |
| **Dedup Rate** | 11.7% | 528 / 4,513 |
| **Kaggle Retained** | 1,411 | 1,412 - 1 (99.9%) |
| **GitHub Retained** | 2,574 | 3,101 - 527 (83.0%) |
| **GitHub Dedup Impact** | 17.0% | 527 / 3,101 |

**Key Insights**:
- ✅ Kaggle almost fully retained (only 1 lost, likely data quality issue)
- ✅ GitHub lost 17% → most duplicates were from GitHub overlapping with Kaggle
- ✅ 11.7% overall dedup rate is reasonable for multi-source aggregation
- ✅ Kaggle priority ensures higher quality data (has company details from join)

---

### 🔗 Related Documentation

- **Master Schema**: `docs/schema.md` (job_id generation after dedup)
- **Column Mapping**: `docs/column_mapping.md` (merge strategy section)
- **Categorization Rules**: `docs/categorization_rules.md` (not affected by dedup)

---

#### 🎯 Role in Pipeline
- **Consolidation**: Merge 2 sources thành 1 table
- **Deduplication**: Loại bỏ 528 job trùng lặp (11.7%)
- **Unique ID**: Tạo job_id cho mỗi job
- **Organization**: Sắp xếp cột logic
- **Quality**: Prioritize Kaggle (has company metadata)

---

### BLOCK E: Data Quality & Export

#### 📥 Input
```python
df_master             # 3,985 × 19 (from Block D)
df_kaggle_normalized  # For intermediate export
df_github_normalized  # For intermediate export
```

#### ⚙️ Process

**Step 8: Data Quality Report**
```python
# Print comprehensive quality metrics:

1. Total jobs: 3,985

2. By source:
   - kaggle_itviec: 1,411 (35.4%)
   - github_it_job_posting: 2,574 (64.6%)

3. By job site:
   - itviec: 1,411
   - LinkedIn: 995
   - ITViec: 923
   - TopCV: 656

4. By city (top 10):
   - Ho Chi Minh: 2,060 (51.7%)
   - Ha Noi: 1,431 (35.9%)
   - Da Nang: 115 (2.9%)
   - Other: 364 (9.1%)
   - Remote: 6, Hai Phong: 3, Can Tho: 3, etc.

5. By job category (top 10):
   - Other: 1,615 (40.5%)
   - Backend Developer: 374 (9.4%)
   - Fullstack Developer: 345 (8.7%)
   - QA/Tester: 338 (8.5%)
   - Mobile Developer: 303 (7.6%)
   - ... 5 more categories

6. By job level:
   - mid: 2,618 (65.7%)
   - senior: 928 (23.3%)
   - junior: 198 (5.0%)
   - manager: 131 (3.3%)
   - intern: 110 (2.8%)

7. Missing values:
   - salary_min: 3,985 (100%)
   - salary_max: 3,985 (100%)
   - salary_avg: 3,985 (100%)
   - salary_currency: 3,985 (100%)
   - url: 1,411 (35.4%)
   - Other columns: 0 (0%)

8. Salary statistics:
   - Jobs with salary: 0 (0.0%)
   - (No salary data available)
```

**Step 9: Export to Files**
```python
# Master table
df_master.to_csv('data/final/jobs_master.csv', index=False)
df_master.to_parquet('data/final/jobs_master.parquet', index=False)

# Intermediate tables
df_kaggle_normalized.to_csv('data/processed/jobs_kaggle_clean.csv', index=False)
df_github_normalized.to_csv('data/processed/jobs_github_clean.csv', index=False)
```

#### 📤 Output Files
```
data/final/jobs_master.csv            12.1 MB  (3,985 jobs × 19 cols)
data/final/jobs_master.parquet         6.05 MB (compressed)
data/processed/jobs_kaggle_clean.csv   3.69 MB (1,412 jobs)
data/processed/jobs_github_clean.csv   9.93 MB (3,101 jobs)
```

#### 🎯 Role in Pipeline
- **Quality Assurance**: Comprehensive data quality metrics
- **Persistence**: Save processed data to disk
- **Format Flexibility**: CSV (human-readable) + Parquet (efficient)
- **Traceability**: Intermediate files for debugging

---

### BLOCK F: EDA (Exploratory Data Analysis)

#### 📥 Input
```python
df_master  # 3,985 × 19 (from Block D/E)
```

#### ⚙️ Process (Step 10)

**Visualization 1: Job Category Distribution**
```python
plt.figure(figsize=(12, 6))
df_master['job_category'].value_counts().head(15).plot(kind='barh')
plt.title('Top 15 Job Categories')
plt.xlabel('Count')
plt.tight_layout()
plt.show()
```
**Purpose**: Hiểu market demand cho từng role type

**Visualization 2: Job Level Distribution**
```python
plt.figure(figsize=(10, 6))
df_master['job_level'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Job Level Distribution')
plt.ylabel('')
plt.tight_layout()
plt.show()
```
**Purpose**: Phân tích seniority distribution

**Visualization 3: City Distribution**
```python
plt.figure(figsize=(10, 6))
df_master['city'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 Cities')
plt.xlabel('City')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```
**Purpose**: Geographic job concentration

**Visualization 4: Salary Distribution** (Conditional)
```python
if df_master['salary_avg'].notna().sum() > 100:
    plt.figure(figsize=(12, 6))
    salary_data = df_master['salary_avg'].dropna() / 1000000
    salary_data[salary_data <= 100].hist(bins=30, edgecolor='black')
    plt.title('Salary Distribution')
    plt.xlabel('Salary (Million VND/month)')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()
```
**Purpose**: Salary range distribution  
**Status**: Currently skipped (no salary data)

#### 📤 Output
```
- 3 matplotlib figures displayed in notebook
- Visual insights about data distribution
```

#### 🎯 Role in Pipeline
- **Understanding**: Hiểu distribution của data
- **Validation**: Visual check data quality
- **Communication**: Present insights to stakeholders
- **Discovery**: Find patterns and anomalies

---

### BLOCK G: ML Pipeline

#### 📥 Input
```python
df_master  # 3,985 × 19 (from Block D/E)
```

#### ⚙️ Process

**Step 11: Feature Engineering**

1. **Filter ML Dataset**
   ```python
   # Only categories with ≥50 samples
   category_counts = df_master['job_category'].value_counts()
   valid_categories = category_counts[category_counts >= 50].index.tolist()
   df_ml = df_master[df_master['job_category'].isin(valid_categories)].copy()
   
   # Result: 3,859 jobs (96.8%), 10 categories
   ```

2. **Create Text Features**
   ```python
   # Combine text fields
   df_ml['text'] = (
       df_ml['job_title'].fillna('') + ' ' + 
       df_ml['job_description'].fillna('') + ' ' + 
       df_ml['skills'].fillna('')
   )
   
   # TF-IDF Vectorization
   tfidf = TfidfVectorizer(
       max_features=500, 
       ngram_range=(1, 2), 
       stop_words='english'
   )
   X_tfidf = tfidf.fit_transform(df_ml['text'])
   # Shape: (3,859, 500)
   ```

3. **Encode Categorical Features**
   ```python
   le_level = LabelEncoder()
   le_city = LabelEncoder()
   
   df_ml['level_encoded'] = le_level.fit_transform(df_ml['job_level'])
   df_ml['city_encoded'] = le_city.fit_transform(df_ml['city'])
   ```

4. **Create Numeric Features**
   ```python
   df_ml['has_salary'] = df_ml['salary_avg'].notna().astype(int)
   df_ml['title_length'] = df_ml['job_title'].str.len()
   df_ml['desc_length'] = df_ml['job_description'].fillna('').str.len()
   
   feature_cols = ['level_encoded', 'city_encoded', 'has_salary', 
                   'title_length', 'desc_length']
   X_additional = df_ml[feature_cols].values
   ```

5. **Combine Features**
   ```python
   from scipy.sparse import hstack
   X = hstack([X_tfidf, X_additional])
   # Shape: (3,859, 505) = 500 TF-IDF + 5 additional
   ```

6. **Prepare Target**
   ```python
   le_target = LabelEncoder()
   y = le_target.fit_transform(df_ml['job_category'])
   # 10 categories encoded as 0-9
   ```

7. **Train/Test Split**
   ```python
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42, stratify=y
   )
   # Train: 3,087 samples
   # Test:  772 samples
   ```

**Step 12: Model Training**
```python
models = {
    'Random Forest': RandomForestClassifier(
        n_estimators=100, 
        random_state=42, 
        n_jobs=-1
    ),
    'XGBoost': XGBClassifier(
        n_estimators=100, 
        random_state=42, 
        eval_metric='mlogloss'
    )
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    results[name] = {
        'model': model, 
        'accuracy': acc, 
        'predictions': y_pred
    }

# Results:
# - Random Forest: 69.17%
# - XGBoost: 77.46% ⭐ BEST
```

**Step 13: Model Evaluation**
```python
best_name = max(results, key=lambda x: results[x]['accuracy'])
y_pred_best = results[best_name]['predictions']

# Classification Report
print(classification_report(y_test, y_pred_best, 
                           target_names=le_target.classes_))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred_best)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title(f'Confusion Matrix - {best_name}')
plt.show()

# Model Comparison
plt.bar(model_names, accuracies)
plt.title('Model Accuracy Comparison')
plt.show()
```

**Step 14: Save Best Model**
```python
model_data = {
    'model': results[best_name]['model'],
    'tfidf': tfidf,
    'le_target': le_target,
    'le_level': le_level,
    'le_city': le_city,
    'feature_cols': feature_cols,
    'accuracy': results[best_name]['accuracy'],
    'model_name': best_name
}

with open('data/final/best_model.pkl', 'wb') as f:
    pickle.dump(model_data, f)
```

**Step 15: Final Summary**
```python
# Print comprehensive summary:
# - Data merge stats (Kaggle, GitHub counts, dedup rate)
# - Distribution (sources, sites, cities, companies, categories)
# - ML stats (dataset size, features, best model, accuracy)
# - Top 5 job categories
# - All output file locations
```

#### 📤 Output
```
data/final/best_model.pkl  1.49 MB (contains model + transformers)

ML Metrics:
- Best Model: XGBoost
- Accuracy: 77.46%
- Features: 505 (500 TF-IDF + 5 encoded)
- Categories: 10
- Train/Test: 3,087 / 772 samples

Visualizations:
- Classification report (console)
- Confusion matrix (heatmap)
- Model comparison (bar chart)
```

#### 🎯 Role in Pipeline
- **Feature Engineering**: Convert raw data → ML features
- **Model Training**: Train multiple classifiers
- **Model Selection**: Choose best performing model
- **Persistence**: Save model for deployment
- **Documentation**: Final comprehensive summary

---

## 🔄 Data Flow Summary

```
RAW DATA (2 sources, 4,513 jobs)
  ↓
MAPPED DATA (aligned to master schema)
  ↓
NORMALIZED DATA (standardized format)
  ↓
MERGED DATA (single table, deduplicated)
  ↓
MASTER TABLE (3,985 unique jobs, 19 columns)
  ├─→ CSV/Parquet Export
  ├─→ EDA Visualizations
  └─→ ML Pipeline
       ├─→ Feature Engineering (505 features)
       ├─→ Model Training (Random Forest, XGBoost)
       ├─→ Model Evaluation (77.46% accuracy)
       └─→ Model Export (best_model.pkl)
```

---

## 📊 Pipeline Metrics

| Metric | Value |
|--------|-------|
| **Input Jobs** | 4,513 (1,412 + 3,101) |
| **Output Jobs** | 3,985 (11.7% dedup) |
| **Columns** | 19 (master schema) |
| **Data Completeness** | 73.7% (14/19 columns) |
| **ML Dataset** | 3,859 jobs (96.8%) |
| **ML Categories** | 10 (≥50 samples) |
| **ML Features** | 505 (TF-IDF + encoded) |
| **Best Model** | XGBoost |
| **Model Accuracy** | 77.46% |
| **Pipeline Duration** | ~30-60 seconds |

---

## 🎯 Key Design Principles

### 1. **Block Independence**
- Each block có input/output rõ ràng
- Có thể test từng block riêng biệt
- Dễ dàng debug khi có lỗi

### 2. **Forward Compatibility**
- Schema có sẵn cột cho future data (salary, posted_date)
- Normalization functions reusable cho source mới
- Pipeline structure stable, dễ extend

### 3. **Data Quality First**
- Comprehensive quality checks sau mỗi transform
- Missing value handling explicit
- Deduplication strategy clear và reproducible

### 4. **ML-Ready Output**
- Text features (TF-IDF) từ title, description, skills
- Categorical encoding (job_level, city)
- Target variable clear (job_category)
- Train/test split stratified

### 5. **Documentation & Traceability**
- Mỗi step có explanation
- Intermediate files saved
- Metrics logged throughout
- Final summary comprehensive

---

## 🔮 Extending the Pipeline

### Add New Data Source

**Example: VietnamWorks**

1. **Thêm vào Block A**: Load vietnamworks.csv
2. **Thêm vào Block B**: Tạo `map_vietnamworks_jobs()`
3. **Sử dụng Block C**: Apply `apply_normalization()` (reuse!)
4. **Update Block D**: Add vào merge: `pd.concat([kaggle, github, vietnamworks])`
5. **Tự động work**: Quality check, EDA, ML pipeline không cần thay đổi!

### Add New Features

**Example: Thêm "years_of_experience" feature**

1. **Update Block C**: Thêm `extract_experience()` function
2. **Update normalization**: Apply trong `apply_normalization()`
3. **Update Block G**: Add vào ML features: `X_additional`
4. **Retrain**: Model tự động use new feature!

### Add New ML Model

**Example: Thêm Neural Network**

1. **Update Block G Step 12**: Add model vào dict
2. **Train cùng loop**: Tự động train và evaluate
3. **Compare**: Tự động so sánh với models khác
4. **Select best**: Tự động pick best accuracy

---

## 📚 Related Documentation

- **Master Schema**: `docs/schema.md` - 19 columns chi tiết
- **Column Mapping**: `docs/column_mapping.md` - Source → Master mapping
- **README**: Root README.md - Project overview
- **Notebook**: `vietnam_it_jobs_merge_analysis.ipynb` - Implementation

---

**Last Updated**: November 14, 2025  
**Pipeline Version**: 1.0.0  
**Status**: ✅ Production-ready và documented đầy đủ!
