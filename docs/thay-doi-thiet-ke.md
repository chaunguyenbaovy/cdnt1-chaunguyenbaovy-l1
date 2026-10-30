# NHẬT KÝ ĐIỀU CHỈNH THIẾT KẾ (DESIGN CHANGE LOG)

**Môn học:** Chuyên đề Tốt nghiệp 1 (HK1 2026-2027)  
**Sinh viên thực hiện:** Châu Nguyễn Bảo Vy - MSSV: 2374802010578  
**Dự án:** Smart CRM Mekong Mobile - Luồng L1  

---

## BẢNG GHI NHẬN ĐIỀU CHỈNH THIẾT KẾ SO VỚI BÀI TẬP 1 (BT1)

| Mã thay đổi | Hạng mục điều chỉnh | Mô tả chi tiết lý do & Giải pháp thực hiện | Kết quả cập nhật |
| :---: | :--- | :--- | :--- |
| **TD-01** | **Mô hình hóa Kho dữ liệu Star Schema (DWH)** | Tiếp thu phản hồi của Giảng viên ở BT1 về việc cần làm rõ cấu trúc lưu trữ cho phân tích, nhóm đã chuyển đổi lưu trữ từ bảng phẳng sang CSDL Star Schema `dwh.db` gồm `dim_customer` và `fact_customer_segment`. | Đã nạp thành công dữ liệu vào `dwh.db`, có phát biểu Hạt Dữ liệu (GRAIN Statement) rõ ràng. |
| **TD-02** | **Cập nhật Wireframe & Layout Dashboard Streamlit** | Tối ưu hóa giao diện hiển thị báo cáo: bổ sung biểu đồ cột phân bổ phân khúc (QT-12) và bảng tra cứu danh sách tiếp thị mục tiêu có mã hóa che SĐT (QT-15). | Dựng hoàn chỉnh tệp `app.py`, xử lý trọn vẹn 3 trạng thái UI (Loading, Empty, Error). |
| **TD-03** | **Bổ sung Bộ kiểm thử tự động (Unit Tests - Pytest)** | Xây dựng bộ 5 test cases bằng thư viện `pytest` để kiểm thử tự động các quy tắc chất lượng dữ liệu (DQ Rules) và gán phân khúc trước khi nạp vào Kho DWH. | Chạy lệnh `pytest` ra kết quả xanh `5 passed in 0.06s` bao phủ đủ 3 loại test. |