# EDA Plan - Exploratory Data Analysis Chi Tiết

## 📋 Tổng quan

**Mục tiêu**: Biến EDA từ 4 biểu đồ cơ bản thành **"Gói phân tích xu hướng việc làm IT"** có chiều sâu, trả lời các câu hỏi quan trọng về thị trường việc làm IT tại Việt Nam.

**Dataset**: `jobs_master.csv` (3,985 jobs)
- **Source**: Kaggle (1,411 jobs - 35.4%) + GitHub (2,574 jobs - 64.6%)
- **Coverage**: 100% có 13/19 cột quan trọng, 92.7% có skills, 64.6% có URL

---

## 🎯 Cấu trúc EDA - 4 Nhóm Câu Hỏi

### **Nhóm A – Cấu trúc dữ liệu (Data Structure Overview)**
*Mục tiêu: Hiểu phân bố cơ bản của dataset*

### **Nhóm B – Skills Analysis (Phân tích kỹ năng)**
*Mục tiêu: Khám phá skills phổ biến và must-have cho từng category*

### **Nhóm C – Company & Job Site Analysis (Phân tích công ty & nền tảng)**
*Mục tiêu: So sánh công ty, nguồn dữ liệu, nền tảng tuyển dụng*

### **Nhóm D – Kết nối giữa Category & City (Geo-Category Analysis)**
*Mục tiêu: Tìm mối quan hệ giữa địa điểm và loại công việc*

---

## 📊 CHI TIẾT TỪNG NHÓM

---

## Nhóm A – Cấu trúc dữ liệu (Data Structure Overview)

### A1. Distribution of Job Categories
**Câu hỏi**: Category nào chiếm tỷ lệ lớn nhất trong thị trường IT Việt Nam?

**Cột sử dụng**: `job_category`

**Biểu đồ**: **Horizontal Bar Chart** (Top 15 categories)
- X-axis: Job count
- Y-axis: Job category
- Color: Gradient (dark → light theo số lượng)
- Sort: Descending by count

**Metric tính toán**:
- Count per category
- Percentage distribution
- Top 3 vs Bottom 3 categories

**Insight kỳ vọng**:
1. ✅ **"Other" sẽ chiếm tỷ lệ cao (40.5%)** vì nhiều job title không match keywords (đã validate trong categorization_rules.md)
2. ✅ **Backend > Fullstack > QA/Tester** (dựa trên phân tích hiện tại: Backend 9.4%, Fullstack 8.7%, QA 8.5%)
3. 🔍 **Data Science/AI categories thấp** (emerging field, chưa phổ biến rộng rãi)

**Cross-reference**: 
- `docs/categorization_rules.md` - Keyword rules cho classification
- Current distribution: Other 40.5%, Backend 9.4%, Fullstack 8.7%

---

### A2. Distribution of Job Levels
**Câu hỏi**: Thị trường tuyển level nào nhiều nhất? Junior hay Senior?

**Cột sử dụng**: `job_level`

**Biểu đồ**: **Pie Chart** hoặc **Donut Chart** với percentages
- Slices: 5 levels (intern, junior, mid, senior, manager)
- Colors: Sequential palette (light blue → dark blue)
- Labels: Count + Percentage

**Metric tính toán**:
- Count per level
- Percentage distribution
- Mid-to-Senior ratio (kiểm tra thị trường thiên về experienced hay entry-level)

**Insight kỳ vọng**:
1. ✅ **Mid-level chiếm đa số (~65.7%)** - Đã validate trong categorization_rules.md
2. ✅ **Senior level cao (23.3%)** - Thị trường cần người có kinh nghiệm
3. 🔍 **Junior + Intern thấp (<8%)** - Ít vị trí entry-level?

**Câu hỏi follow-up** (cho EDA phase 2):
- Mid-level nhiều ở category nào? (Backend có nhiều mid hơn QA không?)
- Senior nhiều ở city nào? (HCM vs HN)

**Cross-reference**: 
- `docs/categorization_rules.md` - Job level keywords và priority
- Current distribution: mid 65.7%, senior 23.3%, junior 5.0%

---

### A3. Distribution of Cities
**Câu hỏi**: Job tập trung ở thành phố nào? HCM vs HN vs Remote?

**Cột sử dụng**: `city`

**Biểu đồ**: **Vertical Bar Chart** (Top 10 cities)
- X-axis: City name
- Y-axis: Job count
- Color: Different color per city (use distinctive palette)
- Sort: Descending by count

**Metric tính toán**:
- Count per city
- Percentage distribution
- HCM-to-HN ratio
- Remote job percentage

**Insight kỳ vọng**:
1. 🔍 **Ho Chi Minh >> Ha Noi** (HCM là tech hub lớn nhất)
2. 🔍 **Da Nang ở vị trí thứ 3** (hub mới nổi)
3. 🔍 **Remote jobs tăng** (trend sau COVID)
4. 🔍 **Other cities < 5%** (job tập trung ở 2-3 thành phố chính)

**Câu hỏi follow-up**:
- Remote jobs thuộc category nào? (Backend/Frontend phù hợp remote hơn QA?)

**Cross-reference**: 
- `docs/schema.md` - City normalization rules
- `data/reference/city_province_mapping.csv` - 90+ patterns normalized

---

### A4. Data Completeness Heatmap (NEW)
**Câu hỏi**: Cột nào có dữ liệu đầy đủ? Cột nào còn thiếu?

**Cột sử dụng**: All 19 columns

**Biểu đồ**: **Heatmap** showing data coverage
- X-axis: Columns (19 columns)
- Y-axis: Single row (data coverage)
- Color: Green (100%) → Yellow (50%) → Red (0%)
- Annotation: Percentage in each cell

**Metric tính toán**:
- For each column: `non_null_count / total_count * 100`
- Identify columns with 0% data (salary fields)
- Identify columns with partial data (skills 92.7%, url 64.6%)

**Insight kỳ vọng**:
1. ✅ **13/19 cột có 100% data** (job_title, company_name, city, job_level, job_category, etc.)
2. ✅ **Skills: 92.7% coverage** (good for skills analysis)
3. ✅ **URL: 64.6% coverage** (chỉ GitHub có, Kaggle không có)
4. ✅ **Salary: 0% coverage** (cả 4 cột salary đều NULL)

**Ý nghĩa**: Xác định columns nào reliable cho analysis, columns nào cần skip

**Cross-reference**: 
- `docs/schema.md` - Full column documentation
- `docs/STAGE_2_SUMMARY.md` - Task 2.2 salary clarification

---

## Nhóm B – Skills Analysis (Phân tích kỹ năng)

### B1. Top 20 Most Popular Skills
**Câu hỏi**: Skill nào được yêu cầu nhiều nhất trong job IT Việt Nam?

**Cột sử dụng**: `skills` (92.7% coverage)

**Xử lý dữ liệu**:
```python
# Skills are pipe-separated: "python|django|postgresql"
skills_list = df['skills'].dropna().str.split('|')
all_skills = [skill.strip().lower() for sublist in skills_list for skill in sublist]
skill_counts = pd.Series(all_skills).value_counts().head(20)
```

**Biểu đồ**: **Horizontal Bar Chart** (Top 20 skills)
- X-axis: Frequency count
- Y-axis: Skill name
- Color: Gradient by frequency (hot colormap)
- Sort: Descending by count

**Metric tính toán**:
- Frequency count per skill
- Percentage of jobs mentioning skill
- Top 5 skills dominating market

**Insight kỳ vọng**:
1. 🔍 **JavaScript/TypeScript/React phổ biến** (web development dominant)
2. 🔍 **Python xuất hiện nhiều** (backend + data + AI)
3. 🔍 **Java/Spring phổ biến** (enterprise applications)
4. 🔍 **SQL/Database skills high** (backend fundamental)
5. 🔍 **Docker/Kubernetes/AWS** (DevOps trend)

**Câu hỏi follow-up**:
- Skill nào đang "hot" (tăng trưởng nhanh)?
- Skill nào kết hợp với nhau? (React + Node? Python + Django?)

---

### B2. Must-Have Skills Per Category (Category-Specific Skills)
**Câu hỏi**: Với mỗi category (Backend, Frontend, QA, Data...), skill nào là "must-have"?

**Cột sử dụng**: `job_category`, `skills`

**Xử lý dữ liệu**:
```python
# For each category, extract top skills
for category in ['Backend Developer', 'Frontend Developer', 'QA/Tester', 
                  'Data Engineer', 'Mobile Developer', 'DevOps Engineer']:
    cat_skills = df[df['job_category'] == category]['skills'].dropna()
    # Get top 10 skills for this category
```

**Biểu đồ**: **Grouped Horizontal Bar Chart** hoặc **Facet Plot**
- Option 1: Facet grid (6 subplots for top 6 categories)
- Option 2: Single chart với colors per category
- X-axis: Skill frequency
- Y-axis: Skill name
- Color: Different color per category

**Metric tính toán**:
- Top 10 skills per category
- Skill penetration rate: `jobs_with_skill / total_jobs_in_category`
- "Exclusive skills" (skills chỉ có trong 1 category)

**Insight kỳ vọng**:

**Backend Developer**:
- 🔍 Must-have: Java, Python, Node.js, Spring Boot, PostgreSQL, MySQL, Docker
- 🔍 Framework: Django, Laravel, .NET Core

**Frontend Developer**:
- 🔍 Must-have: React, Vue, Angular, JavaScript, TypeScript, HTML/CSS
- 🔍 Tools: Webpack, Redux, Next.js

**QA/Tester**:
- 🔍 Must-have: Selenium, Jira, Postman, automation testing
- 🔍 Languages: Python (test scripts), Java (test frameworks)

**Data Engineer**:
- 🔍 Must-have: Python, SQL, Spark, Kafka, Airflow, ETL
- 🔍 Cloud: AWS, GCP, Azure

**Mobile Developer**:
- 🔍 Must-have: React Native, Flutter, Swift, Kotlin, iOS, Android

**DevOps Engineer**:
- 🔍 Must-have: Docker, Kubernetes, Jenkins, CI/CD, AWS, Terraform, Ansible

**Câu hỏi follow-up**:
- Skills nào overlap giữa các categories? (Python trong Backend vs Data)
- Skills "unicorn" (hiếm, chỉ 1 category cần)?

---

### B3. Skills Co-occurrence Matrix (Advanced)
**Câu hỏi**: Skills nào thường đi cùng nhau? (React + Node? Python + Django?)

**Cột sử dụng**: `skills`

**Xử lý dữ liệu**:
```python
# Create co-occurrence matrix
from itertools import combinations
# For each job, count skill pairs
skill_pairs = []
for skills in df['skills'].dropna():
    skills_list = [s.strip().lower() for s in skills.split('|')]
    skill_pairs.extend(list(combinations(skills_list, 2)))
# Count frequency of pairs
```

**Biểu đồ**: **Heatmap** (Top 15 skills × Top 15 skills)
- X-axis: Skill A
- Y-axis: Skill B
- Color: Co-occurrence frequency (dark = high co-occurrence)
- Annotation: Counts in cells

**Metric tính toán**:
- Co-occurrence count for each skill pair
- Support: `P(A and B)` - How often both appear together
- Confidence: `P(B|A)` - If job has A, probability of having B

**Insight kỳ vọng**:
1. 🔍 **React + TypeScript** (modern frontend stack)
2. 🔍 **Python + Django/Flask** (Python backend combo)
3. 🔍 **Java + Spring** (enterprise Java stack)
4. 🔍 **Docker + Kubernetes** (containerization stack)
5. 🔍 **AWS + Terraform** (cloud infrastructure)

**Ứng dụng**: 
- Recommendation: "Nếu bạn biết React, nên học thêm TypeScript/Redux"
- Job matching: Skills combos for better matches

---

### B4. Skills Diversity by Category (Box Plot)
**Câu hỏi**: Category nào yêu cầu nhiều skills nhất? Backend hay QA?

**Cột sử dụng**: `job_category`, `skills`

**Xử lý dữ liệu**:
```python
# Count number of skills per job
df['skill_count'] = df['skills'].str.split('|').str.len()
# Group by category, get distribution
```

**Biểu đồ**: **Box Plot** (Skills count distribution per category)
- X-axis: Job category
- Y-axis: Number of skills required
- Box: Q1, Median, Q3
- Whiskers: Min, Max
- Outliers: Jobs with unusually many/few skills

**Metric tính toán**:
- Mean skills per category
- Median skills per category
- Max skills (most demanding jobs)
- Min skills (entry-level?)

**Insight kỳ vọng**:
1. 🔍 **Backend/Fullstack yêu cầu nhiều skills nhất** (database + framework + DevOps)
2. 🔍 **QA yêu cầu ít skills hơn** (focused on testing tools)
3. 🔍 **Data Engineer/DevOps cao** (multi-tool environments)
4. 🔍 **Junior jobs: ít skills, Senior jobs: nhiều skills**

**Câu hỏi follow-up**:
- Job nào yêu cầu nhiều skills nhất? (specific job_id)
- Có correlation giữa số skills và job_level không?

---

## Nhóm C – Company & Job Site Analysis (Phân tích công ty & nền tảng)

### C1. Top 20 Companies Hiring Most
**Câu hỏi**: Công ty nào tuyển nhiều job IT nhất?

**Cột sử dụng**: `company_name`

**Biểu đồ**: **Horizontal Bar Chart** (Top 20 companies)
- X-axis: Number of job postings
- Y-axis: Company name
- Color: Gradient (or industry-based if available)
- Sort: Descending by count

**Metric tính toán**:
- Job count per company
- Percentage of total jobs
- Top 5 companies vs Rest

**Insight kỳ vọng**:
1. 🔍 **Big tech companies** (FPT Software, Viettel, VNPT) tuyển nhiều
2. 🔍 **Outsourcing companies** (KMS, NashTech, Luxoft) high volume
3. 🔍 **Startups** (nếu có) - smaller counts, distributed
4. 🔍 **Top 20 chiếm ~30-40% total jobs** (tập trung vào big players)

**Câu hỏi follow-up**:
- Công ty nào tuyển level nào? (FPT nhiều junior? KMS nhiều senior?)
- Công ty nào tuyển category gì? (Viettel nhiều Backend? VNG nhiều Game Dev?)

---

### C2. Job Distribution by Source Dataset
**Câu hỏi**: Kaggle vs GitHub - nguồn nào đóng góp nhiều hơn? Có khác biệt gì?

**Cột sử dụng**: `source_dataset` (kaggle_itviec vs github_it_job_posting)

**Biểu đồ 1**: **Pie Chart** (Simple count comparison)
- Slices: 2 sources (Kaggle 35.4%, GitHub 64.6%)

**Biểu đồ 2**: **Stacked Bar Chart** (Category distribution by source)
- X-axis: Job category
- Y-axis: Job count
- Stacks: 2 colors (Kaggle vs GitHub)
- Compare: Which categories dominated by which source?

**Metric tính toán**:
- Count per source
- Category distribution per source
- Level distribution per source

**Insight kỳ vọng**:
1. ✅ **GitHub đóng góp nhiều hơn (64.6%)** - Đã biết từ deduplication metrics
2. 🔍 **Kaggle (ITViec) có nhiều mid-level jobs** (ITViec popular cho local market)
3. 🔍 **GitHub có nhiều senior jobs** (LinkedIn/TopCV trong GitHub data)
4. 🔍 **Overlap companies: ~500 companies** (từ deduplication analysis)

**Cross-reference**: 
- `docs/pipeline_overview.md` - Deduplication section
- 528 duplicates removed (11.7% overlap)

---

### C3. Job Site Comparison (ITViec vs LinkedIn vs TopCV)
**Câu hỏi**: Nền tảng nào đăng loại job gì? ITViec nhiều Backend? LinkedIn nhiều Senior?

**Cột sử dụng**: `job_site` (itviec, LinkedIn, ITViec, TopCV)

**Xử lý dữ liệu**:
```python
# Normalize job_site (itviec vs ITViec)
df['job_site_clean'] = df['job_site'].str.lower().str.strip()
```

**Biểu đồ 1**: **Grouped Bar Chart** (Job count by site)
- X-axis: Job site
- Y-axis: Job count
- Show top 3-4 sites

**Biểu đồ 2**: **Stacked Bar Chart** (Category distribution by job site)
- X-axis: Job site
- Y-axis: Percentage (normalized to 100% per site)
- Stacks: Top 8 categories
- Compare: ITViec = Backend-heavy? LinkedIn = Senior-heavy?

**Biểu đồ 3**: **Grouped Bar Chart** (Level distribution by job site)
- X-axis: Job site
- Y-axis: Count
- Groups: 5 levels (intern, junior, mid, senior, manager)

**Metric tính toán**:
- Count per job_site
- Category distribution per site (percentage)
- Level distribution per site (percentage)
- Average skills_count per site

**Insight kỳ vọng**:
1. 🔍 **ITViec**: Many mid-level, Backend/Frontend jobs (local focus)
2. 🔍 **LinkedIn**: More senior-level, international companies
3. 🔍 **TopCV**: Mix, potentially more entry-level (broader audience)

**Cross-reference**: 
- `docs/column_mapping.md` - job_site mapping rules
- Kaggle → always `itviec`, GitHub → preserve original `site`

---

### C4. Companies with Most Diverse Job Postings
**Câu hỏi**: Công ty nào tuyển đa dạng nhất (nhiều category, nhiều level)?

**Cột sử dụng**: `company_name`, `job_category`, `job_level`

**Xử lý dữ liệu**:
```python
# For each company, count unique categories and levels
company_diversity = df.groupby('company_name').agg({
    'job_category': 'nunique',
    'job_level': 'nunique',
    'job_id': 'count'
}).rename(columns={'job_id': 'total_jobs'})
# Diversity score = (unique_categories + unique_levels) / 2
company_diversity['diversity_score'] = (
    company_diversity['job_category'] + company_diversity['job_level']
) / 2
```

**Biểu đồ**: **Scatter Plot** (Diversity vs Volume)
- X-axis: Total jobs posted
- Y-axis: Diversity score (unique categories + levels)
- Size: Bubble size = total jobs
- Color: Gradient by diversity score
- Label: Top 10 companies

**Metric tính toán**:
- Unique categories per company
- Unique levels per company
- Diversity score (combined metric)
- Top 10 most diverse companies

**Insight kỳ vọng**:
1. 🔍 **Big companies (FPT, Viettel) = high diversity** (tuyển all categories, all levels)
2. 🔍 **Small companies = low diversity** (focus on 1-2 categories)
3. 🔍 **Outliers**: Nhiều jobs nhưng ít diversity (chỉ tuyển 1 role)

**Ứng dụng**: Identify companies good for career growth (nhiều roles khác nhau)

---

## Nhóm D – Kết nối giữa Category & City (Geo-Category Analysis)

### D1. Category Distribution by City (Heatmap)
**Câu hỏi**: Thành phố nào mạnh về Backend? Thành phố nào nhiều Data Engineer?

**Cột sử dụng**: `city`, `job_category`

**Biểu đồ**: **Heatmap** (City × Category)
- X-axis: Job category (Top 10 categories)
- Y-axis: City (Top 8 cities: HCM, HN, Da Nang, Remote, etc.)
- Color: Job count (dark = high concentration)
- Annotation: Count in each cell

**Metric tính toán**:
- Job count for each (city, category) pair
- Percentage of category jobs in each city
- Dominant category per city

**Insight kỳ vọng**:
1. 🔍 **Ho Chi Minh**: Strong in Backend, Fullstack, QA (tech hub)
2. 🔍 **Ha Noi**: Strong in Data Engineer, AI/ML (research + tech companies)
3. 🔍 **Da Nang**: Growing in Backend, Frontend (emerging hub)
4. 🔍 **Remote**: High in Backend, DevOps (remote-friendly roles)
5. 🔍 **Other cities**: Low job counts, scattered categories

**Câu hỏi follow-up**:
- City nào có "specialty"? (HN = Data, HCM = Backend)
- Remote jobs: Which categories are most remote-friendly?

---

### D2. Level Distribution by City (Stacked Bar Chart)
**Câu hỏi**: HCM vs HN - thành phố nào tuyển senior nhiều hơn?

**Cột sử dụng**: `city`, `job_level`

**Biểu đồ**: **Stacked Bar Chart** (100% stacked)
- X-axis: City (Top 6 cities)
- Y-axis: Percentage (normalized to 100% per city)
- Stacks: 5 levels (intern, junior, mid, senior, manager)
- Colors: Sequential palette (light → dark = intern → manager)

**Metric tính toán**:
- Level distribution per city (percentage)
- Mid-to-Senior ratio per city
- Which city has most entry-level jobs?

**Insight kỳ vọng**:
1. 🔍 **Ha Noi**: More senior/manager roles (HQ of big corps)
2. 🔍 **Ho Chi Minh**: More mid-level roles (high volume, diverse)
3. 🔍 **Da Nang**: More junior/mid roles (growing market, training hub)
4. 🔍 **Remote**: Skew toward senior (trust-based remote work)

**Cross-reference**: 
- Compare với A2 (overall level distribution)
- Identify cities best for entry-level vs experienced candidates

---

### D3. Top Skills by City (Facet Grid)
**Câu hỏi**: HCM cần skill gì? HN cần skill gì khác?

**Cột sử dụng**: `city`, `skills`

**Biểu đồ**: **Facet Grid** (4-6 subplots for top cities)
- Subplots: Ha Noi, Ho Chi Minh, Da Nang, Remote (4 plots)
- Each subplot: Horizontal bar chart (Top 10 skills for that city)
- X-axis: Skill frequency
- Y-axis: Skill name
- Color: Same color per city (for consistency)

**Metric tính toán**:
- Top 10 skills per city
- Skill penetration: `skill_count / total_jobs_in_city`
- Common skills across all cities vs city-specific skills

**Insight kỳ vọng**:
1. 🔍 **Ho Chi Minh**: JavaScript, React, Node, Java (web dev focus)
2. 🔍 **Ha Noi**: Python, AWS, Data skills (data + cloud focus)
3. 🔍 **Da Nang**: React, Vue, Frontend skills (outsourcing focus)
4. 🔍 **Remote**: Docker, Kubernetes, Backend (DevOps/Backend friendly)

**Ứng dụng**: 
- Job seekers: "Nếu bạn biết Python, nên tìm việc ở HN"
- Companies: "HCM thiếu Data Engineer, cơ hội tuyển"

---

### D4. Category-City Concentration Index (Advanced)
**Câu hỏi**: Category nào "tập trung" nhất vào 1 thành phố? (Specialization index)

**Cột sử dụng**: `city`, `job_category`

**Xử lý dữ liệu**:
```python
# Calculate Herfindahl Index (concentration measure)
# For each category, calculate: sum((city_share)^2)
# High index = concentrated in 1 city
# Low index = distributed across cities
```

**Biểu đồ**: **Horizontal Bar Chart** (Concentration index per category)
- X-axis: Concentration index (0 to 1)
- Y-axis: Job category
- Color: Gradient (red = high concentration, green = distributed)
- Sort: Descending by index

**Metric tính toán**:
- Herfindahl Index per category: `HHI = sum((share_i)^2)`
- Which category most concentrated? (e.g., Data Engineer in HN)
- Which category most distributed? (e.g., Backend everywhere)

**Insight kỳ vọng**:
1. 🔍 **Data Engineer/AI jobs**: High concentration (mostly HN)
2. 🔍 **Backend Developer**: Low concentration (distributed HCM/HN/DN)
3. 🔍 **Game Developer**: High concentration (specific hubs)
4. 🔍 **QA/Tester**: Medium concentration (follows Backend)

**Ứng dụng**: 
- Identify specialized cities (HN = Data hub)
- Identify generalist cities (HCM = all categories)

---

## 📊 SUMMARY TABLE - ALL EDA QUESTIONS

| Nhóm | ID | Câu hỏi | Cột sử dụng | Biểu đồ | Insight kỳ vọng |
|------|----|---------|--------------|---------|--------------------|
| **A** | A1 | Category nào chiếm tỷ lệ lớn nhất? | `job_category` | Horizontal Bar | Other 40.5%, Backend 9.4%, Fullstack 8.7% |
| **A** | A2 | Thị trường tuyển level nào nhiều nhất? | `job_level` | Pie/Donut | Mid 65.7%, Senior 23.3% |
| **A** | A3 | Job tập trung ở thành phố nào? | `city` | Vertical Bar | HCM >> HN >> Da Nang |
| **A** | A4 | Cột nào có dữ liệu đầy đủ? | All 19 columns | Heatmap | 13/19 cột 100%, skills 92.7%, salary 0% |
| **B** | B1 | Skill nào phổ biến nhất? | `skills` | Horizontal Bar | JS/React/Python/Java/SQL top 5 |
| **B** | B2 | Must-have skills per category? | `job_category`, `skills` | Grouped/Facet | Backend→Java/Python, Frontend→React/Vue |
| **B** | B3 | Skills nào đi cùng nhau? | `skills` | Heatmap | React+TypeScript, Python+Django, Docker+K8s |
| **B** | B4 | Category nào yêu cầu nhiều skills nhất? | `job_category`, `skills` | Box Plot | Backend/Fullstack nhiều, QA ít |
| **C** | C1 | Công ty nào tuyển nhiều nhất? | `company_name` | Horizontal Bar | FPT, Viettel, KMS top |
| **C** | C2 | Kaggle vs GitHub - khác biệt? | `source_dataset`, `job_category` | Pie + Stacked Bar | GitHub 64.6%, Kaggle 35.4% |
| **C** | C3 | ITViec vs LinkedIn vs TopCV? | `job_site`, `job_category`, `job_level` | Grouped + Stacked | ITViec mid-level, LinkedIn senior |
| **C** | C4 | Công ty nào tuyển đa dạng nhất? | `company_name`, `job_category`, `job_level` | Scatter | Big companies high diversity |
| **D** | D1 | Thành phố nào mạnh về category nào? | `city`, `job_category` | Heatmap | HCM=Backend, HN=Data |
| **D** | D2 | HCM vs HN - level distribution? | `city`, `job_level` | Stacked Bar 100% | HN more senior, HCM more mid |
| **D** | D3 | Top skills by city? | `city`, `skills` | Facet Grid | HCM=JS/React, HN=Python/AWS |
| **D** | D4 | Category nào tập trung vào 1 city? | `city`, `job_category` | Horizontal Bar | Data Engineer concentrated in HN |

**Tổng số**: **16 câu hỏi EDA**, **4 nhóm**, **16 biểu đồ chính**

---

## 🎨 Visualization Guidelines

### Color Palettes
- **Categories**: Use `tab10` or `Set3` (distinctive colors for 13 categories)
- **Levels**: Sequential blue (`Blues_r`) - intern (light) → manager (dark)
- **Cities**: Qualitative palette (`Paired` or `Set2`)
- **Heatmaps**: `YlOrRd` (yellow-orange-red) or `viridis` (perceptually uniform)

### Chart Styling
- **Font**: Use `Arial` or `Helvetica`, size 10-12pt
- **Title**: Bold, size 14pt, clear question
- **Axis labels**: Clear units (count, percentage, etc.)
- **Legend**: Outside plot area (right side), sorted by value
- **Grid**: Light gray, only major gridlines
- **Annotations**: Add percentages for top 3-5 items

### Figure Size Standards
- **Single chart**: 10×6 inches
- **Facet grid (2×2)**: 12×10 inches
- **Heatmap**: 12×8 inches (wide for readability)
- **Resolution**: 300 DPI for publication quality

---

## 🔄 Implementation Roadmap

### Phase 1: Basic Structure (Nhóm A)
**Timeline**: 1-2 hours
**Tasks**:
1. ✅ Load `jobs_master.csv`
2. ✅ Create 4 basic charts (A1-A4)
3. ✅ Validate distributions against documented stats
4. ✅ Add titles, labels, legends

**Deliverable**: Notebook section "Nhóm A - Data Structure Overview" với 4 biểu đồ

---

### Phase 2: Skills Analysis (Nhóm B)
**Timeline**: 2-3 hours
**Tasks**:
1. Parse `skills` column (split by `|`, lowercase, strip)
2. Create B1 (Top 20 skills bar chart)
3. Create B2 (Must-have skills per category - 6 facets)
4. Create B3 (Co-occurrence heatmap - advanced)
5. Create B4 (Skills diversity box plot)

**Challenges**:
- Skills data 92.7% coverage (292 jobs missing skills)
- Need to handle NULL/empty skills gracefully
- Co-occurrence matrix can be large (need to filter top skills only)

**Deliverable**: Notebook section "Nhóm B - Skills Analysis" với 4 biểu đồ

---

### Phase 3: Company & Job Site (Nhóm C)
**Timeline**: 2-3 hours
**Tasks**:
1. Create C1 (Top 20 companies bar chart)
2. Create C2 (Source comparison: pie + stacked bar)
3. Create C3 (Job site comparison: 3 charts)
4. Create C4 (Company diversity scatter plot)

**Challenges**:
- Company name normalization (FPT vs FPT Software?)
- Job site normalization (itviec vs ITViec)
- Source comparison needs clear interpretation

**Deliverable**: Notebook section "Nhóm C - Company & Job Site Analysis" với 7 biểu đồ

---

### Phase 4: Geo-Category Analysis (Nhóm D)
**Timeline**: 2-3 hours
**Tasks**:
1. Create D1 (City × Category heatmap)
2. Create D2 (Level by city stacked bar)
3. Create D3 (Top skills by city facet grid)
4. Create D4 (Concentration index - advanced)

**Challenges**:
- Heatmap can be sparse (many city-category combos have 0 jobs)
- Need to filter to top 8 cities and top 10 categories for clarity
- Concentration index calculation (Herfindahl Index)

**Deliverable**: Notebook section "Nhóm D - Geo-Category Analysis" với 4 biểu đồ

---

### Phase 5: Insights Summary & Report
**Timeline**: 1 hour
**Tasks**:
1. Write markdown summary for each nhóm
2. Compare expected insights vs actual results
3. Highlight surprising findings (if any)
4. Create final summary table (all metrics)
5. Export key charts as PNG/SVG

**Deliverable**: 
- Notebook section "EDA Summary & Key Insights"
- Folder `outputs/eda_charts/` với all PNG exports

---

## 📈 Expected Outputs

### After EDA Completion:

**1. Jupyter Notebook**:
- File: `vietnam_it_jobs_merge_analysis.ipynb` (updated)
- Sections:
  - Nhóm A: Data Structure (4 charts)
  - Nhóm B: Skills Analysis (4 charts)
  - Nhóm C: Company & Job Site (7 charts)
  - Nhóm D: Geo-Category Analysis (4 charts)
  - Summary & Insights (markdown + table)
- **Total**: 19 charts, ~200 lines of markdown insights

**2. Chart Exports** (optional):
- Folder: `outputs/eda_charts/`
- Files: `A1_category_distribution.png`, `B1_top_skills.png`, etc.
- Format: PNG (300 DPI) or SVG (vector)

**3. Insights Report** (optional):
- File: `docs/eda_insights.md`
- Summary of all findings
- Compare expected vs actual insights
- Recommendations for next steps

---

## 🔗 Cross-References

### Related Documentation:
- **Schema**: `docs/schema.md` - Column definitions, data coverage
- **Categorization**: `docs/categorization_rules.md` - Job level/category rules
- **Deduplication**: `docs/pipeline_overview.md` - Source merge strategy
- **City Mapping**: `data/reference/city_province_mapping.csv` - 90+ patterns
- **Master Data**: `data/final/jobs_master.csv` - 3,985 jobs

### Key Statistics to Reference:
- Total jobs: 3,985
- Sources: Kaggle 35.4%, GitHub 64.6%
- Cities: 9 unique (HCM, HN, DN, Remote, etc.)
- Categories: 13 categories (Other 40.5%, Backend 9.4%)
- Levels: 5 levels (mid 65.7%, senior 23.3%)
- Skills coverage: 92.7% (3,693/3,985 jobs)
- Companies: 1,901 unique

---

## 🎯 Success Criteria

### EDA is considered COMPLETE when:
1. ✅ All 16 questions answered with charts
2. ✅ All 4 nhóm (A-D) documented in notebook
3. ✅ Expected insights validated (or explained if different)
4. ✅ Charts have proper titles, labels, legends
5. ✅ Markdown summaries for each nhóm
6. ✅ Key findings highlighted (top 3-5 per nhóm)
7. ✅ Cross-checked against documentation (schema, categorization, dedup)

### Bonus (Optional):
- 📊 Interactive charts (Plotly) instead of static (Matplotlib)
- 📤 Export charts as PNG/SVG for reports
- 📝 Create `docs/eda_insights.md` summary report
- 🔄 Add code comments explaining non-obvious calculations

---

## 💡 Future Enhancements (Post-EDA)

### After completing basic EDA, consider:

**1. Temporal Analysis** (if posted_date becomes available):
- Job posting trends over time
- Seasonal patterns (which months have most jobs?)
- Category growth rates (which categories growing fast?)

**2. Salary Analysis** (if salary data becomes available):
- Salary by category, level, city
- Skills that pay most
- Company salary ranges

**3. Text Analysis on job_description**:
- Word clouds per category
- Required vs preferred skills (from description text)
- Soft skills mentions (communication, teamwork)

**4. Network Analysis**:
- Company-skill networks (which companies use which skills?)
- Skill-skill networks (which skills cluster together?)
- Category-city networks (bipartite graph)

**5. Predictive Modeling** (already in pipeline):
- Use EDA insights to improve feature engineering
- Feature importance from EDA (which features matter most?)

---

## 📝 Notes & Considerations

### Data Quality Notes:
1. **Skills coverage 92.7%**: 292 jobs have no skills data
   - Handle gracefully in B1-B4 (use `.dropna()`)
   - Document impact in insights (e.g., "Based on 3,693 jobs with skills data")

2. **Job site normalization**: `itviec` vs `ITViec`
   - Normalize to lowercase before analysis
   - Document in C3 insights

3. **Company name variations**: 
   - `FPT Software` vs `FPT Software Company Limited`
   - Keep as-is (already normalized in master data)
   - If variations exist, document in C1/C4

4. **Category "Other" high (40.5%)**:
   - Expected (documented in categorization_rules.md)
   - Mention in insights: "Many Vietnamese titles, non-tech roles, specialized roles"

### Visualization Best Practices:
1. **Always sort charts** (descending for bar charts)
2. **Limit to top N** (top 10-20 to avoid clutter)
3. **Add percentages** (not just counts) for context
4. **Use consistent colors** across related charts
5. **Annotate interesting findings** (arrows, text boxes)

### Interpretation Guidelines:
1. **Compare with expectations**: Use "Insight kỳ vọng" as baseline
2. **Explain surprises**: If results differ, investigate why
3. **Cross-validate**: Check against documentation (schema, categorization)
4. **Avoid over-interpretation**: Correlation ≠ causation
5. **Document limitations**: Missing data, normalization issues, etc.

---

## ✅ Checklist - EDA Plan Complete

- [x] Define 4 nhóm câu hỏi (A, B, C, D)
- [x] List 16 specific questions with columns, charts, insights
- [x] Document expected insights per question
- [x] Provide implementation roadmap (5 phases)
- [x] Define success criteria
- [x] Add visualization guidelines (colors, styling, sizes)
- [x] Cross-reference with existing documentation
- [x] Include data quality notes and considerations
- [x] Create summary table (16 questions overview)
- [x] Document future enhancements (post-EDA)

---

**Status**: ✅ **EDA Plan HOÀN THÀNH**  
**File**: `docs/eda_plan.md`  
**Next Step**: Implement EDA in notebook (Phase 1 → Phase 5)  
**Estimated Time**: 8-12 hours for full implementation

---

## 🎓 Key Takeaways

### What Makes This EDA "Deep"?
1. ✅ **16 questions** vs 4 basic charts (4× more comprehensive)
2. ✅ **4 nhóm** organized by theme (not random charts)
3. ✅ **Cross-analysis**: Category × City, Skills × Category, etc.
4. ✅ **Advanced metrics**: Co-occurrence, concentration index, diversity score
5. ✅ **Actionable insights**: Skills to learn, cities to target, companies to apply

### How This Differs from Basic EDA?
| Aspect | Basic EDA | Deep EDA (This Plan) |
|--------|-----------|----------------------|
| Questions | 3-4 | 16 |
| Charts | Bar, Pie | Bar, Heatmap, Facet, Box, Scatter |
| Insights | Descriptive | Descriptive + Cross-analysis + Recommendations |
| Skills | No | 4 dedicated questions (B1-B4) |
| Geo-analysis | No | Full nhóm (D1-D4) |
| Company | Maybe | 3 questions (C1, C3, C4) |
| Depth | Surface | Multi-dimensional |

### Answering Potential Questions

**Q1**: "Tại sao cần 16 questions? 4 biểu đồ không đủ sao?"  
**A**: 4 biểu đồ chỉ mô tả distribution cơ bản. 16 questions trả lời "WHY" và "SO WHAT":
- Nhóm B: Skills analysis → Job seekers biết học skill gì
- Nhóm C: Company analysis → Biết công ty nào hiring active
- Nhóm D: Geo-category → Biết city nào phù hợp với skills mình

**Q2**: "Có cần heatmap, co-occurrence không? Phức tạp quá?"  
**A**: Cần! Đây là điểm khác biệt giữa "EDA report" vs "data summary":
- Heatmap (D1): Một cái nhìn toàn cảnh city-category patterns
- Co-occurrence (B3): Skills recommendation ("Học React → nên học TypeScript")
- Không có → chỉ biết "React phổ biến" (shallow insight)

**Q3**: "Có thể skip phase nào không?"  
**A**: 
- Phase 1 (Nhóm A): **KHÔNG THỂ SKIP** - fundamental distributions
- Phase 2 (Nhóm B): **NÊN LÀM** - skills là key value của dataset
- Phase 3 (Nhóm C): Optional nếu không quan tâm companies
- Phase 4 (Nhóm D): **NÊN LÀM** - geo insights rất quan trọng
- Phase 5: Optional nhưng nên có summary

**Recommended minimum**: Phase 1 + Phase 2 + Phase 4 (10/16 questions)

---

**Ready to implement!** 🚀
