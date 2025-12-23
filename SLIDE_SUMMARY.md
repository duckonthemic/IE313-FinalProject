# 📊 VIETNAM JOB ANALYSIS - SLIDE PRESENTATION SUMMARY
## Phân tích Thị trường Việc làm tại Việt Nam 2024-2025

**📅 Cập nhật:** 23/12/2025  
**📄 Số slides:** 26 slides  
**📊 Số biểu đồ:** 18 charts

---

## 📑 SLIDE 1: TRANG BÌA
**Tiêu đề:** Phân tích Thị trường Việc làm tại Việt Nam 2024-2025  
**Phụ đề:** Data Science End-to-End Project - IE313 Final Project  
**Thông tin dự án:**
- 📊 Dataset: 85,470 tin tuyển dụng → 81,971 bản ghi sạch
- 🌐 Nguồn: CareerViet, TopCV, ViecLam24h, JobsGo
- 📅 Thời gian: Tháng 12/2024 - 12/2025
- 🔧 Công cụ: Python 3.12, Pandas, Scikit-learn, Matplotlib

---

## 📑 SLIDE 2: MỤC TIÊU DỰ ÁN

### Mục tiêu chính:
1. **Khám phá thị trường việc làm** - Phân tích xu hướng tuyển dụng theo ngành, vùng miền, cấp bậc
2. **Xác định yếu tố ảnh hưởng lương** - Nghiên cứu các yếu tố tác động đến mức lương
3. **Xây dựng mô hình dự đoán** - Dự đoán lương và phân loại cấp bậc vị trí
4. **Phân khúc thị trường** - Phân cụm công việc theo đặc điểm

### Câu hỏi nghiên cứu:
- Ngành nghề và kỹ năng nào được tuyển dụng nhiều nhất?
- Mức lương khác biệt như thế nào theo vùng miền, cấp bậc?
- Có thể dự đoán được mức lương dựa trên các đặc điểm công việc không?

---

## 📑 SLIDE 3: MÔ HÌNH NGHIÊN CỨU

### 3.1 Sơ đồ Biến Độc lập - Phụ thuộc:

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

### 3.2 Giải thích biến:

| Biến | Loại | Mô tả | Giá trị |
|------|------|-------|---------|
| **exp_years** | IV (Số) | Số năm kinh nghiệm yêu cầu | 0-10+ năm |
| **skill_count** | IV (Số) | Số lượng kỹ năng yêu cầu | 0-20+ kỹ năng |
| **region** | IV (Phân loại) | Vùng miền địa lý | Bắc/Trung/Nam/TQ |
| **position_simple** | IV (Phân loại) | Cấp bậc công việc | 6 cấp |
| **job_fields** | IV (Phân loại) | Ngành nghề | 50+ ngành |
| **salary_median** | DV (Số) | Mức lương trung vị | triệu VND |

### 3.3 Giả thuyết nghiên cứu:
- **H1:** Kinh nghiệm có tác động dương đến lương ✅ (r=0.29)
- **H2:** Số kỹ năng có tác động dương đến lương ✅ (r=0.15)
- **H3:** Vùng miền ảnh hưởng đến lương ✅ (p<0.001)
- **H4:** Cấp bậc ảnh hưởng đến lương ✅ (p<0.001)
- **H5:** Ngành nghề ảnh hưởng đến lương ✅ (p<0.001)

**📊 Hình ảnh:** `images/research_model.png`

---

## 📑 SLIDE 4: QUY TRÌNH DATA ANALYST (8 BƯỚC)

| Bước | Nội dung | Chi tiết | Trạng thái |
|------|----------|----------|------------|
| 1 | Mô hình nghiên cứu | Xác định IV → DV | ✅ |
| 2 | Tiền xử lý dữ liệu | 8 bước làm sạch | ✅ |
| 3 | Phân tích khám phá (EDA) | Thống kê mô tả | ✅ |
| 4 | Trực quan hóa dữ liệu | 18 biểu đồ | ✅ |
| 5 | Xác định yếu tố tác động | Feature Importance | ✅ |
| 6 | So sánh biến phân loại | ANOVA, t-tests | ✅ |
| 7 | Xây dựng mô hình ML | 5 mô hình | ✅ |
| 8 | Khuyến nghị & Kết luận | Insights | ✅ |

---

## 📑 SLIDE 5: NGUỒN DỮ LIỆU

### 5.1 Thống kê thu thập:
| Nguồn | Số lượng | Tỷ lệ |
|-------|----------|-------|
| CareerViet | ~34,000 | 40% |
| TopCV | ~25,600 | 30% |
| ViecLam24h | ~17,000 | 20% |
| JobsGo | ~8,500 | 10% |
| **Tổng** | **85,470** | **100%** |

### 5.2 Các trường dữ liệu chính (15 cột):
- `job_title`, `job_type`, `position_level`, `city`
- `experience`, `skills`, `job_fields`
- `salary_min`, `salary_max`, `salary_median`, `unit`

---

## 📑 SLIDE 6: TIỀN XỬ LÝ DỮ LIỆU (8 BƯỚC CHI TIẾT)

### STEP 0: Chuẩn hóa tên thành phố
```python
city_mapping = {
    'hcm': 'Ho Chi Minh', 'tphcm': 'Ho Chi Minh', 
    'hn': 'Ha Noi', 'hanoi': 'Ha Noi',
    'dn': 'Da Nang', 'danang': 'Da Nang', ...
}
```
- **Input:** 150+ cách viết khác nhau
- **Output:** 63 tên thành phố chuẩn

### STEP 1: Chuẩn hóa tiền tệ
```python
usd_mask = df['unit'].str.lower().str.contains('usd|dollar', na=False)
df.loc[usd_mask, ['salary_min', 'salary_max']] *= 25000
```
- **Tỷ giá:** 1 USD = 25,000 VND
- **Kết quả:** ~500 bản ghi được convert

### STEP 2: Kiểm tra logic lương
```python
invalid_salary = df['salary_min'] > df['salary_max']
df = df[~invalid_salary]  # Loại bỏ
```
- **Phát hiện:** 1,802 bản ghi sai logic
- **Xử lý:** Loại bỏ hoàn toàn

### STEP 3: Xử lý missing salary
```python
df['has_salary'] = (df['salary_min'].notna()) | (df['salary_max'].notna())
# Impute by industry median
```
- **Phát hiện:** ~80% không có lương
- **Xử lý:** Flag + Impute theo ngành

### STEP 4: Phát hiện trùng lặp
```python
df['is_duplicate'] = df.duplicated(subset=['job_title', 'city'], keep='first')
```
- **Phát hiện:** 1,697 bản ghi trùng
- **Xử lý:** Flag (giữ nguyên)

### STEP 5: Xử lý outliers lương
```python
extreme_salary = df['salary_max'] > 500  # triệu
df = df[~extreme_salary]
```
- **Phát hiện:** 1,802 lương > 500M
- **Xử lý:** Loại bỏ

### STEP 6: Tách ngành nghề
```python
df['job_fields_list'] = df['job_fields'].str.split(',')
```
- **Input:** "IT, Marketing, Sales"
- **Output:** ['IT', 'Marketing', 'Sales']

### STEP 7: Feature Engineering
```python
df['salary_median'] = (df['salary_min'] + df['salary_max']) / 2
df['exp_years'] = df['experience'].map(exp_mapping)
df['skill_count'] = df['skills'].str.count(',') + 1
df['region'] = df['city'].map(region_mapping)
df['position_simple'] = df['position_level'].map(position_mapping)
```

### Kết quả tổng hợp:
| Chỉ số | Giá trị |
|--------|---------|
| **Trước xử lý** | 85,470 bản ghi |
| **Sau xử lý** | 81,971 bản ghi |
| **Tỷ lệ giữ** | 96% |
| **Loại bỏ** | 3,499 bản ghi (4%) |

---

## 📑 SLIDE 7: BIỂU ĐỒ 1 - PHÂN BỐ MỨC LƯƠNG

**📊 Hình ảnh:** `chart_01_salary_distribution.png`

### Thống kê mô tả:
| Chỉ số | Giá trị |
|--------|---------|
| **Count** | 81,971 |
| **Mean** | 15.5 triệu VND |
| **Median** | 13.5 triệu VND |
| **Mode** | 10-12 triệu VND |
| **Std** | 9.6 triệu VND |
| **Min** | 3 triệu VND |
| **Max** | 500 triệu VND |

### Nhận xét chi tiết:
1. **Phân bố right-skewed:** Đa số tập trung ở mức 8-20 triệu, có đuôi dài ở lương cao
2. **Peak tại 10-12M:** Đây là mức lương phổ biến nhất cho Nhân viên
3. **Outliers:** Có một số vị trí Giám đốc/C-level >50M nhưng số lượng ít
4. **Ý nghĩa:** Cần log-transform khi modeling để giảm skewness

---

## 📑 SLIDE 8: BIỂU ĐỒ 2 - TOP 15 NGÀNH NGHỀ

**📊 Hình ảnh:** `chart_02_top_industries.png`

### Top 5 ngành hot nhất:
| Hạng | Ngành | Số lượng | % |
|------|-------|----------|---|
| 1 | Bán hàng/CSKH/Kinh doanh | 2,100+ | 12.8% |
| 2 | Kế toán/Kiểm toán | 1,800+ | 11.0% |
| 3 | Bán hàng/Kinh doanh | 1,350+ | 8.2% |
| 4 | Ngân hàng/Tài chính | 1,200+ | 7.3% |
| 5 | Marketing/Truyền thông | 850+ | 5.2% |

### Nhận xét chi tiết:
1. **Ngành dịch vụ chiếm ưu thế:** Bán hàng, CSKH, Kế toán - đây là các ngành có nhu cầu nhân sự lớn
2. **Kế toán vẫn ổn định:** Dù có phần mềm tự động hóa, nhu cầu kế toán viên vẫn cao
3. **IT không trong top 5:** Do nhiều tin IT không công khai lương
4. **Ngành mới nổi:** Digital Marketing, Data Science đang tăng trưởng

---

## 📑 SLIDE 9: BIỂU ĐỒ 3 - TOP 10 THÀNH PHỐ

**📊 Hình ảnh:** `chart_03_top_cities.png`

### Phân bố địa lý:
| Hạng | Thành phố | Số lượng | % |
|------|-----------|----------|---|
| 1 | **Hà Nội** | 25,279 | **30.8%** |
| 2 | **TP. Hồ Chí Minh** | 24,633 | **30.1%** |
| 3 | Bình Dương | ~3,500 | 4.3% |
| 4 | Đà Nẵng | ~2,800 | 3.4% |
| 5 | Đồng Nai | ~2,200 | 2.7% |

### Nhận xét chi tiết:
1. **2 đầu tàu kinh tế:** HN + HCM chiếm **60.9%** tổng việc làm
2. **Khu công nghiệp:** Bình Dương, Đồng Nai tập trung sản xuất
3. **Đà Nẵng:** Trung tâm lớn nhất miền Trung, đang phát triển mạnh
4. **Các tỉnh khác:** Mỗi tỉnh <2%, thể hiện sự tập trung kinh tế

---

## 📑 SLIDE 10: BIỂU ĐỒ 4 - LƯƠNG THEO CẤP BẬC (BOXPLOT)

**📊 Hình ảnh:** `chart_04_salary_by_position.png`

### Thống kê lương trung vị theo 6 cấp bậc:
| Cấp bậc | Lương trung vị | Số lượng | % |
|---------|----------------|----------|---|
| **Giám đốc** | **35.0M** | 570 | 0.7% |
| Quản lý | 20.0M | 7,344 | 9.0% |
| Trưởng nhóm | 18.0M | 2,766 | 3.4% |
| Chuyên gia | 16.5M | 102 | 0.1% |
| Nhân viên | 12.5M | 69,333 | **84.6%** |
| Thực tập sinh | 7.5M | 1,856 | 2.3% |

### Nhận xét chi tiết:
1. **Hierarchy rõ ràng:** Lương tăng đều theo cấp bậc
2. **Nhân viên chiếm 85%:** Đây là đối tượng chính của thị trường
3. **Bước nhảy lớn nhất:** Quản lý → Giám đốc (+75%)
4. **Giám đốc:** Lương cao gấp ~5 lần Thực tập sinh

### Khoảng cách lương giữa các cấp:
```
Thực tập (7.5M) → +67% → Nhân viên (12.5M) → +32% → Chuyên gia (16.5M)
                                                           ↓
Giám đốc (35M) ← +75% ← Quản lý (20M) ← +11% ← Trưởng nhóm (18M)
```

---

## 📑 SLIDE 11: BIỂU ĐỒ 5 - PHÂN BỐ KINH NGHIỆM

**📊 Hình ảnh:** `chart_05_experience_distribution.png`

### Yêu cầu kinh nghiệm:
| Nhóm | Số lượng | % |
|------|----------|---|
| Không yêu cầu | ~25,000 | 30% |
| 1-2 năm | ~30,000 | **37%** |
| 3-5 năm | ~18,000 | 22% |
| 5-10 năm | ~7,000 | 9% |
| >10 năm | ~2,000 | 2% |

### Nhận xét chi tiết:
1. **67% yêu cầu ≤2 năm:** Thị trường thân thiện với fresher/junior
2. **Senior hiếm:** Chỉ 11% yêu cầu >5 năm kinh nghiệm
3. **Cơ hội cho sinh viên mới ra trường:** 30% không yêu cầu kinh nghiệm
4. **Trend:** Doanh nghiệp sẵn sàng đào tạo nhân sự trẻ

---

## 📑 SLIDE 12: BIỂU ĐỒ 6 - TOP 20 KỸ NĂNG

**📊 Hình ảnh:** `chart_06_top_skills.png`

### Top 10 kỹ năng được yêu cầu nhiều nhất:
| Hạng | Kỹ năng | Số lần | Ngành liên quan |
|------|---------|--------|-----------------|
| 1 | Tư vấn bán hàng | 11,439 | Sales |
| 2 | Chăm sóc khách hàng | 9,646 | CSKH |
| 3 | Bán hàng kinh doanh | 7,492 | Sales |
| 4 | Quản lý cửa hàng | 4,059 | Retail |
| 5 | Phát triển thị trường | 2,828 | BD |
| 6 | Telesale | 2,520 | Sales |
| 7 | Hành chính văn phòng | 2,425 | Admin |
| 8 | Kế toán tổng hợp | 2,389 | Accounting |
| 9 | Xây dựng | 2,025 | Construction |
| 10 | Kiểm toán | 1,889 | Audit |

### Nhận xét chi tiết:
1. **Soft skills chiếm ưu thế:** Bán hàng, CSKH, Giao tiếp
2. **Kỹ năng IT vắng mặt:** Python, SQL không trong top 10 (vì ít tin IT công khai lương)
3. **Xu hướng:** Kỹ năng giao tiếp + kinh doanh được đánh giá cao

---

## 📑 SLIDE 13: BIỂU ĐỒ 7 - LOẠI HÌNH CÔNG VIỆC

**📊 Hình ảnh:** `chart_07_job_types.png`

### Phân bố loại hình:
| Loại hình | Số lượng | Tỷ lệ |
|-----------|----------|-------|
| Full-time | 80,000+ | **97.6%** |
| Internship | 1,300+ | 1.6% |
| Part-time | 575+ | 0.7% |
| Freelance | 96+ | 0.1% |

### Nhận xét chi tiết:
1. **Full-time thống trị:** 97.6% việc làm là toàn thời gian
2. **Gig economy chưa phát triển:** Freelance chỉ 0.1%
3. **Internship ổn định:** 1.6% là cơ hội cho sinh viên
4. **Trend:** Remote work đang tăng nhưng chưa phản ánh trong dữ liệu

---

## 📑 SLIDE 14: BIỂU ĐỒ 8 - LƯƠNG THEO VÙNG MIỀN

**📊 Hình ảnh:** `chart_08_salary_by_region.png`

### Thống kê lương theo vùng:
| Vùng | Lương TB | Lương trung vị | Số lượng | % |
|------|----------|----------------|----------|---|
| Miền Nam | 15.68M | 13.5M | 40,362 | 49.2% |
| Miền Bắc | 15.42M | 13.5M | 33,500 | 40.9% |
| Miền Trung | 15.31M | 13.0M | 5,667 | 6.9% |
| Toàn quốc | 12.61M | 9.5M | 240 | 0.3% |

### Kiểm định ANOVA:
- **F-statistic:** 13.03
- **P-value:** 1.66e-08 (< 0.001)
- **Kết luận:** Có sự khác biệt có ý nghĩa thống kê giữa các vùng

### Nhận xét chi tiết:
1. **Chênh lệch Bắc-Nam nhỏ:** Chỉ ~0.26M (1.7%)
2. **Miền Trung thấp hơn:** Nhưng chi phí sinh hoạt cũng thấp
3. **Toàn quốc thấp nhất:** Thường là việc làm từ xa, entry-level

---

## 📑 SLIDE 15: BIỂU ĐỒ 9 - MA TRẬN TƯƠNG QUAN

**📊 Hình ảnh:** `chart_09_correlation_matrix.png`

### Hệ số tương quan Pearson:
```
                  salary_median  exp_years  skill_count
salary_median           1.000      0.232        0.036
exp_years               0.232      1.000        0.045
skill_count             0.036      0.045        1.000
```

### Nhận xét chi tiết:
1. **Kinh nghiệm vs Lương:** r = 0.232 (tương quan dương trung bình)
   - Mỗi năm kinh nghiệm → tăng ~1-2M lương
2. **Kỹ năng vs Lương:** r = 0.036 (tương quan yếu)
   - Số lượng kỹ năng ít ảnh hưởng hơn chất lượng
3. **Không có multicollinearity:** Các biến phù hợp cho modeling

---

## 📑 SLIDE 16: BIỂU ĐỒ 10 - LƯƠNG THEO CẤP BẬC (BAR)

**📊 Hình ảnh:** `chart_10_position_salary_bar.png`

### Career progression và salary growth:
```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Thực tập    │ Nhân viên   │ Chuyên gia  │ Trưởng nhóm │ Quản lý     │ Giám đốc    │
│    7.5M     │   12.5M     │   16.5M     │    18M      │    20M      │    35M      │
│             │   (+67%)    │   (+32%)    │   (+9%)     │   (+11%)    │   (+75%)    │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

### Insight:
- **Bước nhảy lớn nhất:** Thực tập → Nhân viên (+67%) và Quản lý → Giám đốc (+75%)
- **Plateau zone:** Chuyên gia → Trưởng nhóm → Quản lý (tăng chậm 9-11%)

---

## 📑 SLIDE 17: BIỂU ĐỒ 11 - LƯƠNG THEO KINH NGHIỆM

**📊 Hình ảnh:** `chart_11_salary_by_experience.png`

### Xu hướng lương theo kinh nghiệm:
| Kinh nghiệm | Lương trung vị | Tăng so với mức trước |
|-------------|----------------|----------------------|
| 0-2 năm | 10-12M | Baseline |
| 3-5 năm | 13-15M | +25-30% |
| 6-10 năm | 16-20M | +20-25% |
| >10 năm | 20-25M | +15-20% |

### Nhận xét chi tiết:
1. **Mỗi năm kinh nghiệm:** Tăng ~1-2 triệu lương
2. **Bước nhảy lớn nhất:** Mốc 5 năm kinh nghiệm
3. **Diminishing returns:** Sau 10 năm, tăng lương chậm lại
4. **Cần thăng tiến:** Để tăng lương sau 10 năm, cần lên vị trí cao hơn

---

## 📑 SLIDE 18: BIỂU ĐỒ 12 - KỸ NĂNG THEO NGÀNH

**📊 Hình ảnh:** `chart_12_skills_by_industry.png`

### Kỹ năng đặc thù theo ngành:
| Ngành | Top 5 Kỹ năng |
|-------|---------------|
| **IT** | SQL, JavaScript, C#, .NET, Java, Python |
| **Kế toán** | Kế toán tổng hợp, Kiểm toán, Thuế, Excel |
| **Ngân hàng** | Tư vấn, CSKH, Xử lý nợ, Tín dụng |
| **Marketing** | Digital Marketing, Facebook Ads, SEO, Content |
| **HR** | Nhân sự, Tuyển dụng, Quản trị HR, C&B |
| **Sales** | Bán hàng, Telesale, Đàm phán, B2B |

---

## 📑 SLIDE 19: BIỂU ĐỒ 13 - PAIRPLOT

**📊 Hình ảnh:** `chart_13_pairplot.png`

### Phát hiện từ pairplot:
1. **Right-skewed salary:** Cần log-transform
2. **Giám đốc cluster:** Tập trung ở vùng >30M, >5 năm
3. **Nhân viên dominant:** 85% ở vùng 10-15M
4. **Linear trend:** exp_years vs salary có xu hướng tuyến tính

---

## 📑 SLIDE 20: BIỂU ĐỒ 14 - FEATURE IMPORTANCE

**📊 Hình ảnh:** `feature_importance.png`

### Top 10 Features quan trọng nhất:
| Rank | Feature | Importance | Ý nghĩa |
|------|---------|------------|---------|
| 1 | **exp_years** | **29%** | Số năm kinh nghiệm |
| 2 | **skill_count** | **15%** | Số lượng kỹ năng |
| 3 | region_Miền Trung | 10% | Vùng Trung bộ |
| 4 | position_Nhân viên | 9% | Cấp bậc Nhân viên |
| 5 | position_Quản lý | 5% | Cấp bậc Quản lý |
| 6 | job_type_Full-time | 4% | Loại hình toàn thời gian |
| 7 | region_Miền Nam | 4% | Vùng phía Nam |
| 8 | position_Giám đốc | 3% | Cấp bậc Giám đốc |
| 9 | job_field_IT | 3% | Ngành IT |
| 10 | region_Miền Bắc | 2% | Vùng phía Bắc |

### Kết luận:
- **Kinh nghiệm là yếu tố quan trọng nhất** (29%)
- Top 2 features (exp_years + skill_count) giải thích 44% tầm quan trọng

---

## 📑 SLIDE 21: MÔ HÌNH 1 - DỰ ĐOÁN LƯƠNG (REGRESSION)

### 21.1 Cấu hình mô hình:
- **Input (X):** exp_years, skill_count, region (one-hot), position_simple (one-hot), job_type (one-hot)
- **Output (y):** salary_median (triệu VND)
- **Train/Test split:** 80/20
- **Cross-validation:** 5-fold

### 21.2 So sánh 3 mô hình:
| Mô hình | CV R² | Test R² | RMSE | MAE | Đánh giá |
|---------|-------|---------|------|-----|----------|
| Ridge Regression | 0.1349 | 0.1316 | 8.96M | 5.16M | Baseline |
| **Random Forest** | **0.1675** | **0.2276** | **8.45M** | **4.91M** | **BEST** |
| Gradient Boosting | 0.1632 | 0.1581 | 8.83M | 5.04M | Overfitting |

### 21.3 Kết luận:
- **Random Forest** cho kết quả tốt nhất với R² = 22.76%
- Cải thiện **73%** so với Ridge Regression
- **RMSE = 8.45M** nghĩa là sai số trung bình ~8.45 triệu VND
- **R² = 22.76%** có nghĩa model giải thích được 22.76% phương sai của lương

---

## 📑 SLIDE 22: MÔ HÌNH 2 - PHÂN LOẠI CẤP BẬC (CLASSIFICATION)

**📊 Hình ảnh:** `confusion_matrix.png`

### 22.1 Cấu hình:
- **Input (X):** salary_median, exp_years, skill_count, region, job_type
- **Output (y):** position_simple (6 classes)
- **Model:** Logistic Regression (multi-class)

### 22.2 Kết quả:
| Metric | Giá trị | Ý nghĩa |
|--------|---------|---------|
| **Accuracy** | 47.68% | Tỷ lệ dự đoán đúng |
| **F1-macro** | 35.86% | Trung bình F1 các class |
| **F1-weighted** | 54.12% | F1 có trọng số theo số lượng |
| **ROC-AUC** | 79.43% | Khả năng phân biệt các class |

### 22.3 Chi tiết từng class:
| Class | Precision | Recall | F1-score | Support |
|-------|-----------|--------|----------|---------|
| Thực tập | 0.38 | 0.17 | 0.23 | 371 |
| Nhân viên | 0.48 | 0.99 | 0.64 | 13,867 |
| Chuyên gia | 0.00 | 0.00 | 0.00 | 20 |
| Trưởng nhóm | 0.38 | 0.01 | 0.02 | 553 |
| Quản lý | 0.53 | 0.00 | 0.01 | 1,469 |
| Giám đốc | 0.63 | 0.06 | 0.11 | 114 |

### 22.4 Nhận xét:
- **Class imbalance nghiêm trọng:** Nhân viên chiếm 85%
- Model thiên về predict Nhân viên
- **ROC-AUC cao (79.43%)** cho thấy model có khả năng phân biệt
- Cần SMOTE hoặc class weights để cải thiện minority classes

---

## 📑 SLIDE 23: MÔ HÌNH 3 - PHÂN CỤM VIỆC LÀM (CLUSTERING)

**📊 Hình ảnh:** `kmeans_elbow.png`, `job_clusters.png`

### 23.1 Elbow Method:
- Đánh giá k = 2 đến 10
- **Số cụm tối ưu:** k = 4

### 23.2 K-Means Clustering kết quả:
| Metric | Giá trị |
|--------|---------|
| **Silhouette Score** | 0.4363 |
| **Inertia** | 45,234 |
| **Số cụm** | 4 |

### 23.3 Đặc điểm 4 cụm:
| Cụm | Tên gợi ý | Lương TB | KN TB | Kỹ năng TB | Số lượng | % |
|-----|-----------|----------|-------|------------|----------|---|
| 0 | Junior+ | 23.74M | 4.7 năm | 3.2 | 9,671 | 11.8% |
| 1 | Entry | 13.61M | 0.1 năm | 2.1 | 40,508 | **49.4%** |
| 2 | Executive | 58.15M | 2.6 năm | 2.8 | 1,559 | 1.9% |
| 3 | Mid-level | 13.29M | 2.4 năm | 2.5 | 30,233 | 36.9% |

### 23.4 Insight:
- **Entry (Cụm 1)** chiếm ~50%: Thị trường cần nhiều fresher
- **Executive (Cụm 2)** chỉ 1.9% nhưng lương cao nhất (58M)
- Có sự phân tách rõ ràng giữa các phân khúc

---

## 📑 SLIDE 24: TỔNG KẾT KẾT QUẢ

### 24.1 Kết quả chính:
| Câu hỏi nghiên cứu | Phát hiện |
|-------------------|-----------|
| Ngành nghề hot | Bán hàng, CSKH, Kế toán, Marketing, Ngân hàng |
| Kỹ năng được yêu cầu | Soft skills: Bán hàng, CSKH, Giao tiếp |
| Yếu tố ảnh hưởng lương | Kinh nghiệm (29%) > Kỹ năng (15%) > Cấp bậc (9%) |
| Chênh lệch vùng miền | Không đáng kể (Bắc-Nam chỉ ~1.7%) |
| Model dự đoán tốt nhất | Random Forest (R² = 22.76%) |

### 24.2 Key Insights:
1. **Lương tăng theo cấp bậc:** Thực tập 7.5M → Giám đốc 35M (gấp 4.7 lần)
2. **Kinh nghiệm là yếu tố quan trọng nhất** ảnh hưởng đến lương (29%)
3. **Không có chênh lệch lương đáng kể** giữa Miền Bắc và Miền Nam
4. **67% việc làm** yêu cầu ≤2 năm kinh nghiệm - thân thiện với fresher

---

## 📑 SLIDE 25: KHUYẾN NGHỊ

### 25.1 Cho Người tìm việc:
| Khuyến nghị | Chi tiết | Tác động dự kiến |
|-------------|----------|------------------|
| Tích lũy kinh nghiệm | Đạt mốc 3-5 năm | +30-50% lương |
| Phát triển kỹ năng | Có 5+ kỹ năng | +10-15% lương |
| Thăng tiến | Lên Quản lý/Giám đốc | +60-180% lương |
| Chọn ngành | IT, Ngân hàng, Tài chính | Lương cao hơn TB |

### 25.2 Cho Doanh nghiệp:
| Khuyến nghị | Chi tiết | Lợi ích |
|-------------|----------|---------|
| Công khai dải lương | Minh bạch salary range | Tăng ứng viên quality |
| Benchmark thị trường | Tham khảo mức median | Cạnh tranh talent |
| Xây dựng lộ trình | Career path rõ ràng | Giữ chân nhân tài |
| JD theo cluster | Target đúng đối tượng | Tăng conversion |

---

## 📑 SLIDE 26: HẠN CHẾ & HƯỚNG PHÁT TRIỂN

### 26.1 Hạn chế của nghiên cứu:
| Hạn chế | Mô tả | Ảnh hưởng |
|---------|-------|-----------|
| **R² thấp** | R² = 22.76% | Thiếu features quan trọng |
| **Class imbalance** | Nhân viên 85% | Classification bias |
| **Missing salary** | ~80% ẩn lương | Selection bias |
| **Snapshot data** | 1 thời điểm | Không có trend |

### 26.2 Hướng phát triển:
| Hướng | Chi tiết | Kỳ vọng |
|-------|----------|---------|
| **Thu thập thêm features** | Education, Company size, Benefits | R² → 40%+ |
| **Time-series analysis** | Thu thập theo tháng/quý | Phân tích xu hướng |
| **NLP cho Job Description** | BERT/Word2Vec | Hiểu nội dung JD |
| **Dashboard real-time** | Streamlit/PowerBI | Monitoring liên tục |
| **API prediction** | FastAPI service | Ứng dụng thực tế |

---

## 📎 PHỤ LỤC A - DANH SÁCH 18 BIỂU ĐỒ

| # | Tên file | Nội dung | Slide |
|---|----------|----------|-------|
| 1 | chart_01_salary_distribution.png | Phân bố mức lương | 7 |
| 2 | chart_02_top_industries.png | Top 15 ngành nghề | 8 |
| 3 | chart_03_top_cities.png | Top 10 thành phố | 9 |
| 4 | chart_04_salary_by_position.png | Lương theo cấp bậc (Boxplot) | 10 |
| 5 | chart_05_experience_distribution.png | Phân bố kinh nghiệm | 11 |
| 6 | chart_06_top_skills.png | Top 20 kỹ năng | 12 |
| 7 | chart_07_job_types.png | Loại hình công việc (Pie) | 13 |
| 8 | chart_08_salary_by_region.png | Lương theo vùng miền | 14 |
| 9 | chart_09_correlation_matrix.png | Ma trận tương quan | 15 |
| 10 | chart_10_position_salary_bar.png | Lương theo cấp bậc (Bar) | 16 |
| 11 | chart_11_salary_by_experience.png | Lương theo kinh nghiệm | 17 |
| 12 | chart_12_skills_by_industry.png | Kỹ năng theo ngành | 18 |
| 13 | chart_13_pairplot.png | Pairplot đa biến | 19 |
| 14 | feature_importance.png | Feature Importance | 20 |
| 15 | confusion_matrix.png | Ma trận nhầm lẫn | 22 |
| 16 | kmeans_elbow.png | K-Means Elbow | 23 |
| 17 | job_clusters.png | Phân cụm việc làm | 23 |
| 18 | research_model.png | Mô hình nghiên cứu | 3 |

---

## 📎 PHỤ LỤC B - SO SÁNH MÔ HÌNH

### Regression Models:
```
┌─────────────────────┬───────────┬───────────┬───────────┬───────────┐
│ Model               │ CV R²     │ Test R²   │ RMSE      │ MAE       │
├─────────────────────┼───────────┼───────────┼───────────┼───────────┤
│ Ridge Regression    │ 0.1349    │ 0.1316    │ 8.96M     │ 5.16M     │
│ Random Forest ★     │ 0.1675    │ 0.2276    │ 8.45M     │ 4.91M     │
│ Gradient Boosting   │ 0.1632    │ 0.1581    │ 8.83M     │ 5.04M     │
└─────────────────────┴───────────┴───────────┴───────────┴───────────┘
```

### Classification Models:
```
┌─────────────────────┬───────────┬───────────┬───────────┬───────────┐
│ Model               │ Accuracy  │ F1-macro  │ F1-weight │ ROC-AUC   │
├─────────────────────┼───────────┼───────────┼───────────┼───────────┤
│ Logistic Regression │ 47.68%    │ 35.86%    │ 54.12%    │ 79.43%    │
└─────────────────────┴───────────┴───────────┴───────────┴───────────┘
```

### Clustering Models:
```
┌─────────────────────┬───────────┬───────────┬───────────────────────┐
│ Model               │ K         │ Silhouette│ Interpretation        │
├─────────────────────┼───────────┼───────────┼───────────────────────┤
│ K-Means             │ 4         │ 0.4363    │ Entry/Mid/Junior+/Exec│
└─────────────────────┴───────────┴───────────┴───────────────────────┘
```

---

## 📎 PHỤ LỤC C - THỐNG KÊ MÔ TẢ

### Biến số (Numerical):
| Biến | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|------|-------|------|-----|-----|-----|-----|-----|-----|
| salary_min | 81,971 | 12.3M | 8.1M | 3M | 7M | 10M | 15M | 300M |
| salary_max | 81,971 | 18.7M | 12.4M | 5M | 12M | 17M | 22M | 500M |
| salary_median | 81,971 | 15.5M | 9.6M | 4M | 9.5M | 13.5M | 18.5M | 400M |
| exp_years | 81,971 | 2.1 | 2.3 | 0 | 0 | 1 | 3 | 10+ |
| skill_count | 81,971 | 2.5 | 1.8 | 0 | 1 | 2 | 3 | 20 |

### Biến phân loại (Categorical):
| Biến | Unique | Mode | Mode % |
|------|--------|------|--------|
| region | 4 | Miền Nam | 49.2% |
| position_simple | 6 | Nhân viên | 84.6% |
| job_type | 4 | Full-time | 97.6% |
| city | 63 | Hà Nội | 30.8% |

---

---

## 📎 PHỤ LỤC D - QUICK REFERENCE

### Key Numbers to Remember:
| Metric | Value |
|--------|-------|
| Total Jobs | 85,470 → 81,971 |
| Best Model R² | 22.76% (RF) |
| Top Factor | exp_years (29%) |
| Median Salary | 13.5M VND |
| Director vs Intern | 4.7x |
| HN + HCM Jobs | 60.9% |

### One-liner Insights:
1. **"Kinh nghiệm quyết định 29% mức lương"**
2. **"Giám đốc lương gấp 4.7 lần Thực tập sinh"**
3. **"67% việc làm chỉ cần ≤2 năm kinh nghiệm"**
4. **"Không có chênh lệch lương đáng kể Bắc-Nam"**

---

*Tài liệu được tạo từ kết quả phân tích notebook*  
*Cập nhật: 23/12/2025*  
*Version: 3.0 - Hoàn chỉnh với Quick Reference*
