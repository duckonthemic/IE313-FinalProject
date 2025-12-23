Bạn là Senior Data Analyst + Data Scientist + Data Engineer. Hãy tạo 01 Jupyter Notebook (.ipynb) end-to-end cho đề tài:

Thu thập & phân tích tin tuyển dụng Việt Nam (Snapshot) và mô hình dự đoán lương/level

========================
0) MỤC TIÊU & ĐẦU RA
========================
MỤC TIÊU
1) Thu thập dữ liệu việc làm tại Việt Nam từ các trang tuyển dụng (crawl/scrape) để tạo dataset.
2) Làm sạch – chuẩn hóa – khám phá dữ liệu (EDA) – trực quan hóa dữ liệu.
3) Trả lời các câu hỏi về xu hướng: ngành nghề/kỹ năng nổi bật, khu vực nóng, mức lương, seniority, remote/hybrid, biến động theo thời gian.
4) Xây dựng tối thiểu 04 mô hình ML phù hợp với dữ liệu/bài toán; đánh giá, so sánh, chọn mô hình tốt nhất.
5) Rút ra insight + khuyến nghị hành động cho: sinh viên/người tìm việc, doanh nghiệp, trường đại học/chương trình đào tạo.

ĐẦU RA CUỐI CÙNG (PHẢI IN RA TRONG NOTEBOOK)
- Path/link file dữ liệu đã lưu: raw và clean
- Bảng insight chính (top findings)
- Bảng metrics mô hình (so sánh 4+ mô hình)
- Bộ biểu đồ quan trọng
- Kết luận và khuyến nghị (theo 3 nhóm đối tượng)

========================
1) RÀNG BUỘC BẮT BUỘC
========================
- Tất cả thực hiện trong 01 notebook duy nhất: crawl + xử lý + mô hình + kết luận.
- Có tool crawl dữ liệu từ các trang tuyển dụng (có thể dùng Playwright/Scrapy/Requests/BS4/Selenium…).
- Thiết kế “chạy lại được” (reproducible): seed cố định, checkpoint, log, cấu hình rõ ràng.
- Phải lưu file dữ liệu:
  + raw: /data/raw/<source>_raw.jsonl (hoặc parquet)
  + clean: /data/clean/jobs_clean.parquet (hoặc CSV)
- Khi crawl: tôn trọng robots.txt/ToS ở mức hợp lý, rate-limit, retry/backoff, random delay; tránh gây tải.
- Nếu một website chặn mạnh: chuyển sang nguồn khác, ghi chú rõ hạn chế.
- Mọi giả định phải ghi rõ. Mọi bước quan trọng phải có nhận xét dựa trên thực nghiệm.

========================
2) PHẦN A — CHECKLIST YÊU CẦU MÔN HỌC / TIÊU CHÍ CHẤM (BẮT BUỘC)
========================
Trước khi code, hãy “tự tìm kiếm” và tổng hợp (theo chuẩn bài Data Analyst/đồ án phân tích dữ liệu, ưu tiên chuẩn UIT):
- Checklist tiêu chí chấm: (EDA, làm sạch, trực quan hóa, mô hình, đánh giá, báo cáo, khuyến nghị, tái lập)
- Viết checklist vào đầu notebook dạng bảng + checkbox, rồi đối chiếu trong suốt notebook.

========================
3) PHẦN B — ĐẶT VẤN ĐỀ & CÂU HỎI NGHIÊN CỨU (BẮT BUỘC)
========================
3.1. Bối cảnh: thị trường việc làm VN + lý do chọn đề tài.
3.2. Mục tiêu phân tích: mô tả thị trường, phát hiện xu hướng, dự báo, gợi ý kỹ năng.
3.3. Câu hỏi nghiên cứu (ít nhất 10–12 câu), ví dụ:
- Ngành nào tuyển nhiều nhất theo tháng/quý?
- Kỹ năng nào xuất hiện nhiều nhất trong JD theo ngành?
- Lương khác nhau thế nào theo ngành/cấp bậc/khu vực/work_mode?
- Remote/hybrid tăng hay giảm theo thời gian? ngành nào nhiều remote nhất?
- Top công ty theo số lượng tin? có dấu hiệu spam/trùng lặp không?
- Kỹ năng nào gắn với lương cao hơn (Cloud, SQL, Python, BI…)?
- Dự báo số lượng tin tuyển dụng ngành X trong 3–6 tháng tới?

========================
4) PHẦN C — VẼ MÔ HÌNH NGHIÊN CỨU NGAY TRONG NOTEBOOK (BẮT BUỘC)
========================
Bạn PHẢI vẽ (render) trực tiếp trong notebook tối thiểu 02 sơ đồ:

(1) Sơ đồ quy trình nghiên cứu (Research Workflow / Data Pipeline)
- Vẽ flowchart thể hiện:
  Nguồn dữ liệu → Crawl/Extract → Raw Storage → Cleaning/Normalization
  → Feature Engineering (skills extraction, encoding, TF-IDF, time aggregation)
  → EDA/Visualization → Modeling (Regression + Classification + Forecasting)
  → Evaluation (CV + metrics + model comparison) → Insights → Recommendations.
- BẮT BUỘC render được bằng 1 trong các cách:
  a) Mermaid diagram trong markdown (khuyến nghị),
  b) Graphviz,
  c) Matplotlib + NetworkX.
- Sau sơ đồ, viết 5–10 dòng giải thích dữ liệu vào/ra của từng khối.

(2) Sơ đồ mô hình khái niệm (Conceptual Model / Variable Relationship Diagram)
- Phải thể hiện các nhóm biến (features) → biến mục tiêu (targets).
- BẮT BUỘC có ít nhất 02 targets:
  Target A (Regression): salary_median hoặc log_salary
  Target B (Classification): job_level hoặc work_mode (onsite/hybrid/remote)
  Target C (Forecasting): job_post_count_by_month (theo ngành/khu vực)
- Nhóm features phải có:
  - Company/Job: industry/category, company_name, job_title, seniority_suy_từ_title
  - Location/Region: province, region
  - Work arrangement: work_mode, employment_type
  - Requirements: experience_years, skills_extracted (Python/SQL/Excel/BI/Cloud/…)
  - Text: TF-IDF từ title + description
  - Time: posted_date (tháng/quý)
- Vẽ directed graph: features → targets và giải thích.
- BẮT BUỘC kèm:
  + Data Dictionary 15–25 cột quan trọng (tên cột, kiểu, mô tả, cách tạo)
  + >= 6 giả thuyết nghiên cứu H1..Hn liên hệ trực tiếp tới sơ đồ
  + Cách kiểm chứng H1..Hn bằng EDA + feature importance / coefficients.

========================
5) PHẦN D — THU THẬP DỮ LIỆU (CRAWLING TOOL) (BẮT BUỘC)
========================
5.1. Chọn nguồn:
- Ít nhất 2–3 trang tuyển dụng có dữ liệu VN, ưu tiên truy cập công khai.
- Nếu được, thêm 1 nguồn báo cáo thị trường (public) để đối chiếu xu hướng (không bắt buộc crawl).

5.2. Thiết kế schema chuẩn (unified schema) cho job posting:
- source, job_id (tự tạo), url, crawl_time
- job_title
- company_name
- location_raw + location_standard (tỉnh/thành) + region (Bắc/Trung/Nam)
- salary_raw + salary_min + salary_max + salary_currency + salary_period
- job_level (intern/junior/mid/senior/lead/manager) (nếu thiếu suy từ title)
- experience_years_raw + experience_years_min/max
- employment_type (full-time/part-time/contract)
- work_mode (onsite/hybrid/remote)
- posted_date
- industry/category (nếu có)
- description_text
- skills_extracted (list)

5.3. Viết “tool crawl” ngay trong notebook (module-like):
- config (sources, pagination, limits), fetch, parse, normalize, save.
- có rate limit + random delay + retry/backoff + logging.
- có checkpoint để chạy lại không mất tiến độ.
- có 2 chế độ:
  quick_demo (50–200 tin)
  full_run (2,000–10,000 tin tùy khả năng)
- Lưu raw theo từng nguồn và lưu clean merged.

========================
6) PHẦN E — TIỀN XỬ LÝ & FEATURE ENGINEERING (BẮT BUỘC)
========================
6.1. Làm sạch:
- dedup theo url / (title+company+location+posted_date)
- normalize text (remove HTML, normalize unicode)
- chuẩn hóa location (mapping tỉnh/thành; có bảng mapping)
- chuẩn hóa lương:
  parse salary_raw (“15-25 triệu”, “$1000-1500”, “thỏa thuận”…)
  tạo salary_min/max + salary_median
  tạo log_salary
- missing handling: thỏa thuận → missing, suy job_level từ title rule-based.

6.2. Trích kỹ năng:
- Dictionary + regex cho skill (Python, SQL, Excel, Power BI, Tableau, AWS, Azure, GCP, Docker, K8s, Java, .NET, React…)
- Tạo skills_extracted + one-hot skill columns.

6.3. Encoding:
- one-hot categorical (location/industry/work_mode/employment_type)
- TF-IDF cho job_title + description_text (cho bài toán text).

6.4. Split & CV:
- train/test split rõ ràng
- K-fold CV >= 5
- GridSearchCV/RandomizedSearchCV cho ít nhất 1–2 mô hình.

========================
7) PHẦN F — EDA & TRỰC QUAN HÓA (BẮT BUỘC)
========================
- Thống kê mô tả: theo nguồn, thời gian, region, ngành, work_mode.
- BẮT BUỘC >= 12 biểu đồ + nhận xét 2–5 bullet mỗi cụm:
  1) Top ngành theo số tin
  2) Top kỹ năng theo ngành
  3) Heatmap kỹ năng vs ngành
  4) Phân phối lương theo job_level (box/violin)
  5) Lương theo location (top tỉnh/thành)
  6) Remote/hybrid ratio theo ngành
  7) Trend số tin theo tháng/quý
  8) Trend kỹ năng theo thời gian (>= 3 kỹ năng)
  9) Correlation/pairplot cho numeric
  10) Top n-grams (bar) hoặc wordcloud
  11) Top companies theo số tin (lọc spam nếu cần)
  12) Outlier analysis lương

========================
8) PHẦN G — XÁC ĐỊNH YẾU TỐ TÁC ĐỘNG (BẮT BUỘC)
========================
- Ít nhất 2 cách:
  (a) EDA thống kê (groupby, pivot, so sánh distribution),
  (b) feature importance / SHAP (tree model) hoặc hệ số hồi quy (linear).
- Kết luận: yếu tố nào ảnh hưởng mạnh đến lương/nhu cầu.

========================
9) PHẦN H — SO SÁNH NHÓM (BẮT BUỘC)
========================
- Với mỗi biến phân loại quan trọng (region, industry, job_level, work_mode):
  so sánh mean/median salary và số lượng tin
  kết luận nhóm cao nhất/thấp nhất
  giải thích giả thuyết + cảnh báo bias dữ liệu.

========================
10) PHẦN I — XÂY DỰNG & ĐÁNH GIÁ MÔ HÌNH (>= 04 MÔ HÌNH) (BẮT BUỘC)
========================
Bạn PHẢI huấn luyện tối thiểu 4 mô hình, phủ các dạng sau (chọn phù hợp dữ liệu):

A) REGRESSION (dự đoán lương)
- Target: log_salary hoặc salary_median
- Ít nhất 2 mô hình:
  1) Ridge/Lasso/ElasticNet (GridSearchCV)
  2) RandomForestRegressor hoặc GradientBoosting/HistGradientBoosting (hoặc XGBoost nếu dùng)
- Metrics: RMSE, MAE, R2; k-fold CV.

B) CLASSIFICATION (dự đoán job_level hoặc work_mode)
- Ít nhất 1 mô hình:
  3) Logistic Regression (TF-IDF) hoặc LinearSVC hoặc MultinomialNB
- Metrics: Accuracy, F1-macro, confusion matrix (ROC-AUC nếu binary).

C) FORECASTING (dự báo nhu cầu tuyển dụng theo thời gian)
- Ít nhất 1 mô hình:
  4) Prophet/ARIMA/ETS hoặc baseline moving average
- Target: job_post_count_by_month (cho 1–2 ngành trọng điểm)
- Metrics: MAPE/SMAPE, backtesting rolling window.

YÊU CẦU SO SÁNH & CHỌN MÔ HÌNH
- Bảng so sánh mô hình (metrics + thời gian train + ưu/nhược)
- Chọn mô hình tốt nhất cho từng bài toán và giải thích
- Với model tốt nhất: phân tích feature importance / top coefficients → rút insight.

========================
11) PHẦN J — KẾT LUẬN & KHUYẾN NGHỊ (BẮT BUỘC)
========================
- Tổng hợp 5–10 insight lớn (có số liệu minh họa).
- Khuyến nghị tối thiểu 12 ý, chia theo đối tượng:
  1) Người tìm việc/sinh viên
  2) Doanh nghiệp
  3) Trường/đơn vị đào tạo (gợi ý cập nhật chương trình theo kỹ năng thị trường)
- Nêu hạn chế (bias nguồn dữ liệu, nhiều tin “thỏa thuận”, thời gian crawl ngắn, trùng lặp…)
- Nêu hướng phát triển (crawl dài hạn, thêm nguồn, NLP tốt hơn, dashboard…).

========================
12) ACCEPTANCE CRITERIA (BẮT BUỘC)
========================
- Notebook chạy từ đầu đến cuối không lỗi (khi có internet).
- Có raw + clean dataset được lưu file.
- Có >= 12 biểu đồ kèm nhận xét.
- Có >= 4 mô hình đúng mô tả + bảng so sánh + chọn mô hình tốt nhất.
- Có sơ đồ pipeline + sơ đồ conceptual model render ngay trong notebook.
- Có kết luận + khuyến nghị + hạn chế + hướng phát triển.

========================
13) GIẢ ĐỊNH MẶC ĐỊNH (NẾU THIẾU THÔNG TIN)
========================
- Thời gian lấy tin: 3–6 tháng gần nhất hoặc “latest pages”.
- Phạm vi: toàn Việt Nam.
- Số lượng tin mục tiêu: demo 200–500, full 2,000–10,000 tùy khả năng.
- train/test = 80/20; CV=5 hoặc 10.
- Quy đổi lương: nếu thiếu tỷ giá thì giữ currency hoặc dùng tỷ giá giả định và ghi chú rõ.

BẮT ĐẦU THỰC HIỆN NGAY:
- Tạo notebook có mục lục rõ ràng (Markdown headings).
- Viết code theo từng phần.
- Nếu thiếu dữ liệu lương/posted_date ở một nguồn, chủ động bổ sung nguồn khác và ghi chú.
- Ưu tiên dữ liệu crawl thực tế; chỉ dùng dữ liệu mô phỏng để minh họa pipeline khi crawl thất bại, nhưng phải ghi rõ.
