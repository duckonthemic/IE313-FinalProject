# 🧹 Quy Trình Làm Sạch Dữ Liệu Chi Tiết

## Tổng Quan

Quy trình làm sạch dữ liệu được thiết kế thành **8 bước tuần tự**, chuyển đổi dữ liệu thô thành dữ liệu sạch phục vụ cho phân tích và xây dựng mô hình.

### Kết Quả Tổng Quan

| Chỉ số | Giá trị |
|--------|---------|
| Dữ liệu thô (input) | 85,470 bản ghi |
| Dữ liệu sạch (output) | 81,971 bản ghi |
| Số bản ghi bị loại | 3,499 (4.1%) |
| Tỷ lệ giữ lại | 95.9% |
| Số cột dữ liệu | 11 cột gốc + 8 cột mới |

---

## 📋 BƯỚC 0: CHUẨN BỊ DỮ LIỆU

### 0.1 Normalize Text Columns

**Mục tiêu:** Chuẩn hóa các cột văn bản về dạng lowercase và loại bỏ khoảng trắng thừa.

**Các cột được xử lý:**
- `job_title`, `job_type`, `position_level`, `city`
- `experience`, `skills`, `job_fields`, `unit`

**Code thực hiện:**
```python
text_cols = ['job_title', 'job_type', 'position_level', 'city', 
             'experience', 'skills', 'job_fields', 'unit']
for col in text_cols:
    df[col] = df[col].astype(str).str.lower().str.strip()
```

### 0.2 Handle 'nan' Strings

**Mục tiêu:** Chuyển chuỗi 'nan' (do đọc từ CSV) thành giá trị NaN thực sự.

```python
for col in ['skills', 'job_fields', 'unit', 'city', 'experience', 'position_level', 'job_type']:
    df[col] = df[col].replace('nan', np.nan)
```

---

## 📍 BƯỚC 1: CHUẨN HÓA TÊN THÀNH PHỐ

### Vấn đề

Dữ liệu thô chứa **466 biến thể khác nhau** của tên thành phố do:
- Viết không dấu / có dấu
- Viết tắt khác nhau (HCM, TPHCM, TP.HCM)
- Tiếng Anh / tiếng Việt
- Sai chính tả

### Giải pháp

Xây dựng **từ điển ánh xạ (mapping dictionary)** để chuẩn hóa.

**Ví dụ mapping:**
```python
city_mapping = {
    # Major cities - various Vietnamese forms
    'hồ chí minh': 'Ho Chi Minh City',
    'ho chi minh': 'Ho Chi Minh City',
    'hcm': 'Ho Chi Minh City',
    'tp.hcm': 'Ho Chi Minh City',
    'tp hcm': 'Ho Chi Minh City',
    'tphcm': 'Ho Chi Minh City',
    'sài gòn': 'Ho Chi Minh City',
    'saigon': 'Ho Chi Minh City',
    
    'hà nội': 'Hanoi',
    'ha noi': 'Hanoi',
    'hn': 'Hanoi',
    
    'đà nẵng': 'Da Nang',
    'da nang': 'Da Nang',
    
    # ... 63 tỉnh/thành phố khác
    
    'toàn quốc': 'Nationwide',
    'toan quoc': 'Nationwide',
    'all': 'Nationwide',
}
```

**Hàm chuẩn hóa:**
```python
def standardize_city(city_val):
    if pd.isna(city_val):
        return np.nan
    city_lower = str(city_val).lower().strip()
    
    # Direct mapping
    if city_lower in city_mapping:
        return city_mapping[city_lower]
    
    # Partial match for compound names
    for key, value in city_mapping.items():
        if key in city_lower:
            return value
    
    # Title case fallback for unmapped cities
    return city_val.title()

df['city'] = df['city'].apply(standardize_city)
```

### Kết quả
- **Trước:** 466 unique values
- **Sau:** 415 unique values
- Giảm ~11% số lượng giá trị unique

---

## 💱 BƯỚC 2: CHUẨN HÓA ĐƠN VỊ TIỀN TỆ

### Vấn đề

Một số tin tuyển dụng (đặc biệt công ty nước ngoài) ghi lương bằng **USD** thay vì VND.

### Giải pháp

Áp dụng tỷ giá quy đổi cố định: **1 USD = 25,000 VND**

```python
USD_TO_VND_RATE = 25000

usd_mask = df['unit'].astype(str).str.lower().str.contains('usd', na=False)
usd_converted = int(usd_mask.sum())

if usd_converted > 0:
    # Convert to million VND
    df.loc[usd_mask, 'salary_min'] = df.loc[usd_mask, 'salary_min'] * USD_TO_VND_RATE / 1_000_000
    df.loc[usd_mask, 'salary_max'] = df.loc[usd_mask, 'salary_max'] * USD_TO_VND_RATE / 1_000_000
    df.loc[usd_mask, 'unit'] = 'vnd'
```

### Kết quả
- **713 bản ghi** được chuyển đổi từ USD sang VND
- Đảm bảo tính nhất quán về đơn vị trong toàn bộ dataset

---

## ✅ BƯỚC 3: KIỂM TRA TÍNH HỢP LỆ CỦA MỨC LƯƠNG

### Vấn đề

Một số bản ghi có lương tối thiểu **lớn hơn** lương tối đa - đây là lỗi nhập liệu từ phía nhà tuyển dụng.

### Giải pháp

Loại bỏ các bản ghi không hợp lệ:
```python
salary_invalid = df['salary_min'] > df['salary_max']
n_invalid = int(salary_invalid.sum())  # = 3,495
df = df[~salary_invalid].copy()
```

### Xử lý giá trị lương = 0

Lương bằng 0 thường là giá trị mặc định khi không có thông tin → chuyển thành NaN:
```python
salary_zero = (df['salary_min'] == 0) | (df['salary_max'] == 0)
n_zero = int(salary_zero.sum())  # = 2,202

df.loc[df['salary_min'] == 0, 'salary_min'] = np.nan
df.loc[df['salary_max'] == 0, 'salary_max'] = np.nan
```

### Kết quả
- **3,495 bản ghi** bị loại do salary_min > salary_max
- **2,202 bản ghi** có giá trị 0 được chuyển thành NaN

---

## 🏷️ BƯỚC 4: XỬ LÝ MISSING SALARIES

### Vấn đề

Khoảng 80% tin tuyển dụng không công khai thông tin lương (ghi "thỏa thuận" hoặc "cạnh tranh").

### Giải pháp

**Phương án A: Gắn cờ (Flag)**
```python
both_missing = df['salary_min'].isna() & df['salary_max'].isna()
df['has_salary'] = ~both_missing
```

**Phương án B: Imputation (dùng cho phân tích)**
Sử dụng **median theo ngành nghề** để điền giá trị thiếu:
```python
# Industry-based imputation
industry_salary_avg = df.groupby('job_fields')['salary_min'].transform('median')
df['salary_min_imputed'] = df['salary_min'].fillna(industry_salary_avg)

industry_salary_max_avg = df.groupby('job_fields')['salary_max'].transform('median')
df['salary_max_imputed'] = df['salary_max'].fillna(industry_salary_max_avg)
```

### Kết quả
- Tạo cột `has_salary` để đánh dấu bản ghi có thông tin lương
- Tạo cột `salary_min_imputed` và `salary_max_imputed` cho phân tích

---

## 🔍 BƯỚC 5: PHÁT HIỆN VÀ GẮN CỜ BẢN GHI TRÙNG LẶP

### Vấn đề

Do thu thập từ nhiều nguồn và nhiều thời điểm, có thể có các tin tuyển dụng trùng lặp.

### Giải pháp

**Lưu ý:** Do dữ liệu **không có cột `company_name`**, không thể xác định chính xác trùng lặp → chỉ **gắn cờ** thay vì loại bỏ.

```python
# Check if company_name exists
if 'company_name' in df.columns:
    dup_subset = ['job_title', 'company_name', 'city']
    dup_mask = df.duplicated(subset=dup_subset, keep='first')
    df = df[~dup_mask].copy()  # Remove duplicates
else:
    # Flag potential duplicates only
    dup_subset = ['job_title', 'city']
    dup_mask = df.duplicated(subset=dup_subset, keep=False)
    df['is_potential_duplicate'] = dup_mask
```

### Kết quả
- **67,374 bản ghi** được gắn cờ là potential duplicates
- Không loại bỏ vì thiếu thông tin company_name để xác nhận

---

## 🚫 BƯỚC 6: LOẠI BỎ OUTLIERS LƯƠNG

### Vấn đề

Một số bản ghi có mức lương **cực kỳ cao** (>500 triệu VND/tháng), đây là lỗi nhập liệu hoặc giá trị ngoại lai.

### Giải pháp

Áp dụng **ngưỡng dựa trên domain knowledge**:
```python
# Lương > 500 triệu VND/tháng được coi là outlier
salary_extreme = df['salary_max'] > 500
n_outlier = int(salary_extreme.sum())  # = 4
df = df[~salary_extreme].copy()
```

### Kết quả
- **4 bản ghi** bị loại do lương > 500 triệu VND

---

## 📂 BƯỚC 7: TÁCH VÀ XỬ LÝ JOB FIELDS

### Vấn đề

Cột `job_fields` chứa nhiều ngành nghề phân cách bằng dấu phẩy.

### Giải pháp

Tách thành danh sách và trích xuất thông tin:
```python
def split_job_fields(fields_str):
    if pd.isna(fields_str):
        return []
    return [f.strip().lower() for f in str(fields_str).split(',') if f.strip()]

df['job_fields_list'] = df['job_fields'].apply(split_job_fields)
df['job_fields_count'] = df['job_fields_list'].apply(len)
df['job_field_primary'] = df['job_fields_list'].apply(lambda x: x[0] if x else np.nan)
```

### Kết quả
- `job_fields_list`: Danh sách các ngành nghề (array)
- `job_fields_count`: Số lượng ngành nghề liên quan
- `job_field_primary`: Ngành nghề chính (đầu tiên trong danh sách)

---

## 🧮 BƯỚC 8: TẠO CÁC ĐẶC TRƯNG MỚI (DERIVED FEATURES)

### 8.1 Lương Trung Vị

```python
df['salary_median'] = (df['salary_min'] + df['salary_max']) / 2
df['salary_median_imputed'] = (df['salary_min_imputed'] + df['salary_max_imputed']) / 2
```

### 8.2 Phân Vùng Miền

```python
def classify_region(city):
    if pd.isna(city):
        return 'Toàn quốc'
    city_lower = str(city).lower()
    
    # Miền Bắc
    north = ['hanoi', 'hai phong', 'bac ninh', 'hai duong', 'hung yen', ...]
    # Miền Trung
    central = ['da nang', 'hue', 'nha trang', 'quang nam', 'binh dinh', ...]
    # Miền Nam
    south = ['ho chi minh', 'binh duong', 'dong nai', 'can tho', 'long an', ...]
    
    for city_name in north:
        if city_name in city_lower:
            return 'Miền Bắc'
    for city_name in central:
        if city_name in city_lower:
            return 'Miền Trung'
    for city_name in south:
        if city_name in city_lower:
            return 'Miền Nam'
    return 'Toàn quốc'

df['region'] = df['city'].apply(classify_region)
```

### 8.3 Số Năm Kinh Nghiệm

```python
def parse_experience(exp_str):
    if pd.isna(exp_str):
        return 0
    exp_lower = str(exp_str).lower()
    
    # Extract numbers using regex
    numbers = re.findall(r'(\d+)', exp_lower)
    if numbers:
        return int(numbers[0])
    
    # Handle text patterns
    if 'không yêu cầu' in exp_lower or 'chưa có' in exp_lower:
        return 0
    return 0

df['exp_years'] = df['experience'].apply(parse_experience)
```

### 8.4 Cấp Bậc Vị Trí (Đơn Giản Hóa)

```python
def simplify_position(pos_level):
    if pd.isna(pos_level):
        return 'Nhân viên'
    pos_lower = str(pos_level).lower()
    
    if any(x in pos_lower for x in ['giám đốc', 'director', 'ceo', 'cto', 'cfo']):
        return 'Giám đốc'
    elif any(x in pos_lower for x in ['quản lý', 'manager', 'trưởng phòng']):
        return 'Quản lý'
    elif any(x in pos_lower for x in ['trưởng nhóm', 'team lead', 'supervisor']):
        return 'Trưởng nhóm'
    elif any(x in pos_lower for x in ['chuyên gia', 'expert', 'senior']):
        return 'Chuyên gia'
    elif any(x in pos_lower for x in ['thực tập', 'intern']):
        return 'Thực tập sinh'
    else:
        return 'Nhân viên'

df['position_simple'] = df['position_level'].apply(simplify_position)
```

### 8.5 Đếm Số Kỹ Năng

```python
def count_skills(skills_str):
    if pd.isna(skills_str):
        return 0
    return len([s.strip() for s in str(skills_str).split(',') if s.strip()])

df['skill_count'] = df['skills'].apply(count_skills)
```

### 8.6 Các Feature Khác

```python
# Có yêu cầu tiếng Anh
df['requires_english'] = df['skills'].str.lower().str.contains('english|tiếng anh', na=False).astype(int)

# Có kỹ năng IT
it_keywords = ['python', 'java', 'sql', 'excel', 'javascript', 'c#', 'c++', 'react', 'nodejs']
df['has_tech_skills'] = df['skills'].str.lower().str.contains('|'.join(it_keywords), na=False).astype(int)
```

---

## 📊 TỔNG KẾT QUY TRÌNH

### Bảng Tóm Tắt Các Bước

| Bước | Mô tả | Số bản ghi ảnh hưởng |
|------|-------|---------------------|
| 0 | Normalize text, handle 'nan' strings | Tất cả |
| 1 | Chuẩn hóa tên thành phố | 466 → 415 unique |
| 2 | Chuyển đổi USD → VND | 713 bản ghi |
| 3a | Loại bỏ salary_min > salary_max | -3,495 bản ghi |
| 3b | Chuyển salary = 0 thành NaN | 2,202 bản ghi |
| 4 | Gắn cờ missing salaries, imputation | ~80% dữ liệu |
| 5 | Gắn cờ potential duplicates | 67,374 bản ghi |
| 6 | Loại bỏ outliers lương | -4 bản ghi |
| 7 | Tách job_fields thành array | Tất cả |
| 8 | Tạo derived features | Tất cả |

### Cột Mới Được Tạo

| Tên cột | Kiểu | Mô tả |
|---------|------|-------|
| `city` | string | Tên thành phố đã chuẩn hóa (tiếng Anh) |
| `has_salary` | boolean | True nếu có thông tin lương |
| `salary_min_imputed` | float | Lương min đã impute bằng median ngành |
| `salary_max_imputed` | float | Lương max đã impute bằng median ngành |
| `salary_median` | float | (min + max) / 2 |
| `salary_median_imputed` | float | (min_imputed + max_imputed) / 2 |
| `job_fields_list` | array | Danh sách ngành nghề |
| `job_fields_count` | int | Số lượng ngành nghề |
| `job_field_primary` | string | Ngành nghề chính |
| `region` | string | Vùng miền (Bắc/Trung/Nam/Toàn quốc) |
| `exp_years` | int | Số năm kinh nghiệm yêu cầu |
| `position_simple` | string | Cấp bậc đã đơn giản hóa |
| `skill_count` | int | Số lượng kỹ năng yêu cầu |
| `requires_english` | int | 1 nếu yêu cầu tiếng Anh |
| `has_tech_skills` | int | 1 nếu yêu cầu kỹ năng IT |
| `is_potential_duplicate` | boolean | True nếu có thể trùng lặp |

### Báo Cáo Làm Sạch (Output)

```
======================================================================
 DATA CLEANING REPORT
======================================================================
  • Standardized city names: 466 unique → 415 unique
  • Converted 713 USD salaries to VND (rate=25,000)
  • Removed 3,495 rows: salary_min > salary_max
  • Set 2,202 rows with 0 salary fields to NaN
  • Flagged 4 rows with no salary info (has_salary=False)
  • Created imputed salary columns using industry median
  • Limitation: company_name not available; duplicates are flagged (not removed)
  • Flagged 67,374 rows as potential duplicates using subset=['job_title', 'city']
  • Removed 4 salary outliers (>500M VND)
  • Split job_fields into arrays (job_fields_list) and extracted primary field
======================================================================
 Final rows: 81,971 (from 85,470)
 Removed: 3,499 (4.1%)
 Rows with valid salary: 81,967 (100.0%)
 USD converted: 713
======================================================================
```

---

## 💡 GHI CHÚ VÀ HẠN CHẾ

### Các quyết định thiết kế

1. **Chọn loại bỏ thay vì impute cho salary invalid:** Vì salary_min > salary_max là lỗi logic rõ ràng, không thể khôi phục

2. **Gắn cờ thay vì loại bỏ duplicates:** Do thiếu cột `company_name`, không thể xác định chính xác trùng lặp

3. **Sử dụng median thay vì mean cho imputation:** Median ít bị ảnh hưởng bởi outliers trong dữ liệu lương (skewed distribution)

4. **Chọn ngưỡng 500M VND cho outliers:** Dựa trên domain knowledge - rất ít vị trí có lương > 500 triệu/tháng

### Hạn chế

- Thiếu cột `company_name` → không thể xử lý duplicates hoàn toàn
- Thiếu thông tin chi tiết về `job_description` → khó trích xuất thêm features
- Dữ liệu lương thiếu nhiều (~80%) → ảnh hưởng đến một số phân tích
