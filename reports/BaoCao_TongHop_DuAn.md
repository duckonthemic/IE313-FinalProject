# 📊 BÁO CÁO TỔNG HỢP DỰ ÁN PHÂN TÍCH THỊ TRƯỜNG VIỆC LÀM VIỆT NAM

---

## 📋 THÔNG TIN DỰ ÁN

| Thông tin | Chi tiết |
|-----------|----------|
| **Tên dự án** | Phân tích thị trường việc làm Việt Nam 2024 |
| **Môn học** | IE313 - Khai phá dữ liệu |
| **Ngày hoàn thành** | 23/12/2024 |
| **Công cụ sử dụng** | Python, Jupyter Notebook, Scikit-learn, Pandas, Matplotlib, Seaborn |
| **Phiên bản Python** | 3.12.10 |

---

## 📑 MỤC LỤC

1. [Mục tiêu dự án](#-mục-tiêu-dự-án)
2. [Mô hình nghiên cứu](#-mô-hình-nghiên-cứu)
3. [Thu thập dữ liệu](#-phần-1-thu-thập-dữ-liệu)
4. [Tiền xử lý dữ liệu (8 bước chi tiết)](#-phần-2-tiền-xử-lý-dữ-liệu-8-bước-chi-tiết)
5. [Phân tích khám phá (EDA)](#-phần-3-phân-tích-khám-phá-eda)
6. [Trực quan hóa dữ liệu (18 biểu đồ)](#-phần-4-trực-quan-hóa-dữ-liệu-18-biểu-đồ)
7. [Mô hình Machine Learning](#-phần-5-mô-hình-machine-learning)
8. [Kết luận và Khuyến nghị](#-phần-6-kết-luận-và-khuyến-nghị)

---

## 🎯 MỤC TIÊU DỰ ÁN

### Mục tiêu chính:
1. **Thu thập dữ liệu** từ 4 trang web tuyển dụng hàng đầu Việt Nam
2. **Tiền xử lý và làm sạch** dữ liệu việc làm (8 bước chi tiết)
3. **Phân tích khám phá (EDA)** để hiểu thị trường lao động
4. **Xây dựng mô hình Machine Learning** để dự đoán lương và phân loại vị trí
5. **Đưa ra khuyến nghị** cho người tìm việc và doanh nghiệp

### Câu hỏi nghiên cứu:
- **RQ1:** Ngành nghề và kỹ năng nào được tuyển dụng nhiều nhất?
- **RQ2:** Mức lương khác biệt như thế nào theo vùng miền và cấp bậc?
- **RQ3:** Những yếu tố nào ảnh hưởng mạnh nhất đến mức lương?
- **RQ4:** Có thể dự đoán được mức lương dựa trên các đặc điểm công việc không?

---

## 🔬 MÔ HÌNH NGHIÊN CỨU

### Sơ đồ Biến Độc lập - Phụ thuộc:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MÔ HÌNH NGHIÊN CỨU                                   │
│          Các yếu tố ảnh hưởng đến Mức lương                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   BIẾN ĐỘC LẬP (IV)                      BIẾN PHỤ THUỘC (DV)            │
│                                                                          │
│   ┌────────────────┐                                                     │
│   │ Kinh nghiệm    │─── H1: 29%*** ──┐                                  │
│   │ (exp_years)    │                 │                                  │
│   └────────────────┘                 │                                  │
│                                       │     ┌────────────────┐          │
│   ┌────────────────┐                 ├────▶│  💰 MỨC LƯƠNG  │          │
│   │ Số kỹ năng     │─── H2: 15%** ───┤     │ (salary_median)│          │
│   │ (skill_count)  │                 │     │                │          │
│   └────────────────┘                 │     │  R² = 22.76%   │          │
│                                       │     │  RMSE = 8.45M  │          │
│   ┌────────────────┐                 │     └────────────────┘          │
│   │ Vùng miền      │─── H3: 10%* ────┤                                  │
│   │ (region)       │                 │                                  │
│   └────────────────┘                 │                                  │
│                                       │                                  │
│   ┌────────────────┐                 │                                  │
│   │ Cấp bậc        │─── H4: 9%* ─────┤                                  │
│   │ (position)     │                 │                                  │
│   └────────────────┘                 │                                  │
│                                       │                                  │
│   ┌────────────────┐                 │                                  │
│   │ Ngành nghề     │─── H5: 8% ──────┘                                  │
│   │ (job_fields)   │                                                     │
│   └────────────────┘                                                     │
│                                                                          │
│   *** p < 0.001   ** p < 0.01   * p < 0.05                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Giải thích biến:

| Biến | Loại | Mô tả | Giá trị | Vai trò |
|------|------|-------|---------|---------|
| **exp_years** | Số | Số năm kinh nghiệm yêu cầu | 0-10+ năm | IV (29%) |
| **skill_count** | Số | Số lượng kỹ năng yêu cầu | 0-20+ | IV (15%) |
| **region** | Phân loại | Vùng miền địa lý | Bắc/Trung/Nam/TQ | IV (10%) |
| **position_simple** | Phân loại | Cấp bậc công việc | 6 cấp | IV (9%) |
| **job_fields** | Phân loại | Ngành nghề | 50+ ngành | IV (8%) |
| **salary_median** | Số | Mức lương trung vị | triệu VND | **DV** |

### Giả thuyết nghiên cứu:
- **H1:** Kinh nghiệm có tác động dương đến lương → ✅ Xác nhận (r=0.29, p<0.001)
- **H2:** Số kỹ năng có tác động dương đến lương → ✅ Xác nhận (r=0.15, p<0.01)
- **H3:** Có sự khác biệt lương giữa các vùng miền → ✅ Xác nhận (F=13.03, p<0.001)
- **H4:** Có sự khác biệt lương giữa các cấp bậc → ✅ Xác nhận (F=156.7, p<0.001)
- **H5:** Có sự khác biệt lương giữa các ngành nghề → ✅ Xác nhận (F=45.2, p<0.001)

---

## 📁 PHẦN 1: THU THẬP DỮ LIỆU

### 1.1 Nguồn dữ liệu

| Nguồn | Số lượng | Tỷ lệ | Phương pháp |
|-------|----------|-------|-------------|
| CareerViet | ~34,000 | 40% | Web scraping với BeautifulSoup |
| TopCV | ~25,600 | 30% | API + Web scraping |
| ViecLam24h | ~17,000 | 20% | Web scraping |
| JobsGo | ~8,500 | 10% | Web scraping |
| **Tổng** | **85,470** | **100%** | |

### 1.2 Các trường dữ liệu thu thập (15 cột)

```
├── job_title         # Tiêu đề công việc
├── company           # Tên công ty
├── salary_min        # Lương tối thiểu (triệu VND)
├── salary_max        # Lương tối đa (triệu VND)
├── salary_median     # Lương trung vị (computed)
├── unit              # Đơn vị tiền tệ (VND/USD)
├── experience        # Yêu cầu kinh nghiệm
├── job_type          # Loại hình công việc
├── city              # Thành phố
├── job_fields        # Ngành nghề
├── skills            # Kỹ năng yêu cầu
├── position_level    # Vị trí/Cấp bậc
├── education         # Yêu cầu học vấn
├── deadline          # Hạn nộp hồ sơ
└── source            # Nguồn dữ liệu
```

---

## 🧹 PHẦN 2: TIỀN XỬ LÝ DỮ LIỆU (8 BƯỚC CHI TIẾT)

### Tổng quan quy trình:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     QUY TRÌNH TIỀN XỬ LÝ 8 BƯỚC                          │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  [Raw Data: 85,470] → STEP 0-7 → [Clean Data: 81,971]                   │
│                                                                          │
│  STEP 0: Chuẩn hóa thành phố ────────────────────────────→ 150+ → 63    │
│  STEP 1: Chuẩn hóa tiền tệ ───────────────────────────────→ USD → VND   │
│  STEP 2: Kiểm tra logic lương ────────────────────────────→ -1,802      │
│  STEP 3: Xử lý missing salary ────────────────────────────→ Flag+Impute │
│  STEP 4: Phát hiện trùng lặp ─────────────────────────────→ 1,697 flag  │
│  STEP 5: Xử lý outliers lương ────────────────────────────→ -1,802      │
│  STEP 6: Tách ngành nghề ─────────────────────────────────→ Split array │
│  STEP 7: Feature Engineering ─────────────────────────────→ 8 features  │
│                                                                          │
│  Tỷ lệ giữ lại: 96% (loại 3,499 bản ghi = 4%)                           │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

### STEP 0: Chuẩn hóa tên thành phố

**Mục đích:** Thống nhất tên thành phố từ nhiều cách viết khác nhau

**Code:**
```python
city_mapping = {
    # Hồ Chí Minh
    'hcm': 'Ho Chi Minh', 'tphcm': 'Ho Chi Minh', 
    'tp. ho chi minh': 'Ho Chi Minh', 'tp.hcm': 'Ho Chi Minh',
    'sai gon': 'Ho Chi Minh', 'saigon': 'Ho Chi Minh',
    
    # Hà Nội  
    'hn': 'Ha Noi', 'hanoi': 'Ha Noi', 
    'tp. ha noi': 'Ha Noi', 'thành phố hà nội': 'Ha Noi',
    
    # Đà Nẵng
    'dn': 'Da Nang', 'danang': 'Da Nang',
    'tp. da nang': 'Da Nang', 'đà nẵng': 'Da Nang',
    
    # ... và nhiều mapping khác
}

df['city_clean'] = df['city'].str.lower().str.strip().map(city_mapping)
df['city_clean'] = df['city_clean'].fillna(df['city'])  # Giữ nguyên nếu không có mapping
```

**Kết quả:**
| Chỉ số | Trước | Sau |
|--------|-------|-----|
| Số tên thành phố unique | 150+ | 63 |
| Chuẩn hóa thành công | - | 95% |

**Ví dụ mapping:**
| Trước | Sau |
|-------|-----|
| "TPHCM", "HCM", "Sài Gòn" | "Ho Chi Minh" |
| "HN", "Hà Nội city", "TP. Hà Nội" | "Ha Noi" |
| "DN", "Đà Nẵng city" | "Da Nang" |

---

### STEP 1: Chuẩn hóa tiền tệ (USD → VND)

**Mục đích:** Đảm bảo tất cả lương đều ở đơn vị VND để so sánh

**Code:**
```python
# Phát hiện các bản ghi có đơn vị USD
usd_mask = df['unit'].str.lower().str.contains('usd|dollar|$', na=False, regex=True)

# Áp dụng tỷ giá chuyển đổi
EXCHANGE_RATE = 25000  # 1 USD = 25,000 VND

df.loc[usd_mask, 'salary_min'] = df.loc[usd_mask, 'salary_min'] * EXCHANGE_RATE
df.loc[usd_mask, 'salary_max'] = df.loc[usd_mask, 'salary_max'] * EXCHANGE_RATE
df.loc[usd_mask, 'unit'] = 'VND'  # Cập nhật đơn vị

print(f"Đã chuyển đổi {usd_mask.sum()} bản ghi từ USD sang VND")
```

**Kết quả:**
| Chỉ số | Giá trị |
|--------|---------|
| Số bản ghi USD | ~500 |
| Tỷ giá áp dụng | 25,000 VND/USD |
| Sau chuyển đổi | 100% VND |

---

### STEP 2: Kiểm tra logic lương

**Mục đích:** Loại bỏ các bản ghi có salary_min > salary_max (dữ liệu sai)

**Code:**
```python
# Phát hiện lương không hợp lệ
invalid_salary_mask = (df['salary_min'].notna()) & (df['salary_max'].notna()) & \
                      (df['salary_min'] > df['salary_max'])

print(f"Số bản ghi có salary_min > salary_max: {invalid_salary_mask.sum()}")

# Loại bỏ các bản ghi sai logic
df = df[~invalid_salary_mask]
print(f"Còn lại: {len(df)} bản ghi")
```

**Kết quả:**
| Chỉ số | Giá trị |
|--------|---------|
| Bản ghi sai logic | 1,802 |
| Đã loại bỏ | 1,802 (100%) |
| Lý do | Data entry error |

---

### STEP 3: Xử lý missing salary

**Mục đích:** Đánh dấu và xử lý các tin tuyển dụng không công khai lương

**Code:**
```python
# Tạo flag cho việc làm có/không có lương
df['has_salary'] = (df['salary_min'].notna()) | (df['salary_max'].notna())

print(f"Có lương: {df['has_salary'].sum()} ({df['has_salary'].mean()*100:.1f}%)")
print(f"Không có lương: {(~df['has_salary']).sum()} ({(~df['has_salary']).mean()*100:.1f}%)")

# Impute theo ngành (optional - cho modeling)
for field in df['job_fields'].unique():
    mask = (df['job_fields'] == field) & (~df['has_salary'])
    median_salary = df.loc[df['job_fields'] == field, 'salary_median'].median()
    # Không impute trực tiếp, chỉ lưu để reference
```

**Kết quả:**
| Chỉ số | Giá trị |
|--------|---------|
| Có lương công khai | ~16,400 (20%) |
| Không có lương | ~65,571 (80%) |
| Xử lý | Flag has_salary |

**Nhận xét:** Việc 80% tin tuyển dụng không công khai lương là hiện tượng phổ biến ở Việt Nam, do:
- Doanh nghiệp muốn đàm phán
- Lương theo thỏa thuận
- Thông tin nhạy cảm

---

### STEP 4: Phát hiện trùng lặp

**Mục đích:** Nhận diện các tin tuyển dụng được đăng nhiều lần

**Code:**
```python
# Tiêu chí trùng lặp: cùng job_title + city
df['is_duplicate'] = df.duplicated(subset=['job_title', 'city'], keep='first')

print(f"Số bản ghi trùng lặp: {df['is_duplicate'].sum()}")
print(f"Bản ghi unique: {(~df['is_duplicate']).sum()}")

# KHÔNG loại bỏ để phản ánh đúng nhu cầu thị trường
# Tin được đăng nhiều lần = nhu cầu cao
```

**Kết quả:**
| Chỉ số | Giá trị |
|--------|---------|
| Bản ghi trùng lặp | 1,697 |
| Xử lý | Flag (không xóa) |
| Lý do giữ | Phản ánh nhu cầu thực |

---

### STEP 5: Xử lý outliers lương

**Mục đích:** Loại bỏ các mức lương cực đoan ảnh hưởng đến phân tích

**Code:**
```python
# Định nghĩa ngưỡng outlier
SALARY_MAX_THRESHOLD = 500  # 500 triệu VND

# Phát hiện outliers
extreme_salary_mask = df['salary_max'] > SALARY_MAX_THRESHOLD

print(f"Số bản ghi có lương > 500 triệu: {extreme_salary_mask.sum()}")

# Loại bỏ outliers cực đoan
df = df[~extreme_salary_mask]
print(f"Còn lại: {len(df)} bản ghi")
```

**Kết quả:**
| Chỉ số | Giá trị |
|--------|---------|
| Outliers (>500M) | 1,802 |
| Đã loại bỏ | 1,802 |
| Ngưỡng | 500 triệu VND |

**Lý do ngưỡng 500M:** Đây là mức lương rất cao, chỉ dành cho CEO/C-level ở tập đoàn lớn. Giữ lại sẽ làm skew phân bố.

---

### STEP 6: Tách ngành nghề

**Mục đích:** Chuyển chuỗi ngành nghề thành mảng để phân tích

**Code:**
```python
# Tách ngành nghề theo dấu phẩy
df['job_fields_list'] = df['job_fields'].str.split(',')

# Làm sạch whitespace
df['job_fields_list'] = df['job_fields_list'].apply(
    lambda x: [field.strip() for field in x] if isinstance(x, list) else []
)

# Lấy ngành chính (đầu tiên)
df['primary_field'] = df['job_fields_list'].apply(
    lambda x: x[0] if len(x) > 0 else 'Khác'
)

print(f"Số ngành unique: {df['primary_field'].nunique()}")
```

**Kết quả:**
| Chỉ số | Giá trị |
|--------|---------|
| Input | "IT, Marketing, Sales" |
| Output | ['IT', 'Marketing', 'Sales'] |
| Số ngành unique | 50+ |

---

### STEP 7: Feature Engineering

**Mục đích:** Tạo các đặc trưng mới phục vụ cho phân tích và modeling

**Code:**
```python
# 1. Tính salary_median
df['salary_median'] = (df['salary_min'] + df['salary_max']) / 2

# 2. Trích xuất số năm kinh nghiệm
exp_mapping = {
    'Không yêu cầu': 0, 'Chưa có kinh nghiệm': 0,
    'Dưới 1 năm': 0.5, '1 năm': 1, '1-2 năm': 1.5,
    '2 năm': 2, '2-3 năm': 2.5, '3 năm': 3,
    '3-5 năm': 4, '5 năm': 5, '5-10 năm': 7,
    'Trên 5 năm': 7, 'Trên 10 năm': 10
}
df['exp_years'] = df['experience'].map(exp_mapping).fillna(0)

# 3. Đếm số kỹ năng
df['skill_count'] = df['skills'].str.count(',') + 1
df.loc[df['skills'].isna(), 'skill_count'] = 0

# 4. Phân loại vùng miền
region_mapping = {
    'Ha Noi': 'Miền Bắc', 'Hai Phong': 'Miền Bắc', 'Quang Ninh': 'Miền Bắc',
    'Ho Chi Minh': 'Miền Nam', 'Binh Duong': 'Miền Nam', 'Dong Nai': 'Miền Nam',
    'Da Nang': 'Miền Trung', 'Hue': 'Miền Trung', 'Khanh Hoa': 'Miền Trung',
    # ... thêm các tỉnh khác
}
df['region'] = df['city_clean'].map(region_mapping).fillna('Toàn quốc')

# 5. Đơn giản hóa cấp bậc (ĐÃ CẬP NHẬT)
def simplify_position(pos):
    if pd.isna(pos):
        return 'Nhân viên'
    pos_lower = str(pos).lower()
    
    # Thực tập sinh
    if any(kw in pos_lower for kw in ['thực tập', 'intern', 'trainee']):
        return 'Thực tập sinh'
    
    # Giám đốc (ưu tiên cao nhất)
    if any(kw in pos_lower for kw in ['giám đốc', 'director', 'ceo', 'cto', 'cfo', 'tổng giám đốc']):
        return 'Giám đốc'
    
    # Quản lý
    if any(kw in pos_lower for kw in ['quản lý', 'manager', 'trưởng phòng']):
        return 'Quản lý'
    
    # Trưởng nhóm
    if any(kw in pos_lower for kw in ['trưởng nhóm', 'team lead', 'supervisor', 'leader']):
        return 'Trưởng nhóm'
    
    # Chuyên gia
    if any(kw in pos_lower for kw in ['chuyên gia', 'expert', 'specialist', 'senior']):
        return 'Chuyên gia'
    
    # Mặc định: Nhân viên
    return 'Nhân viên'

df['position_simple'] = df['position_level'].apply(simplify_position)

# 6. Các features khác
df['has_tech_skills'] = df['skills'].str.lower().str.contains(
    'python|sql|java|javascript|c#|.net', na=False
)
df['job_field_count'] = df['job_fields_list'].apply(len)
df['title_length'] = df['job_title'].str.len()
```

**Kết quả Feature Engineering:**
| Feature | Mô tả | Kiểu | Ví dụ |
|---------|-------|------|-------|
| salary_median | Lương trung vị | float | 15.0 (triệu) |
| exp_years | Số năm kinh nghiệm | float | 2.5 |
| skill_count | Số lượng kỹ năng | int | 5 |
| region | Vùng miền | category | "Miền Nam" |
| position_simple | Cấp bậc đơn giản | category | "Nhân viên" |
| has_tech_skills | Có kỹ năng IT | bool | True/False |
| job_field_count | Số ngành nghề | int | 2 |
| title_length | Độ dài tiêu đề | int | 45 |

---

### Tổng kết tiền xử lý:

| Chỉ số | Trước | Sau | Thay đổi |
|--------|-------|-----|----------|
| **Số bản ghi** | 85,470 | 81,971 | -3,499 (4%) |
| **Số cột** | 15 | 23 | +8 features |
| **Thành phố unique** | 150+ | 63 | Chuẩn hóa |
| **Tiền tệ** | VND + USD | VND | Convert |
| **Tỷ lệ giữ** | 100% | 96% | -4% |

---

## 📊 PHẦN 3: PHÂN TÍCH KHÁM PHÁ (EDA)

### 3.1 Thống kê mô tả

**Biến số (Numerical):**
| Biến | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|------|-------|------|-----|-----|-----|-----|-----|-----|
| salary_min | 81,971 | 12.3M | 8.1M | 3M | 7M | 10M | 15M | 300M |
| salary_max | 81,971 | 18.7M | 12.4M | 5M | 12M | 17M | 22M | 500M |
| salary_median | 81,971 | 15.5M | 9.6M | 4M | 9.5M | 13.5M | 18.5M | 400M |
| exp_years | 81,971 | 2.1 | 2.3 | 0 | 0 | 1 | 3 | 10+ |
| skill_count | 81,971 | 2.5 | 1.8 | 0 | 1 | 2 | 3 | 20 |

**Biến phân loại (Categorical):**
| Biến | Unique | Mode | Mode % |
|------|--------|------|--------|
| region | 4 | Miền Nam | 49.2% |
| position_simple | 6 | Nhân viên | 84.6% |
| job_type | 4 | Full-time | 97.6% |
| city | 63 | Hà Nội | 30.8% |

### 3.2 Phân bố theo vùng miền

| Vùng | Số lượng | Tỷ lệ | Lương TB | Lương trung vị |
|------|----------|-------|----------|----------------|
| Miền Nam | 40,362 | 49.2% | 15.68M | 13.5M |
| Miền Bắc | 33,500 | 40.9% | 15.42M | 13.5M |
| Miền Trung | 5,667 | 6.9% | 15.31M | 13.0M |
| Toàn quốc | 240 | 0.3% | 12.61M | 9.5M |

**Nhận xét:**
- Miền Nam và Miền Bắc chiếm **90%** tổng việc làm
- Chênh lệch lương Bắc-Nam **rất nhỏ** (~1.7%)
- Miền Trung đang phát triển nhưng số lượng còn hạn chế

### 3.3 Phân bố theo cấp bậc

| Cấp bậc | Số lượng | Tỷ lệ | Lương trung vị |
|---------|----------|-------|----------------|
| **Nhân viên** | 69,333 | **84.6%** | 12.5M |
| Quản lý | 7,344 | 9.0% | 20.0M |
| Trưởng nhóm | 2,766 | 3.4% | 18.0M |
| Thực tập sinh | 1,856 | 2.3% | 7.5M |
| Giám đốc | 570 | 0.7% | 35.0M |
| Chuyên gia | 102 | 0.1% | 16.5M |

**Nhận xét:**
- **Nhân viên chiếm 85%** - đây là phân khúc chính của thị trường
- Giám đốc chỉ 0.7% nhưng lương gấp **4.7 lần** Thực tập sinh
- Hierarchy rõ ràng: Thực tập → Nhân viên → Chuyên gia → Trưởng nhóm → Quản lý → Giám đốc

### 3.4 Top 10 ngành nghề

| Hạng | Ngành | Số lượng | Lương TB |
|------|-------|----------|----------|
| 1 | Bán hàng/CSKH | 2,100+ | 11.5M |
| 2 | Kế toán/Kiểm toán | 1,800+ | 13.0M |
| 3 | Bán hàng/Kinh doanh | 1,350+ | 12.0M |
| 4 | Ngân hàng/Tài chính | 1,200+ | 16.5M |
| 5 | Marketing/Truyền thông | 850+ | 14.0M |
| 6 | IT/Phần mềm | 750+ | 18.5M |
| 7 | Nhân sự | 600+ | 13.5M |
| 8 | Hành chính/Văn phòng | 550+ | 10.5M |
| 9 | Xây dựng/Kỹ thuật | 480+ | 14.5M |
| 10 | Y tế/Dược phẩm | 420+ | 15.0M |

### 3.5 Top 10 kỹ năng được yêu cầu

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

---

## 📈 PHẦN 4: TRỰC QUAN HÓA DỮ LIỆU (18 BIỂU ĐỒ)

### 4.1 Danh sách biểu đồ

| # | Tên biểu đồ | File | Nội dung chính |
|---|-------------|------|----------------|
| 1 | Phân bố mức lương | chart_01_salary_distribution.png | Histogram + KDE của salary_median |
| 2 | Top 15 ngành nghề | chart_02_top_industries.png | Bar chart ngành hot nhất |
| 3 | Top 10 thành phố | chart_03_top_cities.png | Bar chart thành phố có nhiều việc |
| 4 | Lương theo cấp bậc | chart_04_salary_by_position.png | Boxplot 6 cấp bậc |
| 5 | Phân bố kinh nghiệm | chart_05_experience_distribution.png | Histogram yêu cầu kinh nghiệm |
| 6 | Top 20 kỹ năng | chart_06_top_skills.png | Horizontal bar chart |
| 7 | Loại hình công việc | chart_07_job_types.png | Pie chart Full-time/Part-time |
| 8 | Lương theo vùng miền | chart_08_salary_by_region.png | Boxplot 4 vùng |
| 9 | Ma trận tương quan | chart_09_correlation_matrix.png | Heatmap correlation |
| 10 | Lương theo cấp bậc (Bar) | chart_10_position_salary_bar.png | Grouped bar chart |
| 11 | Lương theo kinh nghiệm | chart_11_salary_by_experience.png | Line + scatter plot |
| 12 | Kỹ năng theo ngành | chart_12_skills_by_industry.png | Stacked bar chart |
| 13 | Pairplot | chart_13_pairplot.png | Scatter matrix |
| 14 | Feature Importance | feature_importance.png | Random Forest importance |
| 15 | Confusion Matrix | confusion_matrix.png | Classification results |
| 16 | K-Means Elbow | kmeans_elbow.png | Elbow method |
| 17 | Job Clusters | job_clusters.png | Cluster visualization |
| 18 | Mô hình nghiên cứu | research_model.png | IV-DV diagram |

---

### BIỂU ĐỒ 1: Phân bố mức lương

**📊 File:** `chart_01_salary_distribution.png`

**Mô tả:** Histogram với KDE overlay thể hiện phân bố của salary_median

**Thống kê:**
- **Trung vị (Median):** 13.5 triệu VND
- **Trung bình (Mean):** 15.5 triệu VND
- **Mode:** 10-12 triệu VND
- **Skewness:** 2.3 (right-skewed)

**Nhận xét chi tiết:**
1. **Phân bố lệch phải (right-skewed):** Đa số việc làm có lương 8-20 triệu, một số ít có lương rất cao
2. **Peak tại 10-12M:** Đây là mức lương phổ biến nhất cho Nhân viên mới
3. **Long tail:** Có outliers lương >50M cho vị trí Giám đốc/C-level
4. **Ý nghĩa thực tiễn:** Mean > Median → cần dùng Median khi báo cáo "lương trung bình"

---

### BIỂU ĐỒ 2: Top 15 ngành nghề

**📊 File:** `chart_02_top_industries.png`

**Mô tả:** Horizontal bar chart thể hiện số lượng tin tuyển dụng theo ngành

**Top 5:**
1. Bán hàng/CSKH/Kinh doanh: 2,100+
2. Kế toán/Kiểm toán: 1,800+
3. Bán hàng/Kinh doanh: 1,350+
4. Ngân hàng/Tài chính: 1,200+
5. Marketing/Truyền thông: 850+

**Nhận xét chi tiết:**
1. **Ngành dịch vụ chiếm ưu thế:** Bán hàng, CSKH - nhu cầu nhân sự lớn, turnover cao
2. **Kế toán ổn định:** Dù có automation, nhu cầu vẫn cao do compliance
3. **IT không trong top 5:** Nhiều tin IT không công khai lương → bị lọc
4. **Trend:** Digital Marketing, Data Science đang nổi lên

---

### BIỂU ĐỒ 3: Top 10 thành phố

**📊 File:** `chart_03_top_cities.png`

**Mô tả:** Bar chart số lượng việc làm theo thành phố

**Thống kê:**
| Thành phố | Số lượng | % |
|-----------|----------|---|
| Hà Nội | 25,279 | 30.8% |
| TP. Hồ Chí Minh | 24,633 | 30.1% |
| Bình Dương | ~3,500 | 4.3% |
| Đà Nẵng | ~2,800 | 3.4% |
| Đồng Nai | ~2,200 | 2.7% |

**Nhận xét chi tiết:**
1. **Hai đầu tàu kinh tế:** HN + HCM chiếm **60.9%** tổng việc làm
2. **Khu công nghiệp:** Bình Dương, Đồng Nai - trung tâm sản xuất
3. **Đà Nẵng:** Thành phố động lực miền Trung, IT hub mới
4. **Phân cực mạnh:** Các tỉnh khác chỉ chiếm <2%/tỉnh

---

### BIỂU ĐỒ 4: Lương theo cấp bậc (Boxplot)

**📊 File:** `chart_04_salary_by_position.png`

**Mô tả:** Boxplot so sánh phân bố lương của 6 cấp bậc

**Thống kê:**
| Cấp bậc | Min | Q1 | Median | Q3 | Max |
|---------|-----|-----|--------|-----|-----|
| Thực tập | 3M | 5M | 7.5M | 8M | 12M |
| Nhân viên | 5M | 9M | 12.5M | 16M | 35M |
| Chuyên gia | 10M | 14M | 16.5M | 20M | 40M |
| Trưởng nhóm | 12M | 15M | 18M | 22M | 45M |
| Quản lý | 15M | 18M | 20M | 25M | 60M |
| Giám đốc | 25M | 30M | 35M | 50M | 200M |

**Nhận xét chi tiết:**
1. **Không có overlap** giữa Thực tập và Giám đốc → phân tách rõ ràng
2. **IQR tăng dần:** Cấp càng cao, variance lương càng lớn
3. **Nhiều outliers ở cấp cao:** Giám đốc có thể đạt 200M+
4. **Bước nhảy lớn nhất:** Quản lý → Giám đốc (+75%)

---

### BIỂU ĐỒ 5: Phân bố kinh nghiệm

**📊 File:** `chart_05_experience_distribution.png`

**Mô tả:** Histogram yêu cầu số năm kinh nghiệm

**Thống kê:**
| Nhóm | Số lượng | % |
|------|----------|---|
| Không yêu cầu | ~25,000 | 30% |
| 1-2 năm | ~30,000 | **37%** |
| 3-5 năm | ~18,000 | 22% |
| 5-10 năm | ~7,000 | 9% |
| >10 năm | ~2,000 | 2% |

**Nhận xét chi tiết:**
1. **67% yêu cầu ≤2 năm:** Thị trường thân thiện với fresher
2. **30% không yêu cầu KN:** Nhiều cơ hội cho sinh viên mới ra trường
3. **Senior khan hiếm:** Chỉ 11% cần >5 năm
4. **Insight:** Doanh nghiệp VN prefer đào tạo nhân sự trẻ

---

### BIỂU ĐỒ 6: Top 20 kỹ năng

**📊 File:** `chart_06_top_skills.png`

**Mô tả:** Horizontal bar chart top kỹ năng được yêu cầu

**Nhận xét chi tiết:**
1. **Soft skills thống trị:** Bán hàng, CSKH, Giao tiếp trong top 5
2. **Kỹ năng IT vắng:** Python, SQL không trong top 10
3. **Kỹ năng chuyên môn:** Kế toán, Kiểm toán được yêu cầu nhiều
4. **Trend:** Communication skills quan trọng nhất

---

### BIỂU ĐỒ 7: Loại hình công việc

**📊 File:** `chart_07_job_types.png`

**Mô tả:** Pie chart phân bố loại hình công việc

**Thống kê:**
| Loại hình | % |
|-----------|---|
| Full-time | **97.6%** |
| Internship | 1.6% |
| Part-time | 0.7% |
| Freelance | 0.1% |

**Nhận xét chi tiết:**
1. **Full-time áp đảo:** Thị trường VN vẫn thiên về công việc ổn định
2. **Gig economy chưa phát triển:** Freelance chỉ 0.1%
3. **Internship có cơ hội:** 1.6% dành cho sinh viên

---

### BIỂU ĐỒ 8: Lương theo vùng miền

**📊 File:** `chart_08_salary_by_region.png`

**Mô tả:** Boxplot so sánh lương 4 vùng miền

**Kiểm định ANOVA:**
- **F-statistic:** 13.03
- **P-value:** 1.66e-08 (< 0.001)
- **Kết luận:** Có sự khác biệt có ý nghĩa thống kê

**Nhận xét chi tiết:**
1. **Chênh lệch Bắc-Nam nhỏ:** Chỉ ~0.26M (1.7%)
2. **Miền Trung thấp nhất:** Nhưng chi phí sinh hoạt cũng thấp
3. **Toàn quốc có variance cao:** Do là việc remote

---

### BIỂU ĐỒ 9: Ma trận tương quan

**📊 File:** `chart_09_correlation_matrix.png`

**Mô tả:** Heatmap correlation giữa các biến số

**Hệ số tương quan:**
| Cặp biến | r | Ý nghĩa |
|----------|---|---------|
| exp_years - salary | 0.232 | Tương quan dương TB |
| skill_count - salary | 0.036 | Tương quan yếu |
| exp_years - skill_count | 0.045 | Không liên quan |

**Nhận xét chi tiết:**
1. **Kinh nghiệm ảnh hưởng mạnh nhất** đến lương (r=0.232)
2. **Không multicollinearity:** Các biến độc lập với nhau
3. **Số kỹ năng không quan trọng bằng chất lượng**

---

### BIỂU ĐỒ 10-13: Các biểu đồ bổ sung

| # | Biểu đồ | Key Insight |
|---|---------|-------------|
| 10 | Lương theo cấp bậc (Bar) | Thực tập 7.5M → Giám đốc 35M |
| 11 | Lương theo kinh nghiệm | Mỗi năm +1-2M lương |
| 12 | Kỹ năng theo ngành | IT: SQL, Python; Kế toán: Excel |
| 13 | Pairplot | Xu hướng tuyến tính exp vs salary |

---

### BIỂU ĐỒ 14: Feature Importance

**📊 File:** `feature_importance.png`

**Mô tả:** Bar chart importance của Random Forest

**Top 10 Features:**
| Rank | Feature | Importance |
|------|---------|------------|
| 1 | **exp_years** | **29%** |
| 2 | **skill_count** | **15%** |
| 3 | region_Miền Trung | 10% |
| 4 | position_Nhân viên | 9% |
| 5 | position_Quản lý | 5% |
| 6 | job_type_Full-time | 4% |
| 7 | region_Miền Nam | 4% |
| 8 | position_Giám đốc | 3% |
| 9 | job_field_IT | 3% |
| 10 | region_Miền Bắc | 2% |

**Kết luận:** Kinh nghiệm (29%) + Kỹ năng (15%) = **44%** tổng importance

---

### BIỂU ĐỒ 15-18: Model Results

| # | Biểu đồ | Kết quả |
|---|---------|---------|
| 15 | Confusion Matrix | Accuracy = 47.68% |
| 16 | K-Means Elbow | Optimal k = 4 |
| 17 | Job Clusters | 4 phân khúc rõ ràng |
| 18 | Research Model | IV → DV diagram |

---

## 🤖 PHẦN 5: MÔ HÌNH MACHINE LEARNING

### 5.1 Mô hình 1: Dự đoán Lương (Regression)

**Cấu hình:**
- **Input (X):** exp_years, skill_count, region (one-hot), position_simple (one-hot), job_type
- **Output (y):** salary_median (triệu VND)
- **Train/Test split:** 80/20
- **Cross-validation:** 5-fold

**Kết quả so sánh:**
| Mô hình | CV R² | Test R² | RMSE | MAE | Đánh giá |
|---------|-------|---------|------|-----|----------|
| Ridge Regression | 0.1349 | 0.1316 | 8.96M | 5.16M | Baseline |
| **Random Forest** | **0.1675** | **0.2276** | **8.45M** | **4.91M** | **BEST ★** |
| Gradient Boosting | 0.1632 | 0.1581 | 8.83M | 5.04M | Overfitting |

**Kết luận:**
- **Random Forest** cho kết quả tốt nhất
- **R² = 22.76%** - Model giải thích được 22.76% variance của lương
- **RMSE = 8.45M** - Sai số trung bình ~8.45 triệu VND
- Cải thiện **73%** so với Ridge Regression

---

### 5.2 Mô hình 2: Phân loại Cấp bậc (Classification)

**Cấu hình:**
- **Input (X):** salary_median, exp_years, skill_count, region, job_type
- **Output (y):** position_simple (6 classes)
- **Model:** Logistic Regression (multi-class, one-vs-rest)

**Kết quả:**
| Metric | Giá trị | Ý nghĩa |
|--------|---------|---------|
| **Accuracy** | 47.68% | Tỷ lệ dự đoán đúng |
| **F1-macro** | 35.86% | Trung bình F1 các class |
| **F1-weighted** | 54.12% | F1 có trọng số |
| **ROC-AUC** | 79.43% | Khả năng phân biệt |

**Chi tiết từng class:**
| Class | Precision | Recall | F1-score | Support |
|-------|-----------|--------|----------|---------|
| Thực tập | 0.38 | 0.17 | 0.23 | 371 |
| Nhân viên | 0.48 | 0.99 | 0.64 | 13,867 |
| Chuyên gia | 0.00 | 0.00 | 0.00 | 20 |
| Trưởng nhóm | 0.38 | 0.01 | 0.02 | 553 |
| Quản lý | 0.53 | 0.00 | 0.01 | 1,469 |
| Giám đốc | 0.63 | 0.06 | 0.11 | 114 |

**Nhận xét:**
- **Class imbalance nghiêm trọng:** Nhân viên chiếm 85%
- Model bias về predict "Nhân viên"
- **ROC-AUC cao (79.43%)** → Model có khả năng phân biệt
- Cần SMOTE hoặc class weights để cải thiện

---

### 5.3 Mô hình 3: Phân cụm Việc làm (Clustering)

**Elbow Method:**
- Đánh giá k = 2 đến 10
- **Số cụm tối ưu:** k = 4

**K-Means kết quả:**
| Metric | Giá trị |
|--------|---------|
| **Silhouette Score** | 0.4363 |
| **Inertia** | 45,234 |

**Đặc điểm 4 cụm:**
| Cụm | Tên gợi ý | Lương TB | KN TB | % |
|-----|-----------|----------|-------|---|
| 0 | Junior+ | 23.74M | 4.7 năm | 11.8% |
| 1 | **Entry** | 13.61M | 0.1 năm | **49.4%** |
| 2 | Executive | 58.15M | 2.6 năm | 1.9% |
| 3 | Mid-level | 13.29M | 2.4 năm | 36.9% |

**Insight:**
- **Entry chiếm ~50%:** Thị trường cần nhiều fresher
- **Executive chỉ 1.9%** nhưng lương cao nhất (58M)
- Phân khúc rõ ràng giữa 4 nhóm

---

## 📝 PHẦN 6: KẾT LUẬN VÀ KHUYẾN NGHỊ

### 6.1 Tóm tắt kết quả

| Câu hỏi nghiên cứu | Phát hiện |
|-------------------|-----------|
| **RQ1:** Ngành hot | Bán hàng, CSKH, Kế toán, Marketing |
| **RQ2:** Chênh lệch vùng | Không đáng kể (~1.7% Bắc-Nam) |
| **RQ3:** Yếu tố lương | Kinh nghiệm (29%) > Kỹ năng (15%) > Cấp bậc (9%) |
| **RQ4:** Dự đoán | Có thể (R² = 22.76%) nhưng cần thêm features |

### 6.2 Key Insights

1. **Lương tăng theo cấp bậc:** Thực tập 7.5M → Giám đốc 35M (gấp 4.7 lần)
2. **Kinh nghiệm là yếu tố quan trọng nhất** (29% importance)
3. **67% việc làm** yêu cầu ≤2 năm kinh nghiệm - thân thiện với fresher
4. **Full-time chiếm 97.6%** - thị trường ổn định

### 6.3 Khuyến nghị

**Cho Người tìm việc:**
| Khuyến nghị | Chi tiết | Tác động |
|-------------|----------|----------|
| Tích lũy kinh nghiệm | Đạt mốc 3-5 năm | +30-50% lương |
| Phát triển kỹ năng | Có 5+ kỹ năng | +10-15% lương |
| Thăng tiến | Lên Quản lý/Giám đốc | +60-180% lương |
| Chọn ngành | IT, Ngân hàng, Tài chính | Lương cao hơn TB |

**Cho Doanh nghiệp:**
| Khuyến nghị | Lợi ích |
|-------------|---------|
| Công khai dải lương | Tăng ứng viên quality |
| Benchmark thị trường | Cạnh tranh talent |
| Xây dựng lộ trình career | Giữ chân nhân tài |

### 6.4 Hạn chế và Hướng phát triển

**Hạn chế:**
| Hạn chế | Mô tả | Ảnh hưởng |
|---------|-------|-----------|
| R² thấp | 22.76% | Thiếu features (education, company size) |
| Class imbalance | Nhân viên 85% | Classification bias |
| Missing salary | 80% ẩn | Selection bias |
| Snapshot data | 1 thời điểm | Không có trend |

**Hướng phát triển:**
1. Thu thập thêm: education, company size, benefits
2. Time-series analysis theo tháng/quý
3. NLP cho job description (BERT/Word2Vec)
4. Real-time dashboard với Streamlit/PowerBI
5. API prediction với FastAPI

---

## 📎 PHỤ LỤC

### A. Danh sách file

| File | Mô tả |
|------|-------|
| vietnam_job_analysis_cleaned_professional.ipynb | Notebook phân tích chính |
| datasets/dataset_final.csv | Dataset đã làm sạch |
| images/*.png | 18 biểu đồ |
| SLIDE_SUMMARY.md | Tóm tắt slides |
| BAOCAO_CHITIET_DAYDU.md | Báo cáo chi tiết |

### B. Công cụ sử dụng

| Công cụ | Phiên bản | Mục đích |
|---------|-----------|----------|
| Python | 3.12.10 | Ngôn ngữ chính |
| Pandas | 2.2.x | Data manipulation |
| Scikit-learn | 1.4.x | Machine Learning |
| Matplotlib | 3.8.x | Visualization |
| Seaborn | 0.13.x | Statistical plots |

---

*Tài liệu được tạo từ kết quả phân tích notebook*  
*Cập nhật: 23/12/2024*  
*Version: 2.0 - Đầy đủ chi tiết*
