Nhưng các điểm “bị bắt” vẫn còn (và vài cái vẫn là BLOCKING)
🔴 1) Claim “4 sources” vẫn sai so với pipeline

Cover page + checklist vẫn ghi 4 sources (CareerViet, TopCV, ViecLam24h, JobsGo).

Nhưng code chỉ load 1 file: RAW_PATH = 'data/raw/careerviet_raw.csv' và pd.read_csv(RAW_PATH).

➡️ Đây là blocking về credibility: reviewer sẽ hỏi “4 sources nằm ở đâu?”. Hiện notebook đang tự mâu thuẫn.

🔴 2) Dedup vẫn đang DROP theo job_title + city (dù có note limitation)

Trong code cleaning (Section 2.2) bạn vẫn làm:

duplicates = df.duplicated(subset=['job_title','city'])

df_dedup = df[~duplicates]

log “Removed …% rows …”

➡️ Dù bạn có cảnh báo limitation, reviewer khó tính vẫn đánh giá đây là rủi ro làm méo thị trường (xoá nhầm job hợp lệ). Nếu bạn nói “snapshot thị trường”, bước này vẫn có thể khiến kết quả “top cities/roles/skills” lệch mạnh.

Nếu bạn “đã sửa” theo hướng không drop mà chỉ flag, thì hiện tại notebook chưa phản ánh điều đó.

🔴 3) Currency/unit normalization: vẫn chưa có bằng chứng xử lý

Mình không thấy cell nào:

kiểm tra phân bố unit (unique values / counts), hoặc

convert USD→VND (hoặc khẳng định 100% VND bằng evidence).

➡️ Với bài toán salary, thiếu phần này là rủi ro lớn (không nhất thiết data có USD, nhưng notebook phải chứng minh).

🟡 4) “Evidence-based” nhưng Key Insights vẫn dùng số xấp xỉ “~”

Trong bảng Key Insights, bạn vẫn ghi:

“~60%”, “~70%”, “R² ~0.15–0.20”

➡️ Điều này mâu thuẫn với checklist “All claims with n=”. Reviewer sẽ muốn số đúng từ output (kèm n=), không phải ước lượng.

🟡 5) Imbalance đã xử lý một phần, nhưng CV metric vẫn là Accuracy

Model 3 có class_weight='balanced' và bạn in F1 trên test (tốt), nhưng 5-fold CV đang chạy theo accuracy (scoring='accuracy').

➡️ Với imbalance, accuracy vẫn dễ “ảo”, reviewer sẽ kỳ vọng CV theo F1-macro/weighted (ít nhất là macro).

🟢 6) Tính nhất quán ngôn ngữ vẫn còn “Vietlish”

Ví dụ:

Title tiếng Việt, nhưng section “Setup & Data Loading” tiếng Anh.
➡️ Không phá dự án, nhưng làm giảm cảm giác “report chuyên nghiệp”.

🟢 7) Cover page đang “bẩn” (có code/snippet lẫn vào markdown)

Trong cell đầu có đoạn code (dedup snippet) lẫn vào phần giới thiệu.
➡️ Đây là điểm presentation bị trừ khá rõ khi người khác đọc.