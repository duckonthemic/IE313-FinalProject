# Master Schema Documentation

## 📋 Tổng quan

Master schema là cấu trúc dữ liệu thống nhất được thiết kế để **gộp nhiều nguồn dữ liệu việc làm IT từ các nền tảng khác nhau** (Kaggle/ITViec, GitHub/Multi-source) về một **cấu trúc duy nhất**, chuẩn hóa và nhất quán.

### 🎯 Mục tiêu

- **Thống nhất**: Tất cả các nguồn dữ liệu được map vào cùng một schema
- **Chuẩn hóa**: Dữ liệu được làm sạch và chuẩn hóa theo quy tắc chung
- **Mở rộng**: Dễ dàng thêm nguồn dữ liệu mới trong tương lai
- **ML-Ready**: Schema hỗ trợ trực tiếp cho machine learning pipeline

### 📊 Thống kê

- **Tổng số cột**: 19 cột
- **Cột bắt buộc**: 5 cột (job_id, job_title, company_name, source_dataset, country)
- **Cột có dữ liệu**: 14 cột (73.7%)
- **Cột trống hoàn toàn**: 5 cột (26.3%)

---

## 📑 Chi tiết Master Schema (19 cột)

### 1. Metadata & Identification Columns

#### `job_id`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Unique identifier cho mỗi job sau khi merge và deduplicate
- **Format**: `job_XXXXXX` (6 chữ số zero-padded)
- **Ví dụ**: `job_000000`, `job_000001`, `job_003984`
- **Bắt buộc**: ✅ Yes
- **Hiện trạng**: ✅ **100% có dữ liệu** (auto-generated)

#### `source_dataset`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Nguồn gốc của dữ liệu job
- **Giá trị hợp lệ**: 
  - `kaggle_itviec` - Dữ liệu từ Kaggle (ITViec)
  - `github_it_job_posting` - Dữ liệu từ GitHub (multi-source)
- **Ví dụ**: `kaggle_itviec`, `github_it_job_posting`
- **Bắt buộc**: ✅ Yes
- **Hiện trạng**: ✅ **100% có dữ liệu**

#### `job_site`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Nền tảng đăng tin tuyển dụng gốc
- **Giá trị hợp lệ**: `itviec`, `LinkedIn`, `ITViec`, `TopCV`
- **Ví dụ**: `itviec`, `LinkedIn`, `TopCV`
- **Bắt buộc**: ✅ Yes
- **Hiện trạng**: ✅ **100% có dữ liệu**
- **Ghi chú**: 
  - Kaggle jobs → luôn là `itviec`
  - GitHub jobs → giữ nguyên từ cột `site`

---

### 2. Core Job Information Columns

#### `job_title`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Tên vị trí tuyển dụng
- **Ví dụ**: `Senior Backend Engineer`, `Frontend Developer (React)`, `QA Engineer`
- **Bắt buộc**: ✅ Yes (critical field)
- **Hiện trạng**: ✅ **100% có dữ liệu**
- **Ghi chú**: Được dùng để deduplicate và extract job_level

#### `company_name`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Tên công ty tuyển dụng
- **Ví dụ**: `Vinova`, `FPT Software`, `ĐÚNG NGƯỜI ĐÚNG VIỆC Community`
- **Bắt buộc**: ✅ Yes (critical field)
- **Hiện trạng**: ✅ **100% có dữ liệu** (1,901 unique companies)
- **Ghi chú**: 
  - Kaggle: Join từ companies.csv qua company_id
  - GitHub: Lấy trực tiếp từ cột company

#### `job_description`
- **Kiểu dữ liệu**: `text` (long string)
- **Ý nghĩa**: Mô tả chi tiết về công việc, yêu cầu, trách nhiệm
- **Ví dụ**: `We are looking for a talented Backend Engineer...`
- **Bắt buộc**: No (but highly recommended)
- **Hiện trạng**: ✅ **~100% có dữ liệu**
- **Ghi chú**: Được dùng làm text feature cho ML (TF-IDF)

---

### 3. Location Columns

#### `location_raw`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Địa điểm gốc chưa được chuẩn hóa (từ source)
- **Ví dụ**: `Hồ Chí Minh`, `Ha Noi, Vietnam`, `Đà Nẵng, Việt Nam`
- **Bắt buộc**: No
- **Hiện trạng**: ✅ **~100% có dữ liệu**
- **Ghi chú**: Được dùng để extract ra city và province

#### `city`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Thành phố đã được chuẩn hóa
- **Giá trị hợp lệ**: 
  - `Ha Noi` - Hà Nội
  - `Ho Chi Minh` - TP. Hồ Chí Minh
  - `Da Nang` - Đà Nẵng
  - `Hai Phong` - Hải Phòng
  - `Can Tho` - Cần Thơ
  - `Binh Duong` - Bình Dương
  - `Dong Nai` - Đồng Nai
  - `Remote` - Làm việc từ xa
  - `Other` - Thành phố khác
  - `Unknown` - Không xác định
- **Ví dụ**: `Ha Noi`, `Ho Chi Minh`, `Da Nang`
- **Bắt buộc**: No
- **Hiện trạng**: ✅ **100% có dữ liệu** (9 unique cities)
- **Ghi chú**: Được normalize từ location_raw, dùng cho ML feature
- **Chi tiết**: Xem thêm mục [City Normalization Strategy](#city-normalization-strategy) bên dưới

#### `province`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Tỉnh/Thành phố (hiện tại giống city)
- **Ví dụ**: `Ha Noi`, `Ho Chi Minh`
- **Bắt buộc**: No
- **Hiện trạng**: ✅ **100% có dữ liệu** (giống city)
- **Ghi chú**: Reserved cho phân biệt city vs province trong tương lai

#### `country`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Quốc gia (luôn là Vietnam cho dataset hiện tại)
- **Giá trị**: `Vietnam`
- **Ví dụ**: `Vietnam`
- **Bắt buộc**: ✅ Yes
- **Hiện trạng**: ✅ **100% có dữ liệu** (constant value)
- **Ghi chú**: Schema sẵn sàng cho mở rộng quốc tế

---

### 4. Salary Columns

#### `salary_min`
- **Kiểu dữ liệu**: `float` (nullable)
- **Ý nghĩa**: Mức lương tối thiểu (VND/tháng)
- **Đơn vị**: VND (Vietnam Dong)
- **Ví dụ**: `10000000.0` (10 triệu VND/tháng), `15000000.0`
- **Bắt buộc**: No
- **Hiện trạng**: ❌ **0% có dữ liệu** (100% NULL)
- **Lý do**: Source datasets không chứa thông tin lương
- **Status**: ⚠️ **Schema sẵn sàng, chờ data source có salary**

#### `salary_max`
- **Kiểu dữ liệu**: `float` (nullable)
- **Ý nghĩa**: Mức lương tối đa (VND/tháng)
- **Đơn vị**: VND (Vietnam Dong)
- **Ví dụ**: `20000000.0` (20 triệu VND/tháng), `30000000.0`
- **Bắt buộc**: No
- **Hiện trạng**: ❌ **0% có dữ liệu** (100% NULL)
- **Lý do**: Source datasets không chứa thông tin lương
- **Status**: ⚠️ **Schema sẵn sàng, chờ data source có salary**

#### `salary_avg`
- **Kiểu dữ liệu**: `float` (nullable)
- **Ý nghĩa**: Mức lương trung bình = (salary_min + salary_max) / 2
- **Đơn vị**: VND (Vietnam Dong)
- **Ví dụ**: `15000000.0` (15 triệu VND/tháng)
- **Bắt buộc**: No
- **Hiện trạng**: ❌ **0% có dữ liệu** (100% NULL)
- **Lý do**: Computed từ salary_min và salary_max (cả 2 đều NULL)
- **Status**: ⚠️ **Schema sẵn sàng, chờ data source có salary**

#### `salary_currency`
- **Kiểu dữ liệu**: `string` (nullable)
- **Ý nghĩa**: Đơn vị tiền tệ của lương
- **Giá trị hợp lệ**: `VND`, `USD`
- **Ví dụ**: `VND`, `USD`
- **Bắt buộc**: No (required nếu có salary)
- **Hiện trạng**: ❌ **0% có dữ liệu** (100% NULL)
- **Lý do**: Source datasets không chứa thông tin lương
- **Status**: ⚠️ **Schema sẵn sàng, chờ data source có salary**
- **Ghi chú**: Nếu có USD, sẽ convert sang VND (rate = 24,000)

---

### 5. Job Classification Columns

#### `job_level`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Cấp bậc/Seniority của công việc (extracted từ job_title)
- **Giá trị hợp lệ**:
  - `intern` - Thực tập sinh/Fresher/Graduate
  - `junior` - Junior Developer
  - `mid` - Mid-level (default nếu không có keyword)
  - `senior` - Senior/Lead/Principal/Staff
  - `manager` - Manager/Head/Director/Chief/VP/CTO/CEO
- **Ví dụ**: `senior`, `mid`, `junior`
- **Bắt buộc**: No
- **Hiện trạng**: ✅ **100% có dữ liệu**
- **Distribution**: 
  - mid: 65.7%
  - senior: 23.3%
  - junior: 5.0%
  - manager: 3.3%
  - intern: 2.8%
- **Ghi chú**: Extracted bằng keyword matching từ job_title

#### `job_category`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Phân loại công việc theo chuyên môn (extracted từ job_title)
- **Giá trị hợp lệ** (13 categories):
  - `Backend Developer`
  - `Frontend Developer`
  - `Fullstack Developer`
  - `Mobile Developer`
  - `DevOps Engineer`
  - `Data Engineer`
  - `Data Scientist`
  - `QA/Tester`
  - `Security Engineer`
  - `Software Engineer`
  - `Product Manager`
  - `Business Analyst`
  - `Other` - Không thuộc các category trên
- **Ví dụ**: `Backend Developer`, `Frontend Developer`, `QA/Tester`
- **Bắt buộc**: No
- **Hiện trạng**: ✅ **100% có dữ liệu**
- **Distribution** (Top 5):
  - Other: 40.5%
  - Backend Developer: 9.4%
  - Fullstack Developer: 8.7%
  - QA/Tester: 8.5%
  - Mobile Developer: 7.6%
- **ML Ready**: 10 categories có ≥50 samples (96.8% data)
- **Ghi chú**: Classified bằng keyword matching từ job_title

#### `employment_type`
- **Kiểu dữ liệu**: `string`
- **Ý nghĩa**: Loại hình công việc
- **Giá trị hợp lệ**: `full_time`, `part_time`, `contract`, `remote`
- **Ví dụ**: `full_time`
- **Bắt buộc**: No
- **Hiện trạng**: ✅ **100% có dữ liệu** (default = `full_time`)
- **Ghi chú**: Hiện tại mặc định full_time vì source không có field này

---

### 6. Skills & Technical Columns

#### `skills`
- **Kiểu dữ liệu**: `string` (pipe-separated)
- **Ý nghĩa**: Danh sách kỹ năng yêu cầu (normalized)
- **Format**: `skill1|skill2|skill3` (lowercase, pipe-separated)
- **Ví dụ**: 
  - `python|sql|docker`
  - `javascript|react|node.js`
  - `java|spring|mysql`
- **Bắt buộc**: No
- **Hiện trạng**: ✅ **100% có dữ liệu**
- **Source mapping**:
  - Kaggle: taglist → skills
  - GitHub: main_programming_languages → skills
- **Ghi chú**: 
  - Normalized: lowercase, remove brackets/quotes, pipe-separated
  - Được dùng làm text feature cho ML (TF-IDF)

---

### 7. Additional Columns

#### `url`
- **Kiểu dữ liệu**: `string` (URL)
- **Ý nghĩa**: Link đến job posting gốc
- **Ví dụ**: `https://itviec.com/job/12345`, `https://www.linkedin.com/jobs/view/...`
- **Bắt buộc**: No
- **Hiện trạng**: ⚠️ **64.6% có dữ liệu** (35.4% NULL)
- **Distribution**:
  - GitHub jobs: 100% có URL (từ job_url)
  - Kaggle jobs: 0% có URL (không có trong source)
- **Ghi chú**: Chỉ có từ GitHub source

#### `posted_date`
- **Kiểu dữ liệu**: `date` (YYYY-MM-DD)
- **Ý nghĩa**: Ngày đăng tin tuyển dụng
- **Format**: ISO 8601 date format
- **Ví dụ**: `2025-11-01`, `2025-10-15`
- **Bắt buộc**: No
- **Hiện trạng**: ❌ **0% có dữ liệu** (không có trong source)
- **Status**: ⚠️ **Schema sẵn sàng, chờ data source có posted_date**
- **Ghi chú**: Column reserved cho future data sources

---

## 📊 Bảng tổng hợp Master Schema

| # | Column Name | Data Type | Required | Data Availability | Source | ML Feature |
|---|-------------|-----------|----------|-------------------|--------|------------|
| 1 | `job_id` | string | ✅ | 100% ✅ | Generated | No |
| 2 | `source_dataset` | string | ✅ | 100% ✅ | Metadata | No |
| 3 | `job_site` | string | ✅ | 100% ✅ | Source | No |
| 4 | `job_title` | string | ✅ | 100% ✅ | Source | ✅ Yes (TF-IDF) |
| 5 | `company_name` | string | ✅ | 100% ✅ | Source/Join | No |
| 6 | `location_raw` | string | No | 100% ✅ | Source | No |
| 7 | `city` | string | No | 100% ✅ | Normalized | ✅ Yes (Encoded) |
| 8 | `province` | string | No | 100% ✅ | Normalized | No |
| 9 | `country` | string | ✅ | 100% ✅ | Constant | No |
| 10 | `salary_min` | float | No | 0% ❌ | N/A | No |
| 11 | `salary_max` | float | No | 0% ❌ | N/A | No |
| 12 | `salary_avg` | float | No | 0% ❌ | Computed | ✅ Planned |
| 13 | `salary_currency` | string | No | 0% ❌ | N/A | No |
| 14 | `job_level` | string | No | 100% ✅ | Extracted | ✅ Yes (Encoded) |
| 15 | `job_category` | string | No | 100% ✅ | Classified | ✅ Yes (Target) |
| 16 | `employment_type` | string | No | 100% ✅ | Default | No |
| 17 | `skills` | string | No | 100% ✅ | Normalized | ✅ Yes (TF-IDF) |
| 18 | `job_description` | text | No | ~100% ✅ | Source | ✅ Yes (TF-IDF) |
| 19 | `url` | string | No | 64.6% ⚠️ | Source | No |
| 20 | `posted_date` | date | No | 0% ❌ | N/A | ✅ Planned |

---

## 🔍 Hiện trạng dữ liệu chi tiết

### ✅ Cột có dữ liệu đầy đủ (14/19 = 73.7%)

1. **job_id** - 100% (auto-generated)
2. **source_dataset** - 100% (metadata)
3. **job_site** - 100% (metadata)
4. **job_title** - 100% (critical field)
5. **company_name** - 100% (critical field)
6. **location_raw** - 100% (from source)
7. **city** - 100% (normalized from location_raw)
8. **province** - 100% (same as city)
9. **country** - 100% (constant: Vietnam)
10. **job_level** - 100% (extracted from job_title)
11. **job_category** - 100% (classified from job_title)
12. **employment_type** - 100% (default: full_time)
13. **skills** - 100% (normalized from source)
14. **job_description** - ~100% (from source)

### ⚠️ Cột có dữ liệu một phần (1/19 = 5.3%)

15. **url** - 64.6% (chỉ có từ GitHub source, Kaggle không có)

### ❌ Cột trống hoàn toàn (5/19 = 26.3%)

16. **salary_min** - 0% (source không có)
17. **salary_max** - 0% (source không có)
18. **salary_avg** - 0% (computed từ min/max)
19. **salary_currency** - 0% (source không có)
20. **posted_date** - 0% (source không có)

---

## 📝 Ghi chú quan trọng

### 🎯 Schema Design Philosophy

1. **Forward Compatible**: Schema được thiết kế để sẵn sàng cho dữ liệu tương lai
   - Các cột salary, posted_date đã có sẵn structure
   - Không cần thay đổi schema khi có data source mới

2. **Normalization First**: Ưu tiên chuẩn hóa dữ liệu
   - city: 9 giá trị chuẩn thay vì hàng ngàn variations
   - job_level: 5 cấp độ rõ ràng
   - job_category: 13 categories có ý nghĩa
   - skills: lowercase, pipe-separated format

3. **ML-Ready**: Schema hỗ trợ trực tiếp ML pipeline
   - Text fields: job_title, job_description, skills → TF-IDF
   - Categorical fields: city, job_level → LabelEncoder
   - Target: job_category → classification target

4. **Source of Truth**: Đây là tài liệu chính thức
   - Mọi thay đổi schema phải update file này
   - Mọi mapping mới phải tuân theo schema này
   - Không xóa cột "ít dùng", chỉ đánh dấu status

### ⚠️ Lưu ý khi thêm data source mới

1. **Bắt buộc map các cột critical**:
   - job_title
   - company_name
   - source_dataset
   - job_site
   - country

2. **Nên có nhưng không bắt buộc**:
   - location_raw (để extract city)
   - job_description (quan trọng cho ML)
   - skills (quan trọng cho ML)

3. **Có thì tốt**:
   - salary_min, salary_max
   - url
   - posted_date

4. **Auto-computed fields**:
   - city (from location_raw)
   - province (from city)
   - job_level (from job_title)
   - job_category (from job_title)
   - salary_avg (from min/max)

### 🔄 Quy trình cập nhật schema

1. **Thêm cột mới**:
   - Update file này trước
   - Update mapping functions
   - Update normalization functions
   - Update README.md
   - Update VERIFICATION_CHECKLIST.md

2. **Thay đổi kiểu dữ liệu**:
   - Phải có migration plan
   - Test với data hiện tại
   - Document breaking changes

3. **Xóa cột** (tránh nếu có thể):
   - Phải có lý do rõ ràng
   - Deprecate trước khi xóa
   - Update toàn bộ pipeline

---

## 🗺️ City Normalization Strategy

### 📍 Overview

Thay vì hard-code city trong hàm `normalize_city()`, chúng ta sử dụng **bảng tham chiếu city/province chuẩn** để dễ dàng mở rộng và maintain. Bảng này map các pattern location đa dạng về một tập giá trị chuẩn.

### 🎯 Quy trình Normalization

Pipeline thực hiện 3 bước sau:

1. **Pre-processing**: Chuẩn hóa `location_raw`
   - Chuyển về lowercase: `Hà Nội` → `hà nội`
   - Bỏ dấu (unidecode): `hà nội` → `ha noi`
   - Loại bỏ ký tự đặc biệt: dấu phẩy, dấu chấm, số nhà
   - Trim whitespace: `  ha noi  ` → `ha noi`

2. **Pattern Matching**: So khớp với bảng tham chiếu
   - Tìm pattern match (substring hoặc exact match)
   - Priority: Exact match > Substring match
   - First match wins

3. **Fallback Logic**: Nếu không match
   - Chứa "remote" → `Remote`
   - Không match → `Other`
   - NULL/empty → `Unknown`

### 📋 Bảng Tham Chiếu City/Province

| Pattern (Normalized) | City Standard | Province Standard | Notes |
|---------------------|---------------|-------------------|-------|
| **Hà Nội** | | | |
| `ha noi` | `Ha Noi` | `Ha Noi` | Exact match |
| `hanoi` | `Ha Noi` | `Ha Noi` | Variant |
| `hoang mai` | `Ha Noi` | `Ha Noi` | District in Hanoi |
| `dong da` | `Ha Noi` | `Ha Noi` | District in Hanoi |
| `cau giay` | `Ha Noi` | `Ha Noi` | District in Hanoi |
| `ba dinh` | `Ha Noi` | `Ha Noi` | District in Hanoi |
| `hoan kiem` | `Ha Noi` | `Ha Noi` | District in Hanoi |
| `thanh xuan` | `Ha Noi` | `Ha Noi` | District in Hanoi |
| `hai ba trung` | `Ha Noi` | `Ha Noi` | District in Hanoi |
| `nam tu liem` | `Ha Noi` | `Ha Noi` | District in Hanoi |
| `tay ho` | `Ha Noi` | `Ha Noi` | District in Hanoi |
| `long bien` | `Ha Noi` | `Ha Noi` | District in Hanoi |
| **TP. Hồ Chí Minh** | | | |
| `ho chi minh` | `Ho Chi Minh` | `Ho Chi Minh` | Exact match |
| `hcm` | `Ho Chi Minh` | `Ho Chi Minh` | Abbreviation |
| `saigon` | `Ho Chi Minh` | `Ho Chi Minh` | Old name |
| `sai gon` | `Ho Chi Minh` | `Ho Chi Minh` | Old name variant |
| `tp hcm` | `Ho Chi Minh` | `Ho Chi Minh` | Abbreviation |
| `tphcm` | `Ho Chi Minh` | `Ho Chi Minh` | Abbreviation |
| `quan 1` | `Ho Chi Minh` | `Ho Chi Minh` | District 1 |
| `district 1` | `Ho Chi Minh` | `Ho Chi Minh` | District 1 |
| `quan 2` | `Ho Chi Minh` | `Ho Chi Minh` | District 2 |
| `district 2` | `Ho Chi Minh` | `Ho Chi Minh` | District 2 |
| `quan 3` | `Ho Chi Minh` | `Ho Chi Minh` | District 3 |
| `district 3` | `Ho Chi Minh` | `Ho Chi Minh` | District 3 |
| `quan 4` | `Ho Chi Minh` | `Ho Chi Minh` | District 4 |
| `quan 5` | `Ho Chi Minh` | `Ho Chi Minh` | District 5 |
| `quan 7` | `Ho Chi Minh` | `Ho Chi Minh` | District 7 |
| `quan 10` | `Ho Chi Minh` | `Ho Chi Minh` | District 10 |
| `quan 12` | `Ho Chi Minh` | `Ho Chi Minh` | District 12 |
| `tan binh` | `Ho Chi Minh` | `Ho Chi Minh` | District |
| `binh thanh` | `Ho Chi Minh` | `Ho Chi Minh` | District |
| `phu nhuan` | `Ho Chi Minh` | `Ho Chi Minh` | District |
| `go vap` | `Ho Chi Minh` | `Ho Chi Minh` | District |
| `thu duc` | `Ho Chi Minh` | `Ho Chi Minh` | Thu Duc City |
| `thu duc city` | `Ho Chi Minh` | `Ho Chi Minh` | Thu Duc City |
| **Đà Nẵng** | | | |
| `da nang` | `Da Nang` | `Da Nang` | Exact match |
| `danang` | `Da Nang` | `Da Nang` | Variant |
| `hai chau` | `Da Nang` | `Da Nang` | District in Da Nang |
| `son tra` | `Da Nang` | `Da Nang` | District in Da Nang |
| `ngu hanh son` | `Da Nang` | `Da Nang` | District in Da Nang |
| **Hải Phòng** | | | |
| `hai phong` | `Hai Phong` | `Hai Phong` | Exact match |
| `haiphong` | `Hai Phong` | `Hai Phong` | Variant |
| `hong bang` | `Hai Phong` | `Hai Phong` | District |
| `le chan` | `Hai Phong` | `Hai Phong` | District |
| **Cần Thơ** | | | |
| `can tho` | `Can Tho` | `Can Tho` | Exact match |
| `cantho` | `Can Tho` | `Can Tho` | Variant |
| `ninh kieu` | `Can Tho` | `Can Tho` | District |
| **Bình Dương** | | | |
| `binh duong` | `Binh Duong` | `Binh Duong` | Exact match |
| `binhduong` | `Binh Duong` | `Binh Duong` | Variant |
| `thu dau mot` | `Binh Duong` | `Binh Duong` | City in province |
| `di an` | `Binh Duong` | `Binh Duong` | City in province |
| **Đồng Nai** | | | |
| `dong nai` | `Dong Nai` | `Dong Nai` | Exact match |
| `dongnai` | `Dong Nai` | `Dong Nai` | Variant |
| `bien hoa` | `Dong Nai` | `Dong Nai` | City in province |
| **Remote Work** | | | |
| `remote` | `Remote` | `Remote` | Remote work |
| `work from home` | `Remote` | `Remote` | Remote work |
| `wfh` | `Remote` | `Remote` | Remote work abbreviation |
| `online` | `Remote` | `Remote` | Online work |
| **Special Cases** | | | |
| `null` | `Unknown` | `Unknown` | NULL value |
| `empty` | `Unknown` | `Unknown` | Empty string |
| `(no match)` | `Other` | `Other` | Fallback |

### 📊 Coverage Statistics

Dựa trên phân tích raw data (Kaggle + GitHub):

- **Ha Noi**: ~35.9% jobs (1,431 / 3,985)
  - Patterns: `ha noi`, `hanoi`, `cau giay`, `dong da`, `ba dinh`, `thanh xuan`
  
- **Ho Chi Minh**: ~51.7% jobs (2,060 / 3,985)
  - Patterns: `ho chi minh`, `hcm`, `saigon`, `quan 1`, `district 1-12`, `tan binh`, `binh thanh`, `thu duc`
  
- **Da Nang**: ~2.9% jobs (115 / 3,985)
  - Patterns: `da nang`, `hai chau`
  
- **Other Cities**: ~9.1% jobs (364 / 3,985)
  - Hai Phong: 3 jobs
  - Can Tho: 3 jobs
  - Binh Duong: Minimal
  - Dong Nai: Minimal
  
- **Remote**: ~0.2% jobs (6 / 3,985)
  - Patterns: `remote`, `work from home`

- **Unknown**: ~0.2% jobs (6 / 3,985)

### 🔧 Implementation Notes

**Current Implementation** (Hard-coded):
```python
def normalize_city(location_raw):
    if pd.isna(location_raw) or location_raw == '':
        return 'Unknown'
    
    location_lower = location_raw.lower()
    
    # Hard-coded patterns
    if 'hà nội' in location_lower or 'ha noi' in location_lower or 'hanoi' in location_lower:
        return 'Ha Noi'
    elif 'hồ chí minh' in location_lower or 'hcm' in location_lower or 'saigon' in location_lower:
        return 'Ho Chi Minh'
    # ... more if-else
```

**Proposed Implementation** (Table-driven):
```python
# Load city reference table
city_ref_table = pd.read_csv('data/reference/city_province_mapping.csv')

def normalize_city(location_raw, ref_table=city_ref_table):
    if pd.isna(location_raw) or location_raw == '':
        return 'Unknown'
    
    # Pre-process
    location_normalized = unidecode(location_raw.lower().strip())
    
    # Pattern matching
    for _, row in ref_table.iterrows():
        if row['pattern'] in location_normalized:
            return row['city_standard']
    
    # Fallback
    if 'remote' in location_normalized:
        return 'Remote'
    return 'Other'
```

### 📝 Extensibility

Để thêm city/province mới:

1. **Thêm vào bảng tham chiếu**:
   ```csv
   pattern,city_standard,province_standard,notes
   nha trang,Nha Trang,Khanh Hoa,Coastal city
   cam ranh,Nha Trang,Khanh Hoa,City in Khanh Hoa
   ```

2. **Không cần thay đổi code**: Function `normalize_city()` tự động pickup pattern mới

3. **Re-run normalization**: Apply lại trên raw data

### ⚠️ Known Issues & Limitations

1. **Ambiguous Patterns**:
   - `"Binh Thanh"` có thể là district của HCM hoặc tỉnh khác
   - Solution: Exact match có priority cao hơn substring

2. **International Locations**:
   - `"Singapore"` hiện tại sẽ map về `Other`
   - Future: Thêm country detection trước khi normalize city

3. **Complex Addresses**:
   - `"521 Kim Mã, Ba Dinh, Ha Noi"` → cần extract `Ba Dinh` → map về `Ha Noi`
   - Current implementation: Match `Ha Noi` ở cuối string

4. **Province vs City**:
   - Hiện tại `province` = `city` (duplicate)
   - Future: Separate logic cho province-level grouping

---

## 💰 Salary Fields - Current Status

### ⚠️ IMPORTANT NOTICE

**Các trường salary trong master schema hiện đang hoàn toàn trống (100% NULL)**. Đây không phải bug hay thiếu sót trong pipeline, mà là do **2 nguồn dữ liệu hiện tại (Kaggle và GitHub) không cung cấp thông tin lương**.

### 📊 Salary Columns Overview

| Column | Type | Description | Current Status |
|--------|------|-------------|----------------|
| `salary_min` | float | Mức lương tối thiểu (VND/tháng) | ❌ **0% data** (all NULL) |
| `salary_max` | float | Mức lương tối đa (VND/tháng) | ❌ **0% data** (all NULL) |
| `salary_avg` | float | Mức lương trung bình | ❌ **0% data** (all NULL) |
| `salary_currency` | string | Đơn vị tiền tệ (VND, USD) | ❌ **0% data** (all NULL) |
| `salary_period` | string | Chu kỳ trả lương (monthly, yearly) | ❌ **Not implemented yet** |

### 🔍 Why No Salary Data?

1. **Kaggle Source** (`kaggle_itviec`):
   - Files: `jobs.csv` + `companies.csv`
   - Salary columns: **Không có cột salary nào**
   - Checked: 1,412 jobs → 0 salary info

2. **GitHub Source** (`github_it_job_posting`):
   - File: `job_descriptions.csv`
   - Salary columns: **Không có cột salary nào**
   - Checked: 3,101 jobs → 0 salary info

3. **Master Table** (`jobs_master.csv`):
   - Result: 3,985 jobs → **0% có salary** (100% NULL)

### 🚫 What This Means

**❌ Không thể thực hiện**:
- Phân tích salary distribution
- Salary range by job category/level
- Salary comparison by city
- Salary prediction models
- Salary-based job recommendations

**✅ Pipeline vẫn hoạt động**:
- Schema đã chuẩn bị sẵn các cột salary
- Normalization functions đã implement logic xử lý salary
- Merge logic handle NULL salary correctly
- ML pipeline không phụ thuộc vào salary (dùng text + categorical features)

### 🔮 Future Salary Logic (When Data Available)

Khi có `salary_raw` từ source mới (ví dụ: VietnamWorks, TopCV), pipeline sẽ:

**1. Parse Salary String**:
```python
def parse_salary(salary_raw):
    """
    Examples:
    - "10-20 triệu" → (10M, 20M, 15M, 'VND')
    - "$1000-2000" → (24M, 48M, 36M, 'VND')  # Converted
    - "Negotiate" → (None, None, None, None)
    """
    if pd.isna(salary_raw) or 'negotiate' in salary_raw.lower():
        return None, None, None, None
    
    # Extract numbers
    numbers = re.findall(r'\d+(?:\.\d+)?', salary_raw)
    
    # Detect currency
    if '$' in salary_raw or 'usd' in salary_raw.lower():
        currency = 'USD'
        conversion_rate = 24000  # USD to VND
    else:
        currency = 'VND'
        conversion_rate = 1
    
    # Handle "triệu" (millions)
    if 'triệu' in salary_raw or 'tr' in salary_raw:
        multiplier = 1000000
    else:
        multiplier = 1
    
    # Calculate min/max/avg
    if len(numbers) >= 2:
        salary_min = float(numbers[0]) * multiplier * conversion_rate
        salary_max = float(numbers[1]) * multiplier * conversion_rate
    elif len(numbers) == 1:
        salary_min = salary_max = float(numbers[0]) * multiplier * conversion_rate
    else:
        return None, None, None, None
    
    salary_avg = (salary_min + salary_max) / 2
    
    return salary_min, salary_max, salary_avg, 'VND'  # Always VND after conversion
```

**2. Apply in Normalization**:
```python
def apply_normalization(df):
    # ... other normalizations
    
    if 'salary_raw' in df.columns:
        # Parse salary
        salary_parsed = df['salary_raw'].apply(parse_salary)
        df['salary_min'] = salary_parsed.apply(lambda x: x[0])
        df['salary_max'] = salary_parsed.apply(lambda x: x[1])
        df['salary_avg'] = salary_parsed.apply(lambda x: x[2])
        df['salary_currency'] = salary_parsed.apply(lambda x: x[3])
    else:
        # Initialize as NULL (current behavior)
        df['salary_min'] = None
        df['salary_max'] = None
        df['salary_avg'] = None
        df['salary_currency'] = None
    
    return df
```

**3. Use in ML** (Optional):
```python
# Feature engineering
df_ml['has_salary'] = df_ml['salary_avg'].notna().astype(int)
df_ml['salary_log'] = np.log1p(df_ml['salary_avg'].fillna(0))

# Add to feature matrix
X_salary = df_ml[['has_salary', 'salary_log']].values
X_combined = np.hstack([X_tfidf, X_categorical, X_salary])
```

### 📋 Example Future Sources with Salary

| Source | Salary Column | Format Example |
|--------|--------------|----------------|
| **VietnamWorks** | `salary_range` | `"10-20 triệu"`, `"Thỏa thuận"` |
| **TopCV** | `salary` | `"15000000 VND"`, `"Negotiate"` |
| **LinkedIn** | `salary_from`, `salary_to` | `10000000`, `20000000` (numeric) |
| **CareerBuilder** | `salary_text` | `"$1000-2000/month"` |

### ⚙️ Schema Readiness Checklist

- ✅ Salary columns defined in master schema
- ✅ `parse_salary()` function implemented
- ✅ Normalization logic handles NULL salary
- ✅ Merge logic doesn't break with NULL salary
- ✅ ML pipeline works without salary features
- ✅ Documentation clear about 0% salary data
- ⏳ Waiting for data sources with salary information

### 🔗 Related Documentation

- **Current Data Sources**: See `data/raw/kaggle/` and `data/raw/github/`
- **Column Mapping**: See `docs/column_mapping.md` (salary mapping = NULL)
- **Pipeline**: See `docs/pipeline_overview.md` (Block C: Normalization)
- **Verification**: See `VERIFICATION_CHECKLIST.md` (confirms 0% salary)

---

## 📚 Tài liệu liên quan

- **Column Mapping**: Xem `docs/column_mapping.md` để biết chi tiết mapping từ source
- **Pipeline Overview**: Xem `docs/pipeline_overview.md` để hiểu data flow
- **README**: Xem root README.md để biết overview về project
- **Notebook**: Xem `vietnam_it_jobs_merge_analysis.ipynb` để thấy implementation

---

**Last Updated**: November 14, 2025  
**Version**: 1.0.0  
**Status**: ✅ Production-ready (14/19 columns có data, 5 columns ready cho future)
