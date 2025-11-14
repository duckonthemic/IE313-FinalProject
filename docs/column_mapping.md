# Column Mapping Documentation

## 📋 Tổng quan

Tài liệu này mô tả chi tiết **"hợp đồng" mapping** giữa các cột từ **source datasets** (Kaggle, GitHub) và **master schema** (19 cột thống nhất).

### 🎯 Mục đích

- **Traceability**: Biết mỗi cột master đến từ đâu
- **Consistency**: Đảm bảo mapping nhất quán khi thêm source mới
- **Documentation**: Reference cho development và debugging
- **Validation**: Kiểm tra data quality từ source

---

## 📊 Mapping Overview

| Master Column | Kaggle Source | GitHub Source | Mapping Type |
|---------------|---------------|---------------|--------------|
| job_id | N/A (Generated) | N/A (Generated) | Auto-generated |
| source_dataset | Metadata | Metadata | Constant |
| job_site | Constant | site column | Direct/Constant |
| job_title | job_name | title | Direct |
| company_name | company_name (joined) | company | Direct/Join |
| location_raw | location | location | Direct |
| city | location → normalized | location → normalized | Computed |
| province | city | city | Computed |
| country | Constant | Constant | Constant |
| salary_min | N/A | N/A | Not available |
| salary_max | N/A | N/A | Not available |
| salary_avg | N/A | N/A | Not available |
| salary_currency | N/A | N/A | Not available |
| job_level | job_name → extracted | title → extracted | Computed |
| job_category | job_name → classified | title → classified | Computed |
| employment_type | Default | Default | Constant |
| skills | taglist → normalized | main_programming_languages → normalized | Direct + Transform |
| job_description | description | description | Direct |
| url | N/A | job_url | Direct |
| posted_date | N/A | N/A | Not available |

---

## 🔷 Mapping chi tiết: Kaggle → Master Schema

### 📂 Source Files

- **jobs.csv**: 1,412 rows, 7 columns
  - Columns: `job_id`, `company_id`, `job_name`, `taglist`, `location`, `three_reasons`, `description`
  
- **companies.csv**: 2,041 rows, 14 columns
  - Columns: `company_id`, `company_name`, `average_rating`, `num_review`, `city`, `type`, `num_employee`, `country`, `working_day`, `OT`, `overview`, `expertise`, `benifit`, `logo_link`

### 🔗 Join Strategy

```python
# Merge jobs with companies to get company information
df_merged = df_jobs.merge(
    df_companies[['company_id', 'company_name', 'city']], 
    on='company_id', 
    how='left'
)
```

### 📋 Column Mapping Table

| Master Column | Source Column(s) | Mapping Logic | Example |
|---------------|------------------|---------------|---------|
| **job_id** | N/A | `'job_' + str(i).zfill(6)` | `job_000000` |
| **source_dataset** | N/A | Constant: `'kaggle_itviec'` | `kaggle_itviec` |
| **job_site** | N/A | Constant: `'itviec'` | `itviec` |
| **job_title** | `jobs.job_name` | Direct copy | `QA Engineer` |
| **company_name** | `companies.company_name` | Join via company_id | `Hubble Pte. Ltd` |
| **location_raw** | `jobs.location` | Direct copy | `Hồ Chí Minh` |
| **city** | `jobs.location` | Normalize via `normalize_city()` | `Ho Chi Minh` |
| **province** | city | Copy from city | `Ho Chi Minh` |
| **country** | N/A | Constant: `'Vietnam'` | `Vietnam` |
| **salary_min** | N/A | NULL | `None` |
| **salary_max** | N/A | NULL | `None` |
| **salary_avg** | N/A | NULL | `None` |
| **salary_currency** | N/A | NULL | `None` |
| **job_level** | `jobs.job_name` | Extract via `extract_job_level()` | `mid` |
| **job_category** | `jobs.job_name` | Classify via `categorize_job()` | `QA/Tester` |
| **employment_type** | N/A | Default: `'full_time'` | `full_time` |
| **skills** | `jobs.taglist` | Normalize via `normalize_skills()` | `python\|sql` |
| **job_description** | `jobs.description` | Direct copy | `We are looking...` |
| **url** | N/A | NULL | `None` |
| **posted_date** | N/A | NULL | `None` |

### 📝 Ghi chú Kaggle Mapping

#### ✅ Direct Mappings (Có sẵn trong source)
- `job_name` → `job_title`
- `location` → `location_raw`
- `description` → `job_description`
- `taglist` → `skills` (cần normalize)

#### 🔗 Join-Required Mappings (Cần join tables)
- `company_id` → Join với companies.csv → lấy `company_name`
- Lý do: jobs.csv chỉ có company_id, không có tên công ty

#### 🔄 Computed Mappings (Tính toán từ data có sẵn)
- `location` → normalize → `city`
- `job_name` → keyword extraction → `job_level`
- `job_name` → keyword classification → `job_category`

#### ❌ Not Available (Source không có)
- Salary fields: `salary_min`, `salary_max`, `salary_avg`, `salary_currency`
- URL: `url`
- Date: `posted_date`

#### 📌 Constants (Giá trị cố định cho Kaggle source)
- `source_dataset` = `'kaggle_itviec'`
- `job_site` = `'itviec'`
- `country` = `'Vietnam'`
- `employment_type` = `'full_time'`

---

## 🔶 Mapping chi tiết: GitHub → Master Schema

### 📂 Source File

- **job_descriptions.csv**: 3,101 rows, 11 columns
  - Columns: `title`, `company`, `company_image_url`, `location`, `description`, `site`, `job_url`, `it_role_type`, `main_programming_languages`, `key_technologies`, `city`

### 📋 Column Mapping Table

| Master Column | Source Column | Mapping Logic | Example |
|---------------|---------------|---------------|---------|
| **job_id** | N/A | `'job_' + str(i).zfill(6)` | `job_000001` |
| **source_dataset** | N/A | Constant: `'github_it_job_posting'` | `github_it_job_posting` |
| **job_site** | `site` | Direct copy (or default `'itviec'`) | `LinkedIn`, `TopCV` |
| **job_title** | `title` | Direct copy | `Senior Backend Engineer` |
| **company_name** | `company` | Direct copy | `Vinova` |
| **location_raw** | `location` | Direct copy | `Ha Noi, Vietnam` |
| **city** | `location` | Normalize via `normalize_city()` | `Ha Noi` |
| **province** | city | Copy from city | `Ha Noi` |
| **country** | N/A | Constant: `'Vietnam'` | `Vietnam` |
| **salary_min** | N/A | NULL | `None` |
| **salary_max** | N/A | NULL | `None` |
| **salary_avg** | N/A | NULL | `None` |
| **salary_currency** | N/A | NULL | `None` |
| **job_level** | `title` | Extract via `extract_job_level()` | `senior` |
| **job_category** | `title` | Classify via `categorize_job()` | `Backend Developer` |
| **employment_type** | N/A | Default: `'full_time'` | `full_time` |
| **skills** | `main_programming_languages` | Normalize via `normalize_skills()` | `java\|spring` |
| **job_description** | `description` | Direct copy | `We are hiring...` |
| **url** | `job_url` | Direct copy | `https://...` |
| **posted_date** | N/A | NULL | `None` |

### 📝 Ghi chú GitHub Mapping

#### ✅ Direct Mappings (Có sẵn trong source)
- `title` → `job_title`
- `company` → `company_name`
- `location` → `location_raw`
- `description` → `job_description`
- `main_programming_languages` → `skills` (cần normalize)
- `job_url` → `url` ⭐ **Chỉ có ở GitHub**
- `site` → `job_site` ⭐ **Multi-source information**

#### 🔄 Computed Mappings (Tính toán từ data có sẵn)
- `location` → normalize → `city`
- `title` → keyword extraction → `job_level`
- `title` → keyword classification → `job_category`

#### ❌ Not Available (Source không có)
- Salary fields: `salary_min`, `salary_max`, `salary_avg`, `salary_currency`
- Date: `posted_date`

#### 📌 Constants (Giá trị cố định cho GitHub source)
- `source_dataset` = `'github_it_job_posting'`
- `country` = `'Vietnam'`
- `employment_type` = `'full_time'`

#### 🌟 GitHub-specific Features
- **Multi-source**: GitHub data đến từ nhiều site (LinkedIn, TopCV, ITViec)
- **URL available**: Có link gốc đến job posting
- **Pre-classified**: Có sẵn `it_role_type` (không dùng, tự classify lại)

---

## 🔄 Transformation Functions

### 1. `normalize_city(location_raw)` → `city`

**Input**: Raw location string  
**Output**: Standardized city name  

**Mapping Rules**:
```python
'hà nội' / 'ha noi' / 'hanoi' → 'Ha Noi'
'hồ chí minh' / 'ho chi minh' / 'hcm' / 'saigon' → 'Ho Chi Minh'
'đà nẵng' / 'da nang' / 'danang' → 'Da Nang'
'hai phong' → 'Hai Phong'
'can tho' → 'Can Tho'
'binh duong' → 'Binh Duong'
'dong nai' → 'Dong Nai'
'remote' → 'Remote'
Other → 'Other'
NULL → 'Unknown'
```

**Example**:
```python
normalize_city('Hồ Chí Minh')  # → 'Ho Chi Minh'
normalize_city('HCM City')      # → 'Ho Chi Minh'
normalize_city('Ha Noi')        # → 'Ha Noi'
```

---

### 2. `parse_salary(salary_raw)` → `salary_min, salary_max, salary_avg, currency`

**Input**: Salary string (not available in current sources)  
**Output**: Tuple (min, max, avg, currency)  

**Parsing Rules** (for future data):
```python
# Extract numbers
'15-20 triệu' → min=15M, max=20M, avg=17.5M VND
'$2000-3000' → min=48M, max=72M, avg=60M VND (converted)
'Negotiate' → NULL

# Currency conversion
USD → VND (rate = 24,000)
'triệu' / 'tr' → multiply by 1,000,000
```

**Current Status**: ❌ Not available (returns NULL)

---

### 3. `extract_job_level(job_title)` → `job_level`

**Input**: Job title  
**Output**: Job level (intern/junior/mid/senior/manager)  

**Extraction Rules**:
```python
# Keyword matching (case-insensitive)
['intern', 'fresher', 'graduate'] → 'intern'
['junior', 'jr'] → 'junior'
['senior', 'sr', 'lead', 'principal', 'staff'] → 'senior'
['manager', 'head', 'director', 'chief', 'vp', 'cto', 'ceo'] → 'manager'
No match → 'mid' (default)
```

**Examples**:
```python
extract_job_level('Senior Backend Engineer')  # → 'senior'
extract_job_level('Junior Frontend Dev')      # → 'junior'
extract_job_level('Backend Developer')        # → 'mid'
extract_job_level('Engineering Manager')      # → 'manager'
```

---

### 4. `categorize_job(job_title)` → `job_category`

**Input**: Job title  
**Output**: Job category (13 categories)  

**Classification Rules** (keyword matching):
```python
['backend', 'back-end', 'server'] → 'Backend Developer'
['frontend', 'front-end', 'ui developer'] → 'Frontend Developer'
['fullstack', 'full-stack', 'full stack'] → 'Fullstack Developer'
['mobile', 'ios', 'android', 'flutter'] → 'Mobile Developer'
['devops', 'sre', 'infrastructure'] → 'DevOps Engineer'
['data engineer', 'etl', 'big data'] → 'Data Engineer'
['data scientist', 'data analyst', 'ml engineer'] → 'Data Scientist'
['qa', 'qc', 'test', 'tester'] → 'QA/Tester'
['security', 'cybersecurity'] → 'Security Engineer'
['software engineer', 'software developer'] → 'Software Engineer'
['product manager', 'product owner'] → 'Product Manager'
['business analyst', 'ba'] → 'Business Analyst'
No match → 'Other'
```

**Examples**:
```python
categorize_job('Senior Backend Engineer')     # → 'Backend Developer'
categorize_job('React Native Developer')      # → 'Mobile Developer'
categorize_job('Quality Assurance Engineer')  # → 'QA/Tester'
categorize_job('Blockchain Developer')        # → 'Other'
```

**Priority**: First match wins (order matters)

---

### 5. `normalize_skills(skills_raw)` → `skills`

**Input**: Skills string (comma-separated, may have brackets/quotes)  
**Output**: Pipe-separated lowercase skills  

**Normalization Rules**:
```python
# Remove brackets and quotes
"['Python', 'SQL', 'Docker']" → "Python, SQL, Docker"

# Split by comma
"Python, SQL, Docker" → ["Python", "SQL", "Docker"]

# Lowercase and strip whitespace
["Python", "SQL", "Docker"] → ["python", "sql", "docker"]

# Join with pipe
["python", "sql", "docker"] → "python|sql|docker"
```

**Examples**:
```python
normalize_skills("['Python', 'SQL']")  # → 'python|sql'
normalize_skills("Java, Spring, MySQL") # → 'java|spring|mysql'
normalize_skills("React, Node.js")      # → 'react|node.js'
```

---

## 🔀 Merge Strategy & Deduplication

### Merge Process

```python
# Step 1: Align columns
all_columns = set(df_kaggle.columns) | set(df_github.columns)
for col in all_columns:
    if col not in df_kaggle.columns:
        df_kaggle[col] = None
    if col not in df_github.columns:
        df_github[col] = None

# Step 2: Concatenate
df_merged = pd.concat([df_kaggle, df_github], ignore_index=True)
# Total: 4,513 rows (1,412 + 3,101)

# Step 3: Remove empty critical fields
df_merged = df_merged.dropna(subset=['job_title', 'company_name'])
df_merged = df_merged[df_merged['job_title'].str.strip() != '']
df_merged = df_merged[df_merged['company_name'].str.strip() != '']
```

### Deduplication Strategy

```python
# Create dedup key: title + company + city (lowercase)
df_merged['_dedup_key'] = (
    df_merged['job_title'].str.lower().str.strip() + '_' +
    df_merged['company_name'].str.lower().str.strip() + '_' +
    df_merged['city'].fillna('').str.lower()
)

# Sort by source_dataset (alphabetically: github < kaggle)
# This ensures Kaggle data is kept when duplicate found
df_merged = df_merged.sort_values('source_dataset')

# Drop duplicates, keep first (Kaggle priority)
df_merged = df_merged.drop_duplicates(subset='_dedup_key', keep='first')

# Result: 3,985 unique jobs (11.7% deduplication rate)
```

**Deduplication Results**:
- Before: 4,513 jobs
- After: 3,985 jobs
- Removed: 528 duplicates (11.7%)
- Priority: **Kaggle > GitHub** (keep Kaggle when duplicate)

---

## 📊 Data Flow Diagram (Text)

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOURCE DATASETS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  KAGGLE:                          GITHUB:                       │
│  ├─ jobs.csv (1,412)              └─ job_descriptions.csv      │
│  └─ companies.csv (2,041)            (3,101)                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                 MAPPING FUNCTIONS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  map_kaggle_jobs():                map_github_jobs():           │
│  ├─ Join with companies            ├─ Direct column mapping    │
│  ├─ Map to master schema           ├─ Map to master schema     │
│  └─ Add metadata                   └─ Add metadata             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                NORMALIZATION                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  apply_normalization():                                         │
│  ├─ normalize_city()         → city                            │
│  ├─ parse_salary()           → salary_min/max/avg              │
│  ├─ extract_job_level()      → job_level                       │
│  ├─ categorize_job()         → job_category                    │
│  └─ normalize_skills()       → skills                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│              MERGE & DEDUPLICATE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ├─ Align columns (add missing as NULL)                        │
│  ├─ Concatenate: Kaggle (1,412) + GitHub (3,101)               │
│  ├─ Remove empty title/company                                 │
│  ├─ Create dedup key: title + company + city                   │
│  ├─ Sort by source (Kaggle priority)                           │
│  └─ Drop duplicates → 3,985 unique jobs                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                  MASTER TABLE                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  jobs_master.csv / jobs_master.parquet                          │
│  ├─ 3,985 unique jobs                                           │
│  ├─ 19 columns (master schema)                                 │
│  ├─ 14 columns with data (73.7%)                               │
│  ├─ 5 columns NULL (26.3% - ready for future)                  │
│  └─ Ready for ML pipeline                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔮 Future Data Sources

### Thêm source mới: Quy trình

1. **Analyze Source Schema**
   - Liệt kê tất cả columns trong source
   - Xác định kiểu dữ liệu
   - Sample data để hiểu format

2. **Create Mapping Function**
   ```python
   def map_newsource_jobs(df):
       """Map new source to master schema"""
       mapped = pd.DataFrame()
       
       # Direct mappings
       mapped['job_title'] = df['their_title_column']
       mapped['company_name'] = df['their_company_column']
       # ... map all available columns
       
       # Add metadata
       mapped['source_dataset'] = 'newsource_name'
       mapped['job_site'] = 'their_site_name'
       mapped['country'] = 'Vietnam'
       
       return mapped
   ```

3. **Apply Normalization**
   - Dùng lại các functions: `normalize_city()`, `extract_job_level()`, etc.
   - Không cần viết lại normalization logic

4. **Test Merge**
   - Test mapping với sample data
   - Verify deduplication works correctly
   - Check data quality metrics

5. **Update Documentation**
   - Update file này với mapping mới
   - Update `docs/schema.md` nếu cần thêm cột
   - Update README.md

### Ví dụ: VietnamWorks Source

```python
# Giả sử VietnamWorks có schema:
# - job_title, company_name, location, salary_range, 
#   experience, job_description, skills_required, post_date

def map_vietnamworks_jobs(df):
    mapped = pd.DataFrame()
    
    # Direct mappings
    mapped['job_title'] = df['job_title']
    mapped['company_name'] = df['company_name']
    mapped['location_raw'] = df['location']
    mapped['job_description'] = df['job_description']
    mapped['skills'] = df['skills_required']
    mapped['posted_date'] = pd.to_datetime(df['post_date'])  # NEW!
    
    # Salary parsing (NEW!)
    if 'salary_range' in df.columns:
        mapped['salary_raw'] = df['salary_range']
    
    # Metadata
    mapped['source_dataset'] = 'vietnamworks'
    mapped['job_site'] = 'vietnamworks'
    mapped['country'] = 'Vietnam'
    
    return mapped

# Apply normalization (includes salary parsing!)
df_vietnamworks_normalized = apply_normalization(df_vietnamworks_clean)

# Merge với data hiện tại
df_merged = pd.concat([
    df_kaggle_normalized,
    df_github_normalized,
    df_vietnamworks_normalized  # NEW SOURCE!
], ignore_index=True)

# Deduplication tự động work với priority:
# kaggle > github > vietnamworks (alphabetically sorted)
```

---

## ✅ Validation Checklist

Khi thêm mapping mới, check:

- [ ] **Critical fields mapped**:
  - [ ] job_title
  - [ ] company_name
  - [ ] source_dataset (set constant)
  - [ ] job_site (set constant or map)
  - [ ] country (set to Vietnam)

- [ ] **Recommended fields mapped** (nếu có):
  - [ ] location_raw
  - [ ] job_description
  - [ ] skills
  - [ ] url
  - [ ] salary_raw (nếu có)
  - [ ] posted_date (nếu có)

- [ ] **Normalization applied**:
  - [ ] `normalize_city()` → city
  - [ ] `parse_salary()` → salary fields
  - [ ] `extract_job_level()` → job_level
  - [ ] `categorize_job()` → job_category
  - [ ] `normalize_skills()` → skills

- [ ] **Data quality checks**:
  - [ ] No NULL in job_title, company_name
  - [ ] City normalized correctly
  - [ ] Job_category classified correctly
  - [ ] Skills format correct (pipe-separated)

- [ ] **Documentation updated**:
  - [ ] This file (column_mapping.md)
  - [ ] docs/schema.md (if new columns)
  - [ ] README.md (statistics)

---

## 📚 Tài liệu liên quan

- **Master Schema**: `docs/schema.md` - Chi tiết 19 cột
- **Pipeline Overview**: `docs/pipeline_overview.md` - Data flow
- **README**: Root README.md - Project overview
- **Notebook**: `vietnam_it_jobs_merge_analysis.ipynb` - Implementation

---

**Last Updated**: November 14, 2025  
**Version**: 1.0.0  
**Mapping Sources**: 2 (Kaggle, GitHub) - Ready for more!
