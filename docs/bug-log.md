# NHẬT KÝ LỖI VÀ CÁCH KHẮC PHỤC (BUG LOG)

| Mã lỗi | Mô tả sự cố | Nguyên nhân | Giải pháp khắc phục | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| **BUG-01** | Chạy lại `pipeline.py` lần 2 bị nhân đôi dòng dữ liệu trong kho `dwh.db`. | Chưa thiết lập khóa chính (Primary Key) và câu lệnh SQL INSERT thông thường bị ghi đè trùng dòng. | Cập nhật bảng `fact_customer_segment` dùng cú pháp `INSERT OR REPLACE` / `UPSERT` theo tiêu chí C5. | **ĐÃ SỬA [✓]** |
| **BUG-02** | SĐT chứa ký tự đệm `+84` hoặc khoảng trắng bị loại bỏ nhầm. | Chuỗi Regex cũ chưa xử lý tiền tố quốc tế. | Bổ sung hàm chuẩn hóa `clean_phone_number()` đưa về chuẩn 10 số đầu `0` theo quy tắc QT-02. | **ĐÃ SỬA [✓]** |