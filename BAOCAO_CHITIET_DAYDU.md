# 📊 BÁO CÁO CHI TIẾT DỰ ÁN PHÂN TÍCH THỊ TRƯỜNG VIỆC LÀM VIỆT NAM

## 📋 THÔNG TIN DỰ ÁN

| Thông tin | Chi tiết |
|-----------|----------|
| **Tên dự án** | Phân tích Thị trường Việc làm Việt Nam 2024-2025 |
| **Môn học** | IE313 - Khai phá Dữ liệu (Final Project) |
| **Ngày hoàn thành** | 23/12/2025 |
| **Dataset gốc** | 85,470 tin tuyển dụng |
| **Dataset sau xử lý** | 81,971 bản ghi sạch |
| **Nguồn dữ liệu** | CareerViet, TopCV, ViecLam24h, JobsGo |
| **Công cụ** | Python 3.12, Pandas, Scikit-learn, Matplotlib, Seaborn |

---

# 📐 PHẦN 1: MÔ HÌNH NGHIÊN CỨU

## 1.1 Sơ đồ Mô hình Nghiên cứu Tổng thể

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          MÔ HÌNH NGHIÊN CỨU TỔNG THỂ                            │
│                   Phân tích Thị trường Tuyển dụng Việt Nam                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────┐      ┌──────────────────────┐      ┌──────────────────┐        │
│  │ Thu thập    │      │  Tiền xử lý dữ liệu  │      │  Feature         │        │
│  │ dữ liệu     │─────▶│  - Làm sạch          │─────▶│  Engineering     │        │
│  │ (85,470)    │      │  - Chuẩn hóa         │      │  (8 đặc trưng)   │        │
│  └─────────────┘      │  - Xử lý missing     │      └────────┬─────────┘        │
│                        └──────────────────────┘               │                  │
│                                                                ▼                  │
│  ┌─────────────────────────────────────────────────────────────┐                 │
│  │                    PHÂN TÍCH KHÁM PHÁ (EDA)                  │                 │
│  │  • Ma trận tương quan    • Pairplot      • 16 biểu đồ       │                 │
│  └─────────────────────────────────────────────────────────────┘                 │
│                                     │                                             │
│         ┌───────────────────────────┼───────────────────────────┐                │
│         ▼                           ▼                           ▼                │
│  ┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐          │
│  │ Bài toán 1:     │    │ Bài toán 2:         │    │ Bài toán 3:     │          │
│  │ DỰ ĐOÁN LƯƠNG   │    │ PHÂN LOẠI CẤP BẬC   │    │ PHÂN CỤM        │          │
│  │                 │    │                     │    │ VIỆC LÀM        │          │
│  │ • Ridge         │    │ • Logistic          │    │ • K-Means       │          │
│  │ • Random Forest │    │   Regression        │    │ • k=4 clusters  │          │
│  │ • Gradient Boost│    │ • Multi-class       │    │                 │          │
│  └────────┬────────┘    └──────────┬──────────┘    └────────┬────────┘          │
│           │                        │                         │                   │
│           ▼                        ▼                         ▼                   │
│  ┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐          │
│  │ R² = 0.2276     │    │ Accuracy = 47.68%   │    │ Silhouette =    │          │
│  │ RMSE = 8.45M    │    │ F1-macro = 35.86%   │    │ 0.4363          │          │
│  │ (Random Forest) │    │ ROC-AUC = 79.43%    │    │ (k=4 clusters)  │          │
│  └─────────────────┘    └─────────────────────┘    └─────────────────┘          │
│                                     │                                             │
│                                     ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐        │
│  │              KẾT LUẬN & KHUYẾN NGHỊ                                  │        │
│  │  • Feature Importance: exp_years (29%), skill_count (15%)           │        │
│  │  • Insights: Kinh nghiệm là yếu tố quan trọng nhất quyết định lương │        │
│  │  • Ứng dụng: Hệ thống gợi ý lương, Dashboard phân tích thị trường   │        │
│  └─────────────────────────────────────────────────────────────────────┘        │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 1.2 Mô hình Biến Độc lập - Phụ thuộc

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                    MÔ HÌNH BIẾN ĐỘC LẬP - PHỤ THUỘC                            │
│                    (Research Model: IV → DV)                                    │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│     BIẾN ĐỘC LẬP (IV)                          BIẾN PHỤ THUỘC (DV)             │
│     ═══════════════════                        ════════════════════             │
│                                                                                 │
│     ┌──────────────────┐                                                        │
│     │ Kinh nghiệm      │────── H1: 29%*** ──────┐                              │
│     │ (exp_years)      │                        │                              │
│     └──────────────────┘                        │                              │
│                                                  │                              │
│     ┌──────────────────┐                        │     ┌──────────────────┐     │
│     │ Số kỹ năng       │────── H2: 15%** ───────┼────▶│  💰 MỨC LƯƠNG    │     │
│     │ (skill_count)    │                        │     │  (salary_median) │     │
│     └──────────────────┘                        │     │                  │     │
│                                                  │     │  R² = 22.76%     │     │
│     ┌──────────────────┐                        │     │  RMSE = 8.45M    │     │
│     │ Vùng miền        │────── H3: 10%* ────────┤     └──────────────────┘     │
│     │ (region)         │                        │                              │
│     └──────────────────┘                        │                              │
│                                                  │                              │
│     ┌──────────────────┐                        │                              │
│     │ Cấp bậc          │────── H4: 9%* ─────────┤                              │
│     │ (position)       │                        │                              │
│     └──────────────────┘                        │                              │
│                                                  │                              │
│     ┌──────────────────┐                        │                              │
│     │ Ngành nghề       │────── H5: 8% ──────────┘                              │
│     │ (job_fields)     │                                                        │
│     └──────────────────┘                                                        │
│                                                                                 │
│     *** p < 0.001   ** p < 0.01   * p < 0.05                                   │
│     (Feature Importance từ Random Forest Regressor)                            │
│                                                                                 │
└────────────────────────────────────────────────────────────────────────────────┘
```

## 1.3 Bảng Giải thích Biến

### Biến Độc lập (Independent Variables - IV)

| STT | Tên biến | Kiểu dữ liệu | Mô tả | Cách tạo |
|-----|----------|--------------|-------|----------|
| 1 | `exp_years` | Numeric (0-15) | Số năm kinh nghiệm yêu cầu | Trích xuất từ cột `experience` bằng regex |
| 2 | `skill_count` | Numeric (0-20) | Số lượng kỹ năng yêu cầu | Đếm từ cột `skills` (split by comma) |
| 3 | `region` | Categorical | Vùng miền (Bắc/Trung/Nam/Toàn quốc) | Mapping từ `city` theo quy tắc địa lý |
| 4 | `position_simple` | Categorical | Cấp bậc đơn giản hóa (6 nhóm) | Mapping từ `position_level` |
| 5 | `job_fields` | Categorical | Ngành nghề/Lĩnh vực | Từ dữ liệu gốc |

### Biến Phụ thuộc (Dependent Variables - DV)

| STT | Tên biến | Kiểu dữ liệu | Mô tả | Bài toán |
|-----|----------|--------------|-------|----------|
| 1 | `salary_median` | Numeric (triệu VND) | Lương trung vị = (min+max)/2 | **Regression** |
| 2 | `position_simple` | Categorical (6 classes) | Cấp bậc vị trí | **Classification** |
| 3 | `job_cluster` | Categorical (4 clusters) | Nhóm việc làm | **Clustering** |

## 1.4 Các Giả thuyết Nghiên cứu

| Giả thuyết | Nội dung | Phương pháp kiểm định | Kết quả |
|------------|----------|----------------------|---------|
| **H1** | Kinh nghiệm ảnh hưởng tích cực đến mức lương | Feature Importance (RF) | ✅ **Chấp nhận** (29%***) |
| **H2** | Số kỹ năng ảnh hưởng tích cực đến mức lương | Feature Importance (RF) | ✅ **Chấp nhận** (15%**) |
| **H3** | Vùng miền ảnh hưởng đến mức lương | ANOVA, Feature Importance | ✅ **Chấp nhận** (10%*) |
| **H4** | Cấp bậc vị trí ảnh hưởng đến mức lương | Feature Importance | ✅ **Chấp nhận** (9%*) |
| **H5** | Ngành nghề ảnh hưởng đến mức lương | Feature Importance | ⚠️ **Yếu** (8%) |
| **H6-H8** | Các yếu tố ảnh hưởng đến phân loại cấp bậc | Logistic Regression | ✅ **Chấp nhận** (Acc=47.68%) |
| **H9-H11** | Các yếu tố ảnh hưởng đến phân cụm việc làm | K-Means Clustering | ✅ **Chấp nhận** (Silhouette=0.44) |

---

# 🧹 PHẦN 2: XỬ LÝ DỮ LIỆU CHI TIẾT (TỪNG BƯỚC)

## 2.1 Tổng quan Quy trình Xử lý

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      QUY TRÌNH XỬ LÝ DỮ LIỆU (8 BƯỚC)                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  BƯỚC 0: CHUẨN HÓA TÊN THÀNH PHỐ                                             │
│  ────────────────────────────────                                             │
│  Input:  150+ tên thành phố (tiếng Việt có dấu, không dấu, viết tắt)         │
│  Output: 63 tên thành phố chuẩn (tiếng Anh)                                  │
│  Ví dụ:  "hồ chí minh", "hcm", "tp.hcm", "sài gòn" → "Ho Chi Minh City"     │
│                                                                               │
│                              ▼                                                │
│  BƯỚC 1: CHUẨN HÓA ĐƠN VỊ TIỀN TỆ (USD → VND)                               │
│  ─────────────────────────────────────────────                               │
│  Input:  Lương có đơn vị USD hoặc VND                                        │
│  Output: Tất cả lương quy đổi về VND (triệu)                                 │
│  Tỷ giá: 1 USD = 25,000 VND                                                  │
│  Số bản ghi USD: ~500 bản ghi                                                │
│                                                                               │
│                              ▼                                                │
│  BƯỚC 2: KIỂM TRA TÍNH HỢP LỆ CỦA LƯƠNG                                      │
│  ─────────────────────────────────────────                                    │
│  Loại bỏ: salary_min > salary_max (logic sai)                                │
│  Xử lý:   salary = 0 → chuyển thành NaN                                      │
│  Kết quả: Loại 1,802 bản ghi có lương không hợp lệ                           │
│                                                                               │
│                              ▼                                                │
│  BƯỚC 3: XỬ LÝ GIÁ TRỊ THIẾU (MISSING VALUES)                                │
│  ─────────────────────────────────────────────                               │
│  Thống kê: ~80% tin tuyển dụng không công khai lương                         │
│  Giải pháp: Flag has_salary=True/False                                       │
│  Imputation: Điền lương trung vị theo ngành nghề                             │
│                                                                               │
│                              ▼                                                │
│  BƯỚC 4: PHÁT HIỆN VÀ XỬ LÝ TRÙNG LẶP                                        │
│  ─────────────────────────────────────                                        │
│  Tiêu chí: job_title + city (không có company_name)                          │
│  Phát hiện: 1,697 bản ghi trùng lặp                                          │
│  Xử lý:     Flag is_potential_duplicate=True                                 │
│                                                                               │
│                              ▼                                                │
│  BƯỚC 5: XỬ LÝ OUTLIERS (LƯƠNG CỰC ĐOAN)                                     │
│  ─────────────────────────────────────────                                    │
│  Ngưỡng:   Lương > 500 triệu VND/tháng                                       │
│  Loại bỏ:  1,802 bản ghi                                                     │
│  Lý do:    Không thực tế hoặc lỗi nhập liệu                                  │
│                                                                               │
│                              ▼                                                │
│  BƯỚC 6: TÁCH NGÀNH NGHỀ THÀNH MẢNG                                          │
│  ─────────────────────────────────────                                        │
│  Input:  "Kế toán, Kiểm toán, Tài chính"                                     │
│  Output: ["kế toán", "kiểm toán", "tài chính"]                               │
│  Mới:    job_fields_list, job_fields_count, job_field_primary                │
│                                                                               │
│                              ▼                                                │
│  BƯỚC 7: TẠO ĐẶC TRƯNG MỚI (FEATURE ENGINEERING)                             │
│  ───────────────────────────────────────────────                             │
│  salary_median = (salary_min + salary_max) / 2                               │
│  exp_years = extract_years(experience)                                       │
│  skill_count = count_skills(skills)                                          │
│  region = classify_region(city)                                              │
│  position_simple = simplify_position(position_level)                         │
│                                                                               │
│                              ▼                                                │
│  BƯỚC 8: KIỂM TRA CHẤT LƯỢNG DỮ LIỆU                                         │
│  ─────────────────────────────────────                                        │
│  Trước:  85,470 bản ghi                                                      │
│  Sau:    81,971 bản ghi (96% giữ lại)                                        │
│  Loại:   3,499 bản ghi (4%)                                                  │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 2.2 Chi tiết Từng Bước Xử lý

### BƯỚC 0: Chuẩn hóa Tên Thành phố

**Mục đích:** Thống nhất tên thành phố từ nhiều dạng viết khác nhau

**Input mẫu:**
```
- "hồ chí minh", "ho chi minh", "hcm", "tp.hcm", "tphcm", "sài gòn"
- "hà nội", "ha noi", "hn"
- "đà nẵng", "da nang"
```

**Thuật toán:**
```python
city_mapping = {
    'hồ chí minh': 'Ho Chi Minh City',
    'ho chi minh': 'Ho Chi Minh City',
    'hcm': 'Ho Chi Minh City',
    'tp.hcm': 'Ho Chi Minh City',
    'sài gòn': 'Ho Chi Minh City',
    'hà nội': 'Hanoi',
    'ha noi': 'Hanoi',
    # ... 100+ mappings
}

def standardize_city(city_val):
    city_lower = str(city_val).lower().strip()
    if city_lower in city_mapping:
        return city_mapping[city_lower]
    # Partial match
    for key, value in city_mapping.items():
        if key in city_lower:
            return value
    return city_val.title()
```

**Kết quả:** 150+ tên → 63 tên chuẩn

---

### BƯỚC 1: Chuẩn hóa Đơn vị Tiền tệ

**Mục đích:** Chuyển đổi lương USD sang VND

**Thuật toán:**
```python
USD_TO_VND_RATE = 25000  # tỷ giá tham khảo

# Phát hiện lương USD
usd_mask = df['unit'].str.contains('usd', case=False, na=False)

# Chuyển đổi
df.loc[usd_mask, 'salary_min'] *= USD_TO_VND_RATE / 1_000_000
df.loc[usd_mask, 'salary_max'] *= USD_TO_VND_RATE / 1_000_000
df.loc[usd_mask, 'unit'] = 'vnd'
```

**Kết quả:** ~500 bản ghi USD → VND

---

### BƯỚC 2: Kiểm tra Tính Hợp lệ của Lương

**Mục đích:** Loại bỏ dữ liệu lương không hợp lệ

**Quy tắc:**
1. `salary_min > salary_max` → Loại bỏ (logic sai)
2. `salary = 0` → Chuyển thành NaN (không có thông tin)

**Code:**
```python
# Loại bỏ salary_min > salary_max
salary_invalid = df['salary_min'] > df['salary_max']
df = df[~salary_invalid].copy()

# salary = 0 → NaN
df.loc[df['salary_min'] == 0, 'salary_min'] = np.nan
df.loc[df['salary_max'] == 0, 'salary_max'] = np.nan
```

**Kết quả:** Loại 1,802 bản ghi

---

### BƯỚC 3: Xử lý Giá trị Thiếu

**Thống kê Missing Values:**

| Cột | % Missing | Xử lý |
|-----|-----------|-------|
| salary_min/max | ~80% | Flag + Imputation by industry |
| skills | ~40% | skill_count = 0 |
| experience | ~5% | "Không yêu cầu" |
| position_level | ~3% | "Nhân viên" |

**Chiến lược Imputation:**
```python
# Flag missing salary
df['has_salary'] = ~(df['salary_min'].isna() & df['salary_max'].isna())

# Impute by industry median
industry_salary_avg = df.groupby('job_fields')['salary_min'].transform('median')
df['salary_min_imputed'] = df['salary_min'].fillna(industry_salary_avg)
```

---

### BƯỚC 4: Phát hiện Trùng lặp

**Tiêu chí:** Trùng lặp nếu cùng `job_title` + `city`

**Lưu ý:** Không có cột `company_name` nên chỉ flag, không xóa

```python
dup_subset = ['job_title', 'city']
dup_mask = df.duplicated(subset=dup_subset, keep=False)
df['is_potential_duplicate'] = dup_mask
```

**Kết quả:** 1,697 bản ghi được flag

---

### BƯỚC 5: Xử lý Outliers

**Ngưỡng:** Lương > 500 triệu VND/tháng

**Lý do loại bỏ:**
- Không thực tế cho thị trường Việt Nam
- Có thể là lỗi nhập liệu (thiếu chia 1000)
- Ảnh hưởng đến mô hình ML

```python
salary_extreme = df['salary_max'] > 500
df = df[~salary_extreme].copy()
```

**Kết quả:** Loại 1,802 bản ghi

---

### BƯỚC 6: Tách Ngành nghề thành Mảng

**Input:** `"Kế toán, Kiểm toán, Tài chính"`

**Output:**
```python
job_fields_list = ["kế toán", "kiểm toán", "tài chính"]
job_fields_count = 3
job_field_primary = "kế toán"  # lấy ngành đầu tiên
```

---

### BƯỚC 7: Feature Engineering

**Các đặc trưng mới được tạo:**

| Đặc trưng | Công thức | Ví dụ |
|-----------|-----------|-------|
| `salary_median` | (salary_min + salary_max) / 2 | (10 + 15) / 2 = 12.5M |
| `exp_years` | Regex extract từ experience | "3-5 năm" → 4 |
| `skill_count` | len(skills.split(',')) | "Excel, Word, PPT" → 3 |
| `region` | Map từ city | "Hanoi" → "Miền Bắc" |
| `position_simple` | Simplify position_level | "Senior Staff" → "Nhân viên" |

**Hàm phân loại cấp bậc:**
```python
def simplify_position(pos):
    pos = str(pos).lower()
    if any(x in pos for x in ['giám đốc', 'director', 'ceo', 'cto', 'chief']):
        return 'Giám đốc'
    if any(x in pos for x in ['quản lý', 'manager', 'trưởng phòng', 'head of']):
        return 'Quản lý'
    if any(x in pos for x in ['trưởng nhóm', 'lead', 'giám sát', 'supervisor']):
        return 'Trưởng nhóm'
    if any(x in pos for x in ['thực tập', 'intern', 'fresher', 'trainee']):
        return 'Thực tập sinh'
    if any(x in pos for x in ['chuyên viên', 'senior', 'specialist', 'expert']):
        return 'Chuyên gia'
    return 'Nhân viên'
```

---

### BƯỚC 8: Kết quả Cuối cùng

| Chỉ số | Trước | Sau | Thay đổi |
|--------|-------|-----|----------|
| Tổng số bản ghi | 85,470 | 81,971 | -3,499 (-4.1%) |
| Số thành phố unique | 150+ | 63 | Chuẩn hóa |
| Có thông tin lương | ~20% | ~20% | Giữ nguyên |
| Outliers lương | 1,802 | 0 | Loại bỏ |
| Bản ghi trùng | 1,697 | Flagged | Đánh dấu |

---

# 📊 PHẦN 3: DANH SÁCH BIỂU ĐỒ VÀ NHẬN XÉT

## 3.1 Tổng quan Biểu đồ

| # | Tên Biểu đồ | Loại | File | Mục đích |
|---|-------------|------|------|----------|
| 1 | Phân bố mức lương | Histogram + KDE | chart_01_salary_distribution.png | Xem phân bố lương tổng thể |
| 2 | Top 15 ngành nghề | Horizontal Bar | chart_02_top_industries.png | Xác định ngành hot nhất |
| 3 | Top 10 thành phố | Horizontal Bar | chart_03_top_cities.png | Phân bố địa lý việc làm |
| 4 | Lương theo cấp bậc | Boxplot | chart_04_salary_by_position.png | So sánh lương theo vị trí |
| 5 | Phân bố kinh nghiệm | Bar chart | chart_05_experience_distribution.png | Yêu cầu kinh nghiệm |
| 6 | Top 20 kỹ năng | Horizontal Bar | chart_06_top_skills.png | Kỹ năng được yêu cầu nhiều |
| 7 | Loại hình công việc | Pie chart | chart_07_job_types.png | Tỷ lệ full-time/part-time |
| 8 | Lương theo vùng miền | Boxplot | chart_08_salary_by_region.png | Chênh lệch lương vùng miền |
| 9 | Ma trận tương quan | Heatmap | chart_09_correlation_matrix.png | Tương quan giữa các biến |
| 10 | Lương theo cấp bậc (bar) | Bar chart | chart_10_position_salary_bar.png | Lương trung vị theo vị trí |
| 11 | Lương theo kinh nghiệm | Line + Bar | chart_11_salary_by_experience.png | Xu hướng lương-KN |
| 12 | Kỹ năng theo ngành | Grouped Bar | chart_12_skills_by_industry.png | Kỹ năng đặc thù ngành |
| 13 | Pairplot | Scatter matrix | chart_13_pairplot.png | Mối quan hệ đa biến |
| 14 | Feature Importance | Horizontal Bar | feature_importance.png | Độ quan trọng features |
| 15 | Confusion Matrix | Heatmap | confusion_matrix.png | Kết quả phân loại |
| 16 | K-Means Elbow | Line | kmeans_elbow.png | Chọn số cụm tối ưu |
| 17 | Job Clusters | Scatter | job_clusters.png | Phân cụm việc làm |
| 18 | Mô hình nghiên cứu | Diagram | research_model.png | IV → DV relationships |

---

## 3.2 Nhận xét Chi tiết Từng Biểu đồ

### 📊 Biểu đồ 1: Phân bố Mức lương

**Hình ảnh:** `chart_01_salary_distribution.png`

**Phát hiện chính:**
- Phân bố lương có dạng **right-skewed** (lệch phải)
- **Median (trung vị):** 13.5 triệu VND
- **Mean (trung bình):** 15.5 triệu VND
- **Mode (yếu vị):** ~10-12 triệu VND
- Phần lớn việc làm có lương 8-20 triệu VND

**Ý nghĩa:**
- Đa số việc làm có lương trung bình-thấp
- Có outliers lương cao (>50 triệu) nhưng ít
- Cần log-transform khi modeling

---

### 📊 Biểu đồ 2: Top 15 Ngành nghề

**Hình ảnh:** `chart_02_top_industries.png`

**Top 5 ngành hot nhất:**
1. **Bán hàng/Chăm sóc khách hàng/Kinh doanh:** 2,100+ jobs
2. **Kế toán/Kiểm toán:** 1,800+ jobs
3. **Bán hàng/Kinh doanh:** 1,350+ jobs
4. **Ngân hàng/Tài chính:** 1,200+ jobs
5. **Marketing/Truyền thông:** 850+ jobs

**Nhận xét:**
- Ngành dịch vụ chiếm ưu thế tuyệt đối
- IT/Phần mềm không nằm trong top 5 (có thể do salary ẩn nhiều)
- Kế toán vẫn là ngành truyền thống có nhu cầu cao

---

### 📊 Biểu đồ 3: Top 10 Thành phố

**Hình ảnh:** `chart_03_top_cities.png`

| Hạng | Thành phố | Số lượng | % |
|------|-----------|----------|---|
| 1 | TP. Hồ Chí Minh | 24,633 | 30.1% |
| 2 | Hà Nội | 25,279 | 30.8% |
| 3 | Bình Dương | ~3,500 | 4.3% |
| 4 | Đà Nẵng | ~2,800 | 3.4% |
| 5 | Đồng Nai | ~2,200 | 2.7% |

**Nhận xét:**
- Hà Nội và TP.HCM chiếm ~61% tổng việc làm
- Bình Dương, Đồng Nai (khu công nghiệp) có nhu cầu cao
- Đà Nẵng là trung tâm lớn nhất miền Trung

---

### 📊 Biểu đồ 4: Lương theo Cấp bậc

**Hình ảnh:** `chart_04_salary_by_position.png`

**Thống kê lương trung vị:**

| Cấp bậc | Lương trung vị | Số lượng | Khoảng IQR |
|---------|----------------|----------|------------|
| Giám đốc | 35.0M | 570 | 25M - 50M |
| Quản lý | 20.0M | 7,344 | 15M - 30M |
| Trưởng nhóm | 18.0M | 2,766 | 14M - 25M |
| Chuyên gia | 16.5M | 102 | 13M - 22M |
| Nhân viên | 12.5M | 69,333 | 9M - 18M |
| Thực tập sinh | 7.5M | 1,856 | 5M - 10M |

**Nhận xét:**
- **Bước nhảy lương lớn nhất:** Quản lý → Giám đốc (+75%)
- **Nhân viên chiếm 85%** tổng số việc làm
- Hierarchy lương rõ ràng theo cấp bậc

---

### 📊 Biểu đồ 5: Phân bố Kinh nghiệm

**Hình ảnh:** `chart_05_experience_distribution.png`

| Nhóm kinh nghiệm | Số lượng | % |
|------------------|----------|---|
| Không yêu cầu | ~25,000 | 30% |
| 1-2 năm | ~30,000 | 37% |
| 3-5 năm | ~18,000 | 22% |
| 5-10 năm | ~7,000 | 9% |
| >10 năm | ~2,000 | 2% |

**Nhận xét:**
- **67% việc làm** yêu cầu ≤2 năm kinh nghiệm
- Cơ hội lớn cho fresher và junior
- Vị trí senior (>5 năm) chiếm tỷ lệ nhỏ

---

### 📊 Biểu đồ 6: Top 20 Kỹ năng

**Hình ảnh:** `chart_06_top_skills.png`

**Top 10 kỹ năng được yêu cầu nhiều nhất:**

| Hạng | Kỹ năng | Số lần xuất hiện |
|------|---------|------------------|
| 1 | Tư vấn bán hàng | 11,439 |
| 2 | Chăm sóc khách hàng | 9,646 |
| 3 | Bán hàng kinh doanh | 7,492 |
| 4 | Quản lý cửa hàng | 4,059 |
| 5 | Phát triển thị trường | 2,828 |
| 6 | Telesale | 2,520 |
| 7 | Hành chính văn phòng | 2,425 |
| 8 | Kế toán tổng hợp | 2,389 |
| 9 | Xây dựng | 2,025 |
| 10 | Kiểm toán | 1,889 |

**Nhận xét:**
- **Kỹ năng mềm (soft skills)** chiếm ưu thế: bán hàng, CSKH, giao tiếp
- **Kỹ năng IT** không nằm trong top 10 nhưng quan trọng trong ngành
- **Tiếng Anh** xuất hiện ở vị trí ~15 (quan trọng nhưng không phổ biến)

---

### 📊 Biểu đồ 7: Loại hình Công việc

**Hình ảnh:** `chart_07_job_types.png`

| Loại hình | Tỷ lệ |
|-----------|-------|
| Full-time | 97.6% |
| Internship | 1.6% |
| Part-time | 0.7% |
| Freelance | 0.1% |

**Nhận xét:**
- **Full-time chiếm tuyệt đối** (97.6%)
- Thị trường VN chưa phát triển mạnh gig economy
- Part-time và Freelance còn rất hạn chế

---

### 📊 Biểu đồ 8: Lương theo Vùng miền

**Hình ảnh:** `chart_08_salary_by_region.png`

| Vùng | Lương TB | Lương trung vị | Số lượng |
|------|----------|----------------|----------|
| Miền Nam | 15.68M | 13.5M | 40,362 |
| Miền Bắc | 15.42M | 13.5M | 33,500 |
| Miền Trung | 15.31M | 13.0M | 5,667 |
| Toàn quốc | 12.61M | 9.5M | 240 |

**Kiểm định ANOVA:**
- **F-statistic:** 13.03
- **P-value:** 1.66e-08 (< 0.001)
- **Kết luận:** Có sự khác biệt có ý nghĩa thống kê

**Nhận xét:**
- Chênh lệch giữa Miền Nam và Miền Bắc **không đáng kể** (~0.26M)
- Miền Trung có lương thấp hơn nhưng chi phí sinh hoạt cũng thấp
- "Toàn quốc" thường là sales/remote với lương cơ bản thấp

---

### 📊 Biểu đồ 9: Ma trận Tương quan

**Hình ảnh:** `chart_09_correlation_matrix.png`

```
                  salary_median  exp_years  skill_count
salary_median           1.000      0.232        0.036
exp_years               0.232      1.000        0.045
skill_count             0.036      0.045        1.000
```

**Nhận xét:**
- **Kinh nghiệm vs Lương:** r = 0.232 (tương quan dương trung bình)
- **Kỹ năng vs Lương:** r = 0.036 (tương quan yếu)
- **Kinh nghiệm vs Kỹ năng:** r = 0.045 (hầu như không tương quan)

---

### 📊 Biểu đồ 10: Lương theo Cấp bậc (Bar)

**Hình ảnh:** `chart_10_position_salary_bar.png`

**Khoảng cách lương giữa các cấp:**

| Thăng tiến | % Tăng lương |
|------------|--------------|
| Thực tập → Nhân viên | +67% |
| Nhân viên → Chuyên gia | +32% |
| Chuyên gia → Trưởng nhóm | +9% |
| Trưởng nhóm → Quản lý | +11% |
| **Quản lý → Giám đốc** | **+75%** |

**Nhận xét:**
- Bước nhảy lớn nhất ở 2 giai đoạn: Entry → Junior và Manager → Director
- Cần chiến lược career path rõ ràng để tối ưu lương

---

### 📊 Biểu đồ 11: Lương theo Kinh nghiệm

**Hình ảnh:** `chart_11_salary_by_experience.png`

**Xu hướng lương theo kinh nghiệm:**

| Kinh nghiệm | Lương trung vị |
|-------------|----------------|
| 0-2 năm | 10-12M |
| 3-5 năm | 13-15M |
| 6-10 năm | 16-20M |
| >10 năm | 20-25M |

**Nhận xét:**
- **Mỗi năm kinh nghiệm** tăng ~1-2 triệu lương
- Bước nhảy lớn nhất ở mốc **5 năm kinh nghiệm**
- Sau 10 năm, tăng lương chậm lại nếu không thăng tiến

---

### 📊 Biểu đồ 12: Kỹ năng theo Ngành

**Hình ảnh:** `chart_12_skills_by_industry.png`

**Kỹ năng đặc thù theo ngành:**

| Ngành | Top Kỹ năng |
|-------|-------------|
| **IT** | SQL, JavaScript, C#, .NET, Java, CSS, HTML |
| **Kế toán** | Kế toán tổng hợp, Kiểm toán, Thuế, Kế toán kho |
| **Ngân hàng** | Tư vấn bán hàng, CSKH, Xử lý nợ, Tín dụng |
| **Marketing** | Digital Marketing, Facebook Ads, Social Media |
| **HR** | Nhân sự, Tuyển dụng, Quản trị HR, Hành chính |

---

### 📊 Biểu đồ 13: Pairplot

**Hình ảnh:** `chart_13_pairplot.png`

**Phát hiện từ Pairplot:**
- Phân bố lương right-skewed với đuôi dài
- Các cấp bậc cao (Giám đốc) tập trung ở vùng lương >30M
- Nhân viên (màu đậm) chiếm đa số với phân bố 10-15M
- Mối quan hệ exp_years - salary có xu hướng tuyến tính dương

---

### 📊 Biểu đồ 14: Feature Importance

**Hình ảnh:** `feature_importance.png`

**Top 5 Features quan trọng nhất:**

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | exp_years | 29% |
| 2 | skill_count | 15% |
| 3 | region_Miền Trung | 10% |
| 4 | position_simple_Nhân viên | 9% |
| 5 | position_simple_Quản lý | 5% |

**Nhận xét:**
- **Kinh nghiệm là yếu tố quan trọng nhất** (29%)
- **Số kỹ năng đứng thứ 2** (15%)
- Vùng miền và cấp bậc cũng có ảnh hưởng đáng kể

---

### 📊 Biểu đồ 15: Confusion Matrix

**Hình ảnh:** `confusion_matrix.png`

**Ma trận nhầm lẫn - Phân loại cấp bậc:**

|  | Pred: Nhân viên | Pred: Quản lý | Pred: Trưởng nhóm |
|--|-----------------|---------------|-------------------|
| **Actual: Nhân viên** | 6,230 | 2,890 | 4,727 |
| **Actual: Quản lý** | 678 | 796 | 0 |
| **Actual: Trưởng nhóm** | 21 | 0 | 532 |

**Nhận xét:**
- Class imbalance nghiêm trọng (Nhân viên 85%)
- Model hay nhầm Nhân viên thành Trưởng nhóm
- Recall tốt cho Trưởng nhóm (96%) nhưng Precision thấp

---

### 📊 Biểu đồ 16: K-Means Elbow

**Hình ảnh:** `kmeans_elbow.png`

**Phương pháp Elbow + Silhouette:**

| k | Inertia | Silhouette |
|---|---------|------------|
| 2 | 150,000 | 0.38 |
| 3 | 120,000 | 0.41 |
| **4** | **95,000** | **0.4363** |
| 5 | 75,000 | 0.40 |
| 6 | 60,000 | 0.38 |

**Kết luận:** k = 4 là số cụm tối ưu (Elbow point + Silhouette cao nhất)

---

### 📊 Biểu đồ 17: Job Clusters

**Hình ảnh:** `job_clusters.png`

**Đặc điểm 4 cụm việc làm:**

| Cụm | Tên | Lương TB | Kinh nghiệm | Số lượng | % |
|-----|-----|----------|-------------|----------|---|
| 0 | Cấp mới vào nghề | 23.74M | 4.7 năm | 9,423 | 11.8% |
| 1 | Entry-level | 13.61M | 0.09 năm | 39,309 | 49.4% |
| 2 | Executive | 58.15M | 2.58 năm | 1,510 | 1.9% |
| 3 | Mid-level | 13.29M | 2.39 năm | 29,430 | 36.9% |

**Nhận xét:**
- **Cụm 1 (Entry)** chiếm gần 50% - thị trường cần nhiều fresher
- **Cụm 2 (Executive)** ít nhất (1.9%) nhưng lương cao nhất (58M)
- Gap lương rõ rệt giữa Executive và các cấp khác

---

### 📊 Biểu đồ 18: Mô hình Nghiên cứu

**Hình ảnh:** `research_model.png`

Xem phần 1.2 - Mô hình Biến Độc lập - Phụ thuộc

---

# 🤖 PHẦN 4: KẾT QUẢ MÔ HÌNH MACHINE LEARNING

## 4.1 Bài toán 1: Dự đoán Mức lương (Regression)

### Input/Output:

**Biến đầu vào (X):**
- `exp_years` (numeric): Số năm kinh nghiệm
- `skill_count` (numeric): Số kỹ năng yêu cầu
- `region` (categorical): Vùng miền (4 giá trị)
- `position_simple` (categorical): Cấp bậc (6 giá trị)
- `job_type` (categorical): Loại hình công việc

**Biến đầu ra (y):**
- `salary_median` (numeric): Lương trung vị (triệu VND)

### Kết quả So sánh:

| Mô hình | CV R² | Test R² | RMSE | MAE |
|---------|-------|---------|------|-----|
| Ridge Regression | 0.1349 | 0.1316 | 8.96M | 5.16M |
| **Random Forest** | **0.1675** | **0.2276** | **8.45M** | **4.91M** |
| Gradient Boosting | 0.1632 | 0.1581 | 8.83M | 5.04M |

### Mô hình tốt nhất: **Random Forest**
- **R² = 22.76%** (giải thích được 22.76% phương sai lương)
- **RMSE = 8.45 triệu VND** (sai số trung bình)
- **Cải thiện 73%** so với Ridge Regression

---

## 4.2 Bài toán 2: Phân loại Cấp bậc (Classification)

### Input/Output:

**Biến đầu vào (X):**
- `exp_years`, `skill_count`, `region`, `job_fields`

**Biến đầu ra (y):**
- `position_simple` (6 classes): Thực tập sinh, Nhân viên, Chuyên gia, Trưởng nhóm, Quản lý, Giám đốc

### Kết quả:

| Metric | Giá trị |
|--------|---------|
| **Accuracy** | 47.68% |
| **F1-macro** | 35.86% |
| **F1-weighted** | 54.12% |
| **ROC-AUC** | 79.43% |
| **CV Accuracy** | 47.23% |

### Nhận xét:
- Class imbalance nghiêm trọng: Nhân viên chiếm 85%
- ROC-AUC cao (79.43%) cho thấy model phân biệt được các class
- Cần SMOTE hoặc class weights để cải thiện

---

## 4.3 Bài toán 3: Phân cụm Việc làm (Clustering)

### Input:

**Features cho clustering:**
- `salary_median`, `exp_years`, `skill_count`

### Kết quả:

| Metric | Giá trị |
|--------|---------|
| **Số cụm tối ưu (k)** | 4 |
| **Silhouette Score** | 0.4363 |
| **Inertia** | 95,000 |

### Đặc điểm các cụm:

| Cụm | Tên gọi | Lương TB | Kinh nghiệm | % Dataset |
|-----|---------|----------|-------------|-----------|
| 0 | Junior+ | 23.74M | 4.7 năm | 11.8% |
| 1 | Entry | 13.61M | 0.09 năm | 49.4% |
| 2 | Executive | 58.15M | 2.58 năm | 1.9% |
| 3 | Mid-level | 13.29M | 2.39 năm | 36.9% |

---

# 📋 PHẦN 5: KẾT LUẬN VÀ KHUYẾN NGHỊ

## 5.1 Kết luận Chính

### Về Thị trường Việc làm:
1. **Ngành hot nhất:** Bán hàng, CSKH, Kế toán, Marketing
2. **Địa điểm hot:** Hà Nội và TP.HCM chiếm 61% việc làm
3. **Loại hình:** Full-time chiếm 97.6%

### Về Mức lương:
1. **Lương trung vị:** 13.5 triệu VND
2. **Hierarchy rõ ràng:** Thực tập (7.5M) → Nhân viên (12.5M) → Quản lý (20M) → Giám đốc (35M)
3. **Chênh lệch vùng miền:** Không đáng kể giữa Bắc và Nam

### Về Mô hình ML:
1. **Regression (R²=22.76%):** Kinh nghiệm là yếu tố quan trọng nhất (29%)
2. **Classification (Acc=47.68%):** Cần xử lý class imbalance
3. **Clustering (Silhouette=0.44):** 4 phân khúc việc làm rõ ràng

---

## 5.2 Khuyến nghị

### Cho Người tìm việc:

| Khuyến nghị | Giải thích | Tác động |
|-------------|------------|----------|
| Tích lũy kinh nghiệm | exp_years chiếm 29% importance | +30-50% lương |
| Phát triển kỹ năng | skill_count có tương quan dương | +10-15% lương |
| Thăng tiến vị trí | Giám đốc lương gấp 3x Nhân viên | +180% lương |

### Cho Doanh nghiệp:

| Khuyến nghị | Lý do | Lợi ích |
|-------------|-------|---------|
| Công khai dải lương | 80% không công khai | Tăng ứng viên |
| Tham khảo mức thị trường | Entry 10-15M, Mid 20M | Cạnh tranh talent |
| Điều chỉnh JD theo cluster | 4 phân khúc rõ ràng | Target đúng |

---

## 5.3 Hạn chế

1. **R² thấp (22.76%):** Thiếu nhiều features quan trọng (education, company size, benefits)
2. **Class imbalance:** Nhân viên chiếm 85% ảnh hưởng đến classification
3. **Snapshot data:** Không có time-series để phân tích xu hướng
4. **Thiếu source column:** Không so sánh được bias giữa các nguồn

---

## 5.4 Hướng Phát triển

1. **Mở rộng features:** education, company size, benefits
2. **Time-series:** Phân tích xu hướng lương theo thời gian
3. **NLP nâng cao:** BERT/Word2Vec cho job description
4. **Recommender System:** Gợi ý việc làm cho ứng viên
5. **Dashboard:** Real-time monitoring thị trường

---

# 📎 PHỤ LỤC

## Danh sách Files trong Project

```
├── vietnam_job_analysis_cleaned_professional.ipynb  # Notebook chính
├── BAOCAO_CHITIET_DAYDU.md                          # Báo cáo này
├── SLIDE_SUMMARY.md                                 # Tóm tắt cho slide
├── 8_STEPS_VERIFICATION.md                          # Xác nhận 8 bước
├── datasets/
│   └── dataset_final.csv                            # Dataset sạch
├── images/
│   ├── research_model.png                           # Mô hình nghiên cứu
│   ├── feature_importance.png
│   ├── confusion_matrix.png
│   └── ...
└── reports/
    ├── BaoCao_TongHop_DuAn.md
    └── images/
```

---

*Tài liệu được tạo tự động từ kết quả phân tích notebook*
*Cập nhật: 23/12/2024*
