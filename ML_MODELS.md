# 🤖 Chi Tiết Mô Hình Machine Learning

## Tổng Quan

Nghiên cứu triển khai **6 bài toán Machine Learning** với các mô hình khác nhau, bao gồm:
- 3 mô hình hồi quy (Salary Prediction)
- 1 mô hình phân loại (Position Classification)
- 1 mô hình phân cụm (Job Clustering)
- 1 mô hình phân loại kinh nghiệm (Experience Prediction)

---

## 📊 BẢNG TỔNG HỢP CÁC MÔ HÌNH

| # | Bài toán | Mô hình | Biến đầu vào (X) | Biến đầu ra (Y) | Metric chính |
|---|----------|---------|------------------|-----------------|--------------|
| 1 | Dự đoán lương | Ridge Regression | region, position, job_type, exp_years, skill_count | salary_median | R²=0.132 |
| 2 | Dự đoán lương | Random Forest | region, position, job_type, exp_years, skill_count | salary_median | R²=0.228 |
| 3 | Dự đoán lương | Gradient Boosting | region, position, job_type, exp_years, skill_count | salary_median | R²=0.158 |
| 4 | Phân loại vị trí | Logistic Regression | region, job_type, exp_years | position_simple | F1=0.359 |
| 5 | Phân cụm việc làm | K-Means | salary_median, exp_years | cluster (4 nhóm) | Silhouette=0.436 |
| 6 | Dự đoán kinh nghiệm | Random Forest Classifier | skill_count, region, position | exp_label | Accuracy=0.58 |

---

## 🎯 BÀI TOÁN 1-3: DỰ ĐOÁN MỨC LƯƠNG (REGRESSION)

### Biến Đầu Ra (Target Variable)

| Tên biến | Kiểu dữ liệu | Mô tả | Đơn vị |
|----------|-------------|-------|--------|
| `salary_median` | Continuous (float) | Mức lương trung vị = (salary_min + salary_max) / 2 | Triệu VND/tháng |

**Thống kê biến đầu ra:**
- Min: 1 triệu VND
- Max: ~500 triệu VND  
- Median: 13.5 triệu VND
- Mean: 15.5 triệu VND
- Phân bố: Right-skewed

### Biến Đầu Vào (Features)

| Tên biến | Kiểu | Mô tả | Số giá trị unique |
|----------|------|-------|-------------------|
| `region` | Categorical | Vùng miền (Bắc/Trung/Nam/Toàn quốc) | 4 |
| `position_simple` | Categorical | Cấp bậc đã chuẩn hóa | 6 |
| `job_type` | Categorical | Loại hình công việc | 4 |
| `exp_years` | Numeric | Số năm kinh nghiệm yêu cầu | 0-15+ |
| `skill_count` | Numeric | Số lượng kỹ năng yêu cầu | 0-20+ |
| `requires_english` | Binary | Có yêu cầu tiếng Anh (0/1) | 2 |
| `has_tech_skills` | Binary | Có yêu cầu kỹ năng IT (0/1) | 2 |

### Preprocessing Pipeline

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

cat_features = ['region', 'position_simple', 'job_type']
num_features = ['exp_years', 'skill_count']
bool_features = ['requires_english', 'has_tech_skills']

preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features),
    ('num', StandardScaler(), num_features),
    ('bool', 'passthrough', bool_features)
])
```

**Kỹ thuật xử lý:**
- **Categorical:** One-Hot Encoding (tạo dummy variables)
- **Numeric:** Z-score Standardization (mean=0, std=1)
- **Binary:** Passthrough (giữ nguyên)

### Train/Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

| Tập dữ liệu | Số mẫu | Tỷ lệ |
|-------------|--------|-------|
| Training | 63,737 | 80% |
| Test | 15,935 | 20% |
| **Tổng** | **79,672** | 100% |

---

### MODEL 1: RIDGE REGRESSION

**Lý do chọn:**
1. ✅ **Baseline model:** Đơn giản, dễ hiểu, dễ diễn giải
2. ✅ **Regularization L2:** Giảm overfitting, xử lý multicollinearity
3. ✅ **Tính toán nhanh:** Phù hợp cho dữ liệu lớn
4. ✅ **Hệ số diễn giải được:** Cho biết tác động của từng feature

**Hyperparameters:**
```python
param_grid = {'model__alpha': [0.1, 1.0, 10.0, 50.0, 100.0]}
grid_ridge = GridSearchCV(ridge_pipe, param_grid=param_grid, cv=5, scoring='r2')
```

**Kết quả:**
| Metric | Giá trị |
|--------|---------|
| Best α | 50.0 |
| CV R² (5-fold) | 0.1349 |
| Test R² | 0.1316 |
| Test RMSE | 8.96 triệu VND |
| Test MAE | 5.16 triệu VND |

**Phân tích hệ số:**
- **Tác động dương (+):** Giám đốc, Quản lý, exp_years, IT skills
- **Tác động âm (-):** Thực tập, Toàn thời gian (so với các loại khác)

---

### MODEL 2: RANDOM FOREST REGRESSOR ⭐ (Best Model)

**Lý do chọn:**
1. ✅ **Ensemble learning:** Kết hợp nhiều Decision Trees (Bagging)
2. ✅ **Non-linear relationships:** Capture được mối quan hệ phi tuyến
3. ✅ **Feature Importance:** Cung cấp thông tin về tầm quan trọng đặc trưng
4. ✅ **Robust to outliers:** Ít bị ảnh hưởng bởi outliers
5. ✅ **Không cần feature scaling:** Tự động xử lý

**Hyperparameters:**
```python
RandomForestRegressor(
    n_estimators=300,      # Số cây
    max_depth=12,          # Độ sâu tối đa
    random_state=42,
    n_jobs=-1              # Parallel processing
)
```

**Kết quả:**
| Metric | Giá trị |
|--------|---------|
| CV R² (5-fold) | 0.1675 (±0.046) |
| Test R² | **0.2276** |
| Test RMSE | **8.45 triệu VND** |
| Test MAE | **4.91 triệu VND** |

**Feature Importance:**
| Feature | Importance |
|---------|------------|
| exp_years | 29% |
| skill_count | 15% |
| region | 10% |
| position_simple | 9% |
| job_type | 8% |
| has_tech_skills | 5% |
| requires_english | 4% |

**Tại sao Random Forest tốt nhất?**
- Cải thiện **73%** so với Ridge Regression
- Capture được non-linear relationships tốt hơn
- Kết hợp nhiều features hiệu quả

---

### MODEL 3: GRADIENT BOOSTING REGRESSOR

**Lý do chọn:**
1. ✅ **Sequential ensemble:** Học tuần tự, sửa lỗi từ model trước
2. ✅ **State-of-the-art performance:** Thường đạt top trong các cuộc thi
3. ✅ **Tối ưu hóa loss function:** Gradient descent on residuals
4. ⚠️ **Dễ overfit:** Cần tune hyperparameters cẩn thận

**Hyperparameters:**
```python
GradientBoostingRegressor(
    n_estimators=300,
    max_depth=3,           # Shallow trees to prevent overfitting
    learning_rate=0.05,    # Low learning rate
    random_state=42
)
```

**Kết quả:**
| Metric | Giá trị |
|--------|---------|
| CV R² (5-fold) | 0.1632 (±0.046) |
| Test R² | 0.1581 |
| Test RMSE | 8.83 triệu VND |
| Test MAE | 5.04 triệu VND |

**Nhận xét:**
- Hiệu suất **giữa Ridge và Random Forest**
- Có thể cải thiện với hyperparameter tuning sâu hơn
- max_depth=3 có thể quá nông (underfitting)

---

### SO SÁNH 3 MÔ HÌNH HỒI QUY

| Metric | Ridge | Random Forest | Gradient Boosting |
|--------|-------|---------------|-------------------|
| CV R² | 0.135 | 0.168 | 0.163 |
| Test R² | 0.132 | **0.228** | 0.158 |
| RMSE | 8.96M | **8.45M** | 8.83M |
| MAE | 5.16M | **4.91M** | 5.04M |
| Ranking | #3 | **#1** | #2 |

**Kết luận:** Random Forest là mô hình tốt nhất cho bài toán dự đoán lương.

---

## 🏷️ BÀI TOÁN 4: PHÂN LOẠI CẤP BẬC VỊ TRÍ (CLASSIFICATION)

### Biến Đầu Ra

| Tên biến | Kiểu | Mô tả | Số lớp |
|----------|------|-------|--------|
| `position_simple` | Categorical (Multi-class) | Cấp bậc vị trí | 4 |

**Phân bố lớp:**
| Lớp | Số lượng | Tỷ lệ |
|-----|----------|-------|
| Nhân viên | 69,234 | 87.2% |
| Quản lý | 7,344 | 9.3% |
| Trưởng nhóm | 2,766 | 3.5% |
| Chuyên viên | - | - |

⚠️ **Class Imbalance nghiêm trọng:** Nhân viên chiếm 87%!

### Biến Đầu Vào

| Tên biến | Kiểu | Lý do chọn |
|----------|------|------------|
| `region` | Categorical | Vị trí địa lý ảnh hưởng loại công việc |
| `job_type` | Categorical | Loại hình ảnh hưởng cấp bậc |
| `exp_years` | Numeric | Kinh nghiệm liên quan cấp bậc |

**Lưu ý quan trọng:** ❌ **KHÔNG sử dụng salary features** để tránh Data Leakage!
- Salary → Position: Có mối quan hệ nhân quả ngược
- Nếu dùng salary, model sẽ "cheat" bằng cách nhìn vào lương

### MODEL: LOGISTIC REGRESSION (Multi-class)

**Lý do chọn:**
1. ✅ **Interpretable:** Hệ số diễn giải được (odds ratio)
2. ✅ **Probabilistic output:** Cho xác suất từng lớp
3. ✅ **Efficient:** Tính toán nhanh
4. ✅ **Regularization:** L2 penalty để tránh overfitting
5. ✅ **Class weight:** Xử lý class imbalance

**Configuration:**
```python
LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight='balanced'  # Xử lý class imbalance
)
```

**Kết quả:**
| Metric | Giá trị |
|--------|---------|
| CV F1-macro (5-fold) | 0.357 |
| CV Accuracy (5-fold) | 0.476 |
| Test Accuracy | 0.4768 |
| Test F1-weighted | 0.5658 |
| Test F1-macro | 0.3586 |
| **ROC-AUC (OvR)** | **0.7943** |

**Classification Report:**
| Lớp | Precision | Recall | F1-score | Support |
|-----|-----------|--------|----------|---------|
| Nhân viên | 0.96 | 0.45 | 0.61 | 13,847 |
| Quản lý | 0.16 | 0.54 | 0.24 | 1,469 |
| Trưởng nhóm | 0.12 | 0.96 | 0.22 | 553 |

**Phân tích:**
- **Accuracy thấp (47.68%):** Do class imbalance
- **ROC-AUC cao (79.43%):** Model phân biệt tốt nếu điều chỉnh threshold
- Model có xu hướng dự đoán nhiều sang "Trưởng nhóm" do class_weight='balanced'

---

## 🎯 BÀI TOÁN 5: PHÂN CỤM VIỆC LÀM (CLUSTERING)

### Mục Tiêu

Khám phá các nhóm công việc tương đồng dựa trên đặc trưng lương và kinh nghiệm (Unsupervised Learning).

### Biến Đầu Vào

| Tên biến | Kiểu | Mô tả |
|----------|------|-------|
| `salary_median` | Numeric | Mức lương trung vị (triệu VND) |
| `exp_years` | Numeric | Số năm kinh nghiệm yêu cầu |

**Preprocessing:**
```python
from sklearn.preprocessing import StandardScaler

X_cluster = cluster_df[['salary_median', 'exp_years']].values
scaler_cluster = StandardScaler()
X_cluster_scaled = scaler_cluster.fit_transform(X_cluster)
```

### MODEL: K-MEANS CLUSTERING

**Lý do chọn:**
1. ✅ **Simple & Efficient:** Thuật toán đơn giản, nhanh với dữ liệu lớn
2. ✅ **Interpretable:** Dễ diễn giải kết quả (centroids)
3. ✅ **Scalable:** Phù hợp với 80K+ data points
4. ✅ **Spherical clusters:** Phù hợp với dữ liệu 2D của bài toán

**Xác định số cụm tối ưu:**
```python
k_range = range(2, 8)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_cluster_scaled)
    inertias.append(kmeans.inertia_)          # Elbow method
    silhouettes.append(silhouette_score(...)) # Silhouette method
```

**Kết quả phân tích:**
| k | Inertia | Silhouette Score |
|---|---------|------------------|
| 2 | 101,584 | 0.478 |
| 3 | 76,295 | 0.473 |
| **4** | **62,536** | **0.436** |
| 5 | 50,628 | 0.472 |
| 6 | 41,952 | 0.469 |

**Lý do chọn k=4:**
1. Điểm uốn (elbow) rõ rệt trên đường cong Inertia
2. 4 cụm cho phép diễn giải ý nghĩa kinh doanh rõ ràng hơn:
   - Entry Level, Mid-Level, Senior, Executive

**Kết quả cuối cùng:**
| Cluster | Tên gọi | Số lượng | Tỷ lệ | Lương TB | KN TB |
|---------|---------|----------|-------|----------|-------|
| 1 | Entry (Mới vào nghề) | 39,309 | 49.4% | 13.6 tr | 0.1 năm |
| 3 | Mid-level (Trung cấp) | 29,430 | 36.9% | 13.3 tr | 2.4 năm |
| 0 | Senior (Có kinh nghiệm) | 9,423 | 11.8% | 23.7 tr | 4.7 năm |
| 2 | Executive (Điều hành) | 1,510 | 1.9% | 58.2 tr | 2.6 năm |

**Silhouette Score = 0.4363** (>0.25 là acceptable)

---

## 📈 BÀI TOÁN 6: DỰ ĐOÁN YÊU CẦU KINH NGHIỆM

### Biến Đầu Ra

| Tên biến | Kiểu | Mô tả | Số lớp |
|----------|------|-------|--------|
| `exp_label` | Categorical | Yêu cầu kinh nghiệm đã nhóm | 4 |

**Phân bố lớp:**
| Lớp | Số lượng | Tỷ lệ |
|-----|----------|-------|
| Chưa có kinh nghiệm | 7,364 | 51.6% |
| 1-3 năm | 3,905 | 27.4% |
| 3-5 năm | 2,529 | 17.7% |
| Trên 5 năm | 455 | 3.2% |

### Biến Đầu Vào

| Tên biến | Kiểu | Mô tả |
|----------|------|-------|
| `skill_count` | Numeric | Số lượng kỹ năng yêu cầu |
| `region_enc` | Encoded | Vùng miền (Label Encoded) |
| `position_enc` | Encoded | Cấp bậc vị trí (Label Encoded) |

### MODEL: RANDOM FOREST CLASSIFIER

**Lý do chọn:**
1. ✅ **Xử lý class imbalance:** Tốt hơn nhiều model khác
2. ✅ **Feature importance:** Cho biết yếu tố nào quan trọng
3. ✅ **Non-linear:** Capture được mối quan hệ phức tạp

**Kết quả:**
| Metric | Giá trị |
|--------|---------|
| Test Accuracy | 0.5789 |
| F1-macro | 0.37 |
| F1-weighted | 0.54 |

**Classification Report:**
| Lớp | Precision | Recall | F1-score | Support |
|-----|-----------|--------|----------|---------|
| Chưa có KN | 0.64 | 0.87 | 0.73 | 7,364 |
| 1-3 năm | 0.43 | 0.36 | 0.39 | 3,905 |
| 3-5 năm | 0.49 | 0.17 | 0.25 | 2,529 |
| Trên 5 năm | 0.53 | 0.04 | 0.08 | 455 |

**Nhận xét:**
- "Chưa có kinh nghiệm" được dự đoán tốt nhất (recall 87%)
- "Trên 5 năm" rất khó dự đoán (recall chỉ 4%) do số mẫu ít

---

## 📏 METRICS ĐÁNH GIÁ

### Cho Bài Toán Hồi Quy

| Metric | Công thức | Ý nghĩa |
|--------|-----------|---------|
| **R²** | $1 - \frac{SS_{res}}{SS_{tot}}$ | % phương sai được giải thích (0-1) |
| **RMSE** | $\sqrt{\frac{1}{n}\sum(y_i - \hat{y}_i)^2}$ | Sai số căn bình phương trung bình |
| **MAE** | $\frac{1}{n}\sum|y_i - \hat{y}_i|$ | Sai số tuyệt đối trung bình |

### Cho Bài Toán Phân Loại

| Metric | Ý nghĩa | Khi nào dùng |
|--------|---------|--------------|
| **Accuracy** | % dự đoán đúng | Khi classes cân bằng |
| **F1-macro** | Trung bình F1 các lớp | Khi classes imbalanced |
| **F1-weighted** | F1 weighted by support | Quan tâm lớp lớn hơn |
| **ROC-AUC** | Diện tích dưới ROC | Đánh giá tổng thể |

### Cho Bài Toán Phân Cụm

| Metric | Công thức | Ý nghĩa |
|--------|-----------|---------|
| **Silhouette** | $\frac{b-a}{max(a,b)}$ | Độ gắn kết và tách biệt (-1 đến 1) |
| **Inertia** | $\sum_i min_j ||x_i - c_j||^2$ | Tổng khoảng cách trong cụm |

---

## 🔧 HYPERPARAMETER TUNING

### GridSearchCV cho Ridge

```python
param_grid = {'model__alpha': [0.1, 1.0, 10.0, 50.0, 100.0]}
grid_ridge = GridSearchCV(
    ridge_pipe, 
    param_grid=param_grid, 
    cv=5, 
    scoring='r2',
    n_jobs=-1
)
```

### Cross-Validation (5-fold)

```python
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
print(f"CV R²: {cv_scores.mean():.4f} (±{cv_scores.std()*2:.4f})")
```

**Lý do chọn k=5:**
- Cân bằng giữa bias và variance
- Đủ lớn để có statistical significance
- Không quá tốn thời gian tính toán

---

## 📋 TỔNG KẾT

### Các Phát Hiện Chính

1. **Random Forest** là model tốt nhất cho dự đoán lương (R²=22.76%)
2. **Kinh nghiệm** là feature quan trọng nhất (29% importance)
3. **Class imbalance** là thách thức lớn cho classification
4. **4 clusters** phân đoạn thị trường việc làm hiệu quả

### Hạn Chế

1. R² = 22.76% → Model chỉ giải thích được ~23% variance của lương
2. Thiếu features quan trọng: học vấn, quy mô công ty, chứng chỉ
3. Class imbalance nghiêm trọng ảnh hưởng classification

### Khuyến Nghị Cải Thiện

1. Thu thập thêm features: education, company_size, certifications
2. Áp dụng NLP để trích xuất skills từ job description
3. Thử các kỹ thuật xử lý imbalance: SMOTE, undersampling
4. Hyperparameter tuning sâu hơn cho Gradient Boosting
