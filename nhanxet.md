1) Mâu thuẫn lớn về “tỷ lệ tin có lương”

Trong phần assumptions/limitations bạn ghi “chỉ khoảng 15–25% tin có lương công khai”.

Nhưng ở phần chuẩn bị ML, notebook in ra: model-ready (has salary) ~79,768 / 85,470 = ~93.3% và bảng “Missing salary pattern” cũng cho thấy Has Salary ~95–99% theo nhóm.

✅ Việc cần làm: chọn 1 sự thật và đồng bộ toàn notebook. Nếu data thật sự có lương ~93% thì:

Bỏ claim 15–25%

Giảm “selection bias” xuống mức phù hợp (hoặc giải thích: “salary là parse từ text, có thể noisy/không chuẩn” nếu đúng).

2) Claim “4 nguồn dữ liệu” chưa có bằng chứng trong data

Notebook nói crawl 4 nguồn, nhưng dataset không có cột source và không có đoạn “audit” chứng minh phân bổ theo nguồn (counts theo domain/platform).

Bạn có ghi “Thiếu cột source” là hạn chế (đúng), nhưng đồng thời vẫn đưa bảng “ước tính số tin theo từng nguồn” → dễ bị xem là suy đoán.

✅ Việc cần làm (chọn 1):

A) Thêm source vào data + thống kê thật (groupby source).

B) Nếu không chứng minh được: đổi wording thành “dataset tổng hợp (không truy vết theo nguồn)” và xoá các con số ước tính theo nguồn.

3) “Loại trùng lặp” trong kết luận chưa đúng với logic thực tế

Cleaning hiện tại: không remove duplicates nếu không có company_name; bạn chỉ flag is_potential_duplicate (đây là cách làm đúng và trung thực).

Nhưng phần kết luận ghi “Sau làm sạch: loại trùng lặp, outlier” → mô tả sai.

✅ Sửa: “flag duplicates (không loại do thiếu company_name)” hoặc “dedup chỉ thực hiện khi có company_name”.

4) Nói “có ý nghĩa thống kê/ANOVA” nhưng chưa thấy test

RQ3 ghi “Box plot, ANOVA”, phần nhận xét Chart 8 có câu “có ý nghĩa thống kê”.

Nhưng trong code không thấy t-test/ANOVA cho chênh lệch lương theo vùng (ít nhất là scipy.stats/Kruskal/ANOVA).

✅ Việc cần làm:

Hoặc thêm kiểm định (và report p-value + effect size),

Hoặc đổi câu chữ thành “chênh lệch quan sát được ~10–15%” (không khẳng định significance).

5) Lỗi nhỏ nhưng “kém chuyên nghiệp”

Cuối notebook ghi “Notebook hoàn thành: December 2024” trong khi dữ liệu mô tả là 12/2025 → lệch timeline.

Trộn ngôn ngữ: có chỗ label chart tiếng Anh (“Number of Job Postings”) nhưng narrative tiếng Việt.

Emoji trong code output/section (📊🔍…) nếu mục tiêu “professional” thì nên tiết chế.

Đánh giá “hay và thực tế” chưa?

Hay: Storytelling tốt, có cấu trúc nghiên cứu, có pipeline, có chart + nhận xét, có ML + tổng kết + khuyến nghị theo 3 nhóm đối tượng.

Thực tế ở mức học thuật/portfolio: ổn.

Chưa đủ thực tế để gọi là “market insight đáng tin” nếu chưa xử lý các điểm mâu thuẫn/claim ở trên (đặc biệt salary-rate và 4 sources). Những lỗi này làm người đọc nghi ngờ toàn bộ kết quả.

5 chỉnh sửa ưu tiên để “khớp” và “thực tế” hơn (theo thứ tự)

Chuẩn hoá sự thật về lương: chốt % has_salary thật và sửa toàn bộ narrative liên quan.

Chốt claim nguồn dữ liệu: có source thì chứng minh; không có thì bỏ số ước tính theo nguồn.

Sửa kết luận về dedup: ghi đúng là “flag”, không nói “loại”.

Bỏ/hoàn thiện các câu “ý nghĩa thống kê/ANOVA”.

Polish trình bày: đồng nhất tiếng Việt, bỏ emoji không cần, sửa timeline cuối notebook. 

Bài toán và giả thuyết đặt ra chưa được hay và thực tế, cần cải thiện