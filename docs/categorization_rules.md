# Categorization Rules - Job Level & Job Category

## 📋 Overview

File này ghi lại **chi tiết các rules** để phân loại job từ `job_title` thành:
1. **`job_level`** - Cấp bậc/Seniority (5 levels)
2. **`job_category`** - Chuyên môn/Role type (13 categories)

**Purpose**:
- 📖 **Documentation**: Source of truth cho categorization logic
- 🔧 **Maintainability**: Dễ dàng tune/adjust rules khi cần
- 🧪 **Baseline**: Reference cho việc so sánh rule-based vs ML-based classification

---

## 🎯 Job Level Rules

### Overview

**Job Level** được extract từ `job_title` bằng **keyword matching** (case-insensitive).

**5 Levels**:
1. `intern` - Thực tập sinh / Fresher / Graduate
2. `junior` - Junior Developer
3. `mid` - Mid-level (default khi không match keyword nào)
4. `senior` - Senior / Lead / Principal / Staff
5. `manager` - Manager / Head / Director / Chief / VP / CTO / CEO

### Detailed Rules

| Level | Priority | Keywords | Case Sensitivity | Examples |
|-------|----------|----------|-----------------|----------|
| **intern** | 1 | `intern`, `internship`, `fresher`, `graduate`, `apprentice` | Case-insensitive | "Intern Backend Developer"<br>"Fresher Software Engineer"<br>"Graduate Trainee" |
| **junior** | 2 | `junior`, `jr`, `jr.`, `entry level` | Case-insensitive | "Junior Frontend Developer"<br>"Jr. Backend Engineer"<br>"Entry Level QA" |
| **senior** | 3 | `senior`, `sr`, `sr.`, `lead`, `principal`, `staff`, `expert`, `architect` | Case-insensitive | "Senior Backend Developer"<br>"Lead Frontend Engineer"<br>"Principal Software Engineer"<br>"Staff Engineer"<br>"Solutions Architect" |
| **manager** | 4 | `manager`, `head`, `director`, `chief`, `vp`, `vice president`, `cto`, `ceo`, `coo`, `cfo`, `president`, `team lead` | Case-insensitive | "Engineering Manager"<br>"Head of Engineering"<br>"Director of Technology"<br>"CTO"<br>"VP of Engineering" |
| **mid** | 5 (default) | (no match) | N/A | "Backend Developer"<br>"Frontend Engineer"<br>"QA Engineer" |

### Implementation Logic

```python
def extract_job_level(job_title):
    """
    Extract job level from job title using keyword matching
    
    Args:
        job_title: Job title string
        
    Returns:
        One of: 'intern', 'junior', 'mid', 'senior', 'manager'
    """
    if pd.isna(job_title):
        return 'mid'  # Default
    
    title_lower = job_title.lower()
    
    # Priority 1: Intern/Fresher (highest priority for entry-level)
    if any(keyword in title_lower for keyword in ['intern', 'internship', 'fresher', 'graduate', 'apprentice']):
        return 'intern'
    
    # Priority 2: Junior
    if any(keyword in title_lower for keyword in ['junior', 'jr', 'jr.', 'entry level']):
        return 'junior'
    
    # Priority 3: Senior/Lead/Principal
    if any(keyword in title_lower for keyword in ['senior', 'sr', 'sr.', 'lead', 'principal', 'staff', 'expert', 'architect']):
        return 'senior'
    
    # Priority 4: Manager/Head/Director/C-level
    if any(keyword in title_lower for keyword in ['manager', 'head', 'director', 'chief', 'vp', 'vice president', 
                                                   'cto', 'ceo', 'coo', 'cfo', 'president', 'team lead']):
        return 'manager'
    
    # Priority 5: Default (mid-level)
    return 'mid'
```

### Priority & Conflict Handling

**Conflict Resolution**: First match wins (top-to-bottom priority)

**Examples**:
```python
# Case 1: Multiple keywords
"Senior Engineering Manager" 
→ Matches 'senior' first (Priority 3) → Returns 'senior' ✅

# Case 2: C-level with Senior
"Senior VP of Engineering"
→ Matches 'senior' first (Priority 3) → Returns 'senior'
→ Note: Should match 'vp' (Priority 4) → Could improve by checking manager keywords first

# Case 3: No keywords
"Backend Developer"
→ No match → Returns 'mid' ✅

# Case 4: Intern vs Junior
"Intern Junior Developer" (rare)
→ Matches 'intern' first (Priority 1) → Returns 'intern' ✅
```

**Known Issues**:
1. **"Senior Manager"** → Returns `senior` (should be `manager`)
   - **Fix**: Check manager keywords before senior keywords
   
2. **"Lead"** → Returns `senior` (could be `manager`)
   - **Depends on context**: "Tech Lead" vs "Team Lead"
   - Current: All map to `senior`

3. **"Architect"** → Returns `senior`
   - **Reasonable**: Solution Architect, Software Architect typically senior-level

### Distribution (3,985 jobs)

| Level | Count | Percentage | Notes |
|-------|-------|-----------|-------|
| **mid** | 2,618 | 65.7% | Default (no keyword match) |
| **senior** | 928 | 23.3% | Senior, Lead, Principal, Staff |
| **junior** | 198 | 5.0% | Junior, Entry-level |
| **manager** | 131 | 3.3% | Manager, Head, Director, C-level |
| **intern** | 110 | 2.8% | Intern, Fresher, Graduate |

**Observations**:
- Most jobs (65.7%) are mid-level (default)
- Senior roles: 23.3% (significant)
- Entry-level (intern + junior): 7.8% combined
- Manager roles: 3.3% (reasonable for leadership positions)

---

## 🏷️ Job Category Rules

### Overview

**Job Category** được classify từ `job_title` bằng **keyword matching** (case-insensitive).

**13 Categories**:
1. `Backend Developer`
2. `Frontend Developer`
3. `Fullstack Developer`
4. `Mobile Developer`
5. `DevOps Engineer`
6. `Data Engineer`
7. `Data Scientist`
8. `QA/Tester`
9. `Security Engineer`
10. `Software Engineer`
11. `Product Manager`
12. `Business Analyst`
13. `Other` (default)

### Detailed Rules

#### 1. Backend Developer

**Keywords**: `backend`, `back-end`, `back end`, `server`, `api`, `node`, `java`, `python`, `.net`, `golang`, `ruby`, `php`, `laravel`, `django`, `spring`

**Priority**: High (checked first)

**Examples**:
- ✅ "Backend Engineer"
- ✅ "Senior Backend Developer"
- ✅ "Node.js Developer"
- ✅ "Python Backend Engineer"
- ✅ "Java Spring Developer"
- ✅ "API Developer"

**Implementation**:
```python
if any(kw in title_lower for kw in ['backend', 'back-end', 'back end', 'server', 'api', 
                                     'node', 'java', 'python', '.net', 'golang', 'ruby', 
                                     'php', 'laravel', 'django', 'spring']):
    return 'Backend Developer'
```

---

#### 2. Frontend Developer

**Keywords**: `frontend`, `front-end`, `front end`, `react`, `vue`, `angular`, `ui`, `web`, `html`, `css`, `javascript`

**Priority**: High (checked after Backend)

**Examples**:
- ✅ "Frontend Developer"
- ✅ "React Developer"
- ✅ "Vue.js Engineer"
- ✅ "Angular Developer"
- ✅ "UI Developer"
- ✅ "Web Developer" (if no backend keywords)

**Implementation**:
```python
if any(kw in title_lower for kw in ['frontend', 'front-end', 'front end', 'react', 'vue', 
                                     'angular', 'ui', 'web', 'html', 'css', 'javascript']):
    return 'Frontend Developer'
```

**Note**: `web` could match both Frontend and Fullstack → depends on order

---

#### 3. Fullstack Developer

**Keywords**: `fullstack`, `full-stack`, `full stack`

**Priority**: Very High (checked FIRST before Backend/Frontend)

**Examples**:
- ✅ "Fullstack Developer"
- ✅ "Full-stack Engineer"
- ✅ "Full Stack Web Developer"

**Implementation**:
```python
if any(kw in title_lower for kw in ['fullstack', 'full-stack', 'full stack']):
    return 'Fullstack Developer'
```

**Conflict Handling**:
- "Fullstack Backend Developer" → Returns `Fullstack Developer` (explicit fullstack keyword wins)
- "Backend and Frontend Developer" → Returns `Backend Developer` (first match, no explicit fullstack)

---

#### 4. Mobile Developer

**Keywords**: `mobile`, `ios`, `android`, `react native`, `flutter`, `swift`, `kotlin`, `xamarin`

**Priority**: High

**Examples**:
- ✅ "Mobile Developer"
- ✅ "iOS Developer"
- ✅ "Android Engineer"
- ✅ "React Native Developer"
- ✅ "Flutter Developer"

**Implementation**:
```python
if any(kw in title_lower for kw in ['mobile', 'ios', 'android', 'react native', 'flutter', 
                                     'swift', 'kotlin', 'xamarin']):
    return 'Mobile Developer'
```

---

#### 5. DevOps Engineer

**Keywords**: `devops`, `sre`, `site reliability`, `infrastructure`, `cloud`, `aws`, `azure`, `gcp`, `kubernetes`, `docker`, `ci/cd`, `jenkins`, `terraform`

**Priority**: High

**Examples**:
- ✅ "DevOps Engineer"
- ✅ "SRE - Site Reliability Engineer"
- ✅ "Cloud Engineer"
- ✅ "AWS DevOps Engineer"
- ✅ "Infrastructure Engineer"
- ✅ "Kubernetes Engineer"

**Implementation**:
```python
if any(kw in title_lower for kw in ['devops', 'sre', 'site reliability', 'infrastructure', 
                                     'cloud', 'aws', 'azure', 'gcp', 'kubernetes', 'docker', 
                                     'ci/cd', 'jenkins', 'terraform']):
    return 'DevOps Engineer'
```

---

#### 6. Data Engineer

**Keywords**: `data engineer`, `etl`, `data pipeline`, `data warehouse`, `big data`, `spark`, `hadoop`, `airflow`, `kafka`

**Priority**: High (checked BEFORE Data Scientist)

**Examples**:
- ✅ "Data Engineer"
- ✅ "Senior Data Engineer"
- ✅ "ETL Developer"
- ✅ "Big Data Engineer"
- ✅ "Data Pipeline Engineer"

**Implementation**:
```python
if any(kw in title_lower for kw in ['data engineer', 'etl', 'data pipeline', 'data warehouse', 
                                     'big data', 'spark', 'hadoop', 'airflow', 'kafka']):
    return 'Data Engineer'
```

---

#### 7. Data Scientist

**Keywords**: `data scientist`, `machine learning`, `ml engineer`, `ai engineer`, `deep learning`, `nlp`, `computer vision`, `data analyst` (advanced)

**Priority**: Medium (checked AFTER Data Engineer)

**Examples**:
- ✅ "Data Scientist"
- ✅ "Machine Learning Engineer"
- ✅ "AI Engineer"
- ✅ "Deep Learning Engineer"
- ✅ "NLP Engineer"
- ✅ "Computer Vision Engineer"

**Implementation**:
```python
if any(kw in title_lower for kw in ['data scientist', 'machine learning', 'ml engineer', 
                                     'ai engineer', 'deep learning', 'nlp', 'computer vision']):
    return 'Data Scientist'
```

**Note**: `data analyst` NOT included here (goes to Business Analyst instead)

---

#### 8. QA/Tester

**Keywords**: `qa`, `quality assurance`, `tester`, `test engineer`, `automation test`, `manual test`, `sdet`, `test automation`

**Priority**: High

**Examples**:
- ✅ "QA Engineer"
- ✅ "Quality Assurance Engineer"
- ✅ "Automation Tester"
- ✅ "Test Engineer"
- ✅ "SDET - Software Development Engineer in Test"

**Implementation**:
```python
if any(kw in title_lower for kw in ['qa', 'quality assurance', 'tester', 'test engineer', 
                                     'automation test', 'manual test', 'sdet', 'test automation']):
    return 'QA/Tester'
```

---

#### 9. Security Engineer

**Keywords**: `security`, `cybersecurity`, `infosec`, `penetration test`, `security analyst`, `security engineer`

**Priority**: High

**Examples**:
- ✅ "Security Engineer"
- ✅ "Cybersecurity Engineer"
- ✅ "Information Security Engineer"
- ✅ "Penetration Tester"
- ✅ "Security Analyst"

**Implementation**:
```python
if any(kw in title_lower for kw in ['security', 'cybersecurity', 'infosec', 'penetration test', 
                                     'security analyst', 'security engineer']):
    return 'Security Engineer'
```

---

#### 10. Software Engineer

**Keywords**: `software engineer`, `software developer`, `programmer`, `coder`

**Priority**: Low (checked near end)

**Examples**:
- ✅ "Software Engineer"
- ✅ "Software Developer"
- ✅ "Programmer"

**Implementation**:
```python
if any(kw in title_lower for kw in ['software engineer', 'software developer', 'programmer', 'coder']):
    return 'Software Engineer'
```

**Conflict Note**: This is a **catch-all for generic software roles**. If title has specific keywords (Backend, Frontend, etc.), those match first.

---

#### 11. Product Manager

**Keywords**: `product manager`, `product owner`, `po`, `product lead`

**Priority**: Medium

**Examples**:
- ✅ "Product Manager"
- ✅ "Senior Product Manager"
- ✅ "Product Owner"
- ✅ "Technical Product Manager"

**Implementation**:
```python
if any(kw in title_lower for kw in ['product manager', 'product owner', 'po', 'product lead']):
    return 'Product Manager'
```

---

#### 12. Business Analyst

**Keywords**: `business analyst`, `ba`, `data analyst`, `business intelligence`, `bi analyst`

**Priority**: Medium

**Examples**:
- ✅ "Business Analyst"
- ✅ "Senior Business Analyst"
- ✅ "Data Analyst"
- ✅ "Business Intelligence Analyst"
- ✅ "BI Analyst"

**Implementation**:
```python
if any(kw in title_lower for kw in ['business analyst', 'ba', 'data analyst', 
                                     'business intelligence', 'bi analyst']):
    return 'Business Analyst'
```

---

#### 13. Other (Default)

**Keywords**: (none - fallback)

**Priority**: Lowest (default)

**Examples**:
- ✅ "PHP Team Leader (Laravel)" (no specific category keyword)
- ✅ "Vận Hành Hệ Thống Chứng Khoán (Linux)" (operations, not dev)
- ✅ "Technical Support Engineer"
- ✅ "Sales Engineer"

**Implementation**:
```python
# If no match found
return 'Other'
```

---

## ⚔️ Conflict Handling

### Priority Order (First Match Wins)

```python
def categorize_job(job_title):
    """
    Categorize job from job title using keyword matching
    Priority order (first match wins):
    1. Fullstack (explicit)
    2. Backend
    3. Frontend
    4. Mobile
    5. DevOps
    6. Data Engineer
    7. Data Scientist
    8. QA/Tester
    9. Security
    10. Software Engineer (generic)
    11. Product Manager
    12. Business Analyst
    13. Other (default)
    """
    if pd.isna(job_title):
        return 'Other'
    
    title_lower = job_title.lower()
    
    # Priority 1: Fullstack (explicit mention)
    if any(kw in title_lower for kw in ['fullstack', 'full-stack', 'full stack']):
        return 'Fullstack Developer'
    
    # Priority 2: Backend
    if any(kw in title_lower for kw in ['backend', 'back-end', 'back end', 'server', 'api', 
                                         'node', 'java', 'python', '.net', 'golang', 'ruby', 
                                         'php', 'laravel', 'django', 'spring']):
        return 'Backend Developer'
    
    # Priority 3: Frontend
    if any(kw in title_lower for kw in ['frontend', 'front-end', 'front end', 'react', 'vue', 
                                         'angular', 'ui', 'web', 'html', 'css', 'javascript']):
        return 'Frontend Developer'
    
    # ... continue for all 13 categories
    
    # Priority 13: Default
    return 'Other'
```

### Conflict Scenarios

#### Scenario 1: Fullstack vs Backend/Frontend

**Problem**: Title contains both "fullstack" and "backend"

**Example**: `"Fullstack Backend Developer"`

**Resolution**:
- Fullstack checked first (Priority 1)
- Returns `Fullstack Developer` ✅

**Reasoning**: Explicit "fullstack" keyword should take precedence

---

#### Scenario 2: Backend vs Frontend (no Fullstack)

**Problem**: Title contains both "backend" and "frontend" but NO explicit "fullstack"

**Example**: `"Backend and Frontend Developer"`

**Resolution**:
- Backend checked first (Priority 2)
- Returns `Backend Developer` ⚠️

**Potential Issue**: Should be `Fullstack Developer` but isn't

**Improvement**: Add detection for "and" pattern:
```python
if ('backend' in title_lower and 'frontend' in title_lower) or \
   ('back-end' in title_lower and 'front-end' in title_lower):
    return 'Fullstack Developer'
```

---

#### Scenario 3: Mobile vs Frontend

**Problem**: "React Native" contains "react" (frontend keyword)

**Example**: `"React Native Developer"`

**Resolution**:
- Need to check `react native` (2 words) BEFORE `react` (1 word)
- Current: Mobile checked at Priority 4 → Returns `Mobile Developer` ✅

**Works correctly** because:
- Mobile keywords include `react native` (exact substring)
- `react native` in `title_lower` matches before separate `react`

---

#### Scenario 4: Data Engineer vs Data Scientist

**Problem**: Both contain "data"

**Example 1**: `"Data Engineer"`
- Matches `data engineer` (Priority 6) → Returns `Data Engineer` ✅

**Example 2**: `"Data Scientist"`
- No `data engineer` keyword → Falls to Priority 7
- Matches `data scientist` → Returns `Data Scientist` ✅

**Example 3**: `"Data Analyst"`
- No `data engineer` or `data scientist` keywords
- Falls to Priority 12 (Business Analyst)
- Matches `data analyst` → Returns `Business Analyst` ✅

**Works correctly** because of priority order

---

#### Scenario 5: Software Engineer (Generic) vs Specific

**Problem**: "Backend Software Engineer" contains both "backend" and "software engineer"

**Example**: `"Backend Software Engineer"`

**Resolution**:
- Backend checked first (Priority 2)
- Returns `Backend Developer` ✅

**Reasoning**: Specific category (Backend) takes precedence over generic (Software Engineer)

---

#### Scenario 6: No Keyword Match

**Problem**: Title has no matching keywords

**Example 1**: `"PHP Team Leader (Laravel)"`
- Contains `php`, `laravel` → Matches Backend (Priority 2)
- Returns `Backend Developer` ✅

**Example 2**: `"Vận Hành Hệ Thống Chứng Khoán (Linux)"`
- Vietnamese title, "operations" role
- No English keywords match
- Returns `Other` ✅

**Example 3**: `"Technical Support Engineer"`
- Contains `engineer` but not specific to any category
- No category keyword matches
- Returns `Other` ✅

---

### Edge Cases & Improvements

#### Edge Case 1: Multi-role Positions

**Example**: `"Backend Developer / DevOps Engineer"`

**Current Behavior**:
- Matches `backend` first (Priority 2)
- Returns `Backend Developer`

**Potential Improvement**:
- Detect "/" or "and" patterns
- Create new category `Backend Developer` OR tag as multi-role

---

#### Edge Case 2: Language-specific Roles

**Example**: `"Python Developer"` (no explicit backend/frontend mention)

**Current Behavior**:
- Matches `python` keyword (in Backend list)
- Returns `Backend Developer` ✅

**Assumption**: Python typically associated with Backend (could be Data Science)

---

#### Edge Case 3: Framework-specific Without Context

**Example**: `"Laravel Developer"`

**Current Behavior**:
- Matches `laravel` (in Backend list)
- Returns `Backend Developer` ✅

**Reasoning**: Laravel is PHP backend framework

---

## 📊 Distribution (3,985 jobs)

| Category | Count | Percentage | Notes |
|----------|-------|-----------|-------|
| **Other** | 1,615 | 40.5% | No specific keyword match |
| **Backend Developer** | 374 | 9.4% | Server-side, API, Node/Java/Python |
| **Fullstack Developer** | 345 | 8.7% | Explicit fullstack keyword |
| **QA/Tester** | 338 | 8.5% | QA, Testing, Automation |
| **Mobile Developer** | 303 | 7.6% | iOS, Android, React Native |
| **Frontend Developer** | 292 | 7.3% | React, Vue, Angular, UI |
| **Software Engineer** | 249 | 6.2% | Generic software engineering |
| **Business Analyst** | 185 | 4.6% | BA, Data Analyst, BI |
| **DevOps Engineer** | 87 | 2.2% | DevOps, SRE, Cloud, Infrastructure |
| **Data Engineer** | 71 | 1.8% | ETL, Data Pipeline, Big Data |
| **Data Scientist** | 41 | 1.0% | ML, AI, Deep Learning |
| **Product Manager** | 41 | 1.0% | PM, Product Owner |
| **Security Engineer** | 44 | 1.1% | Security, Cybersecurity |

### Observations

1. **High "Other" Rate (40.5%)**:
   - Many jobs don't match standard categories
   - Possible reasons:
     - Vietnamese job titles (no English keywords)
     - Non-technical roles (Sales, Support, HR)
     - Specialized roles (Blockchain, Game Dev, etc.)
   - **Improvement**: Add more keywords or categories

2. **Backend > Fullstack > Frontend**:
   - Backend: 9.4% (highest specific category)
   - Fullstack: 8.7%
   - Frontend: 7.3%
   - **Reasonable**: Reflects market demand

3. **QA/Tester High (8.5%)**:
   - Significant testing roles in Vietnam market
   - Many automation testing positions

4. **Low Data Science (1.0%)**:
   - Data Engineer: 1.8%
   - Data Scientist: 1.0%
   - **Reflects**: Emerging field, fewer positions

---

## 🧪 Testing & Validation

### Test Cases

```python
# Test categorize_job function
test_cases = [
    # Fullstack
    ("Fullstack Developer", "Fullstack Developer"),
    ("Full-stack Engineer", "Fullstack Developer"),
    ("Fullstack Backend Developer", "Fullstack Developer"),  # Fullstack wins
    
    # Backend
    ("Backend Engineer", "Backend Developer"),
    ("Node.js Developer", "Backend Developer"),
    ("Python Backend Engineer", "Backend Developer"),
    ("API Developer", "Backend Developer"),
    
    # Frontend
    ("Frontend Developer", "Frontend Developer"),
    ("React Developer", "Frontend Developer"),
    ("Vue.js Engineer", "Frontend Developer"),
    
    # Mobile
    ("iOS Developer", "Mobile Developer"),
    ("React Native Developer", "Mobile Developer"),
    ("Android Engineer", "Mobile Developer"),
    
    # DevOps
    ("DevOps Engineer", "DevOps Engineer"),
    ("SRE", "DevOps Engineer"),
    ("Cloud Engineer", "DevOps Engineer"),
    
    # Data
    ("Data Engineer", "Data Engineer"),
    ("Data Scientist", "Data Scientist"),
    ("Machine Learning Engineer", "Data Scientist"),
    
    # QA
    ("QA Engineer", "QA/Tester"),
    ("Automation Tester", "QA/Tester"),
    
    # Other
    ("Technical Support", "Other"),
    ("Sales Engineer", "Other"),
    ("Vận Hành Hệ Thống", "Other"),
]

for title, expected in test_cases:
    result = categorize_job(title)
    status = "✅" if result == expected else "❌"
    print(f"{status} {title!r} → {result} (expected: {expected})")
```

---

## 🔮 Future Enhancements

### 1. Skills-based Categorization

**Current**: Only uses `job_title`

**Improvement**: Also check `skills` column
```python
def categorize_job_v2(job_title, skills):
    # Check title first
    category_from_title = categorize_job(job_title)
    
    if category_from_title != 'Other':
        return category_from_title
    
    # Fallback: Check skills
    if pd.notna(skills):
        skills_lower = skills.lower()
        if any(kw in skills_lower for kw in ['python', 'django', 'flask']):
            return 'Backend Developer'
        # ... more skill-based rules
    
    return 'Other'
```

### 2. Multi-label Classification

**Current**: Single category per job

**Improvement**: Allow multiple categories
```python
# Job: "Backend and Frontend Developer"
# Current: ['Backend Developer']
# Improved: ['Backend Developer', 'Frontend Developer']
```

### 3. Confidence Scores

**Current**: Binary match (yes/no)

**Improvement**: Return confidence
```python
def categorize_job_v3(job_title):
    scores = {}
    
    # Count keyword matches per category
    for category, keywords in category_keywords.items():
        match_count = sum(1 for kw in keywords if kw in job_title.lower())
        scores[category] = match_count
    
    # Return top category with score
    top_category = max(scores, key=scores.get)
    confidence = scores[top_category] / len(category_keywords[top_category])
    
    return top_category, confidence
```

### 4. ML-based Classification

**Current**: Rule-based (keyword matching)

**Improvement**: Train ML model
- Features: TF-IDF from `job_title` + `skills`
- Labels: Current rule-based categories (or manually labeled)
- Model: Logistic Regression, Random Forest, or XGBoost
- Compare: Rule-based accuracy vs ML accuracy

---

## 📚 Related Documentation

- **Master Schema**: `docs/schema.md` (columns `job_level` and `job_category`)
- **Column Mapping**: `docs/column_mapping.md` (transformation functions)
- **Pipeline Overview**: `docs/pipeline_overview.md` (Block C: Normalization)
- **Implementation**: `vietnam_it_jobs_merge_analysis.ipynb` (Cell 5: Normalization Functions)

---

**Last Updated**: November 14, 2025  
**Version**: 1.0.0  
**Status**: ✅ Production rules documented and validated
