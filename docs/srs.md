# MẪU ĐẶC TẢ YÊU CẦU DỮ LIỆU (DATA REQUIREMENT SPECIFICATION - TRACK DA)

**Họ tên:** Châu Nguyễn Bảo Vy | **MSSV:** 2374802010578 | **Track:** Data Analytics (DA)  
**Bài toán / Luồng nghiệp vụ:** Luồng L1 - Hồ sơ khách hàng & Phân khúc (Smart CRM - Mekong Mobile)

---

## 1. Nguồn dữ liệu đầu vào (Data Sources)

| Tệp dữ liệu nguồn | Định dạng | Hệ thống nguồn / Xuất xứ | Khối lượng ước tính | Tần suất cập nhật | Vấn đề chất lượng ghi nhận |
| :--- | :---: | :--- | :---: | :---: | :--- |
| `customers_raw.csv` | CSV | Tổng hợp từ Excel 24 cửa hàng, Zalo & sổ tay bảo hành | ~65.000 bản ghi | Hằng tháng (Batch ETL) | 18–22% trùng lặp; SĐT chứa nhiều định dạng (`84...`, `090...`, có khoảng trắng); tên chưa chuẩn hóa. |
| `orders_2024_2026.csv` | CSV | Lịch sử đơn hàng 26 tháng từ 24 cửa hàng | ~26.000 đơn hàng | Hằng ngày / Hằng tháng | 3 định dạng ngày tháng lẫn lộn (`DD/MM/YYYY`, `D-M-YY`, `YYYY.MM.DD`). |
| `order_items.csv` | CSV | Dòng sản phẩm chi tiết theo đơn | ~48.000 bản ghi | Hằng tháng | Vài dòng `thanh_tien` lệch so với `so_luong` × `don_gia`. |

---

## 2. Từ điển dữ liệu nguồn (Data Dictionary - `customers_raw.csv`)

| Tên cột | Kiểu dữ liệu thô | Ý nghĩa nghiệp vụ | Giá trị hợp lệ / Ràng buộc | Tỷ lệ thiếu/lỗi | Quy tắc xử lý (Transformation) |
| :--- | :---: | :--- | :--- | :---: | :--- |
| `raw_id` | `VARCHAR(20)` | Mã ID khách hàng gốc | Chuỗi ký tự, Primary Key gốc | 0% | Giữ nguyên làm khóa gốc để truy vết. |
| `full_name` | `VARCHAR(120)` | Họ và tên khách hàng | Chuỗi văn bản tiếng Việt | ~2% | Xóa khoảng trắng thừa, chuyển về Title Case (`Nguyễn Văn A`). |
| `phone` | `VARCHAR(20)` | Số điện thoại liên hệ | Khóa định danh nghiệp vụ (QT-01) | ~3% | Áp dụng quy tắc **QT-02**: Chuẩn hóa về 10 chữ số bắt đầu bằng `0` (ví dụ: `+84901234567` → `0901234567`). |
| `address` | `VARCHAR(255)` | Địa chỉ giao hàng / liên hệ | Chuỗi văn bản | ~15% | Giữ nguyên `NULL` nếu thiếu, chuẩn hóa tên Tỉnh/Thành phố. |
| `created_at` | `VARCHAR(30)` | Ngày tạo hồ sơ gốc | Chuỗi ngày tháng | ~5% | Quy đổi về định dạng chuẩn ISO `YYYY-MM-DD HH:mm:ss`. |

---

## 3. Quy tắc chất lượng dữ liệu (Data Quality Rules - DQ Rules)

1. **Tính đầy đủ (Completeness)**:
   - Ngưỡng: Trường `phone` và `full_name` đạt **≥ 95%** bản ghi không bị khuyết (`NOT NULL`).
   - Công thức: `Completeness Rate = (Số bản ghi có phone hợp lệ / Tổng số bản ghi) * 100%`.

2. **Tính duy nhất (Uniqueness - QT-01 & V1)**:
   - Ngưỡng: **100%** số điện thoại trong bảng sạch `customer_clean` là duy nhất sau khi chuẩn hóa.
   - Xử lý gộp: Xác định và gộp tỷ lệ trùng lặp **18–22%** từ dữ liệu thô, giữ lại bản ghi có giao dịch mới nhất làm Master Record.

3. **Tính nhất quán & Hợp lệ (Consistency & Validity - QT-02)**:
   - Ngưỡng: **100%** giá trị cột `phone` tuân thủ Regex: `^0[3|5|7|8|9]{8}$`.
   - Ngưỡng: **100%** định dạng ngày tháng trong `orders` chuyển về ISO `YYYY-MM-DD`.

---

## 4. Câu hỏi phân tích & Mức độ chi tiết (Analytics & Granularity)

| Mã CH | Câu hỏi phân tích nghiệp vụ | Mức độ chi tiết (Granularity) | Đơn vị sử dụng | Quy tắc nghiệp vụ áp dụng |
| :---: | :--- | :--- | :--- | :--- |
| **Q1** | Tỷ lệ hồ sơ khách hàng bị trùng lặp hiện tại là bao nhiêu và đã làm sạch được bao nhiêu %? | Toàn công ty / Theo từng Cửa hàng | Marketing, Ban Giám Đốc | Phát hiện trùng SĐT (QT-01, V1). |
| **Q2** | Tỷ lệ phân bổ và số lượng khách hàng theo từng phân khúc (VIP, Thường xuyên, Mới, Ngủ đông) là bao nhiêu? | Theo Cửa hàng / Hằng tháng | Quản lý cửa hàng, Marketing | Phân loại hằng tháng theo chi tiêu 12 tháng gần nhất (QT-12). |
| **Q3** | Danh sách chi tiết khách hàng thuộc phân khúc mục tiêu để xuất file chạy chiến dịch truyền thông? | Theo Phân khúc cụ thể / Theo Cửa hàng | Nhân viên Marketing | Lọc & Xuất danh sách tránh gửi tin tràn lan (V5). |

---

## 5. Quy tắc Phân khúc Khách hàng (QT-12)

- **VIP**: Tổng chi tiêu 12 tháng ≥ 30.000.000 VNĐ **HOẶC** ≥ 8 đơn hàng.
- **THƯỜNG XUYÊN**: Tổng chi tiêu 12 tháng ≥ 10.000.000 VNĐ **HOẶC** ≥ 3 đơn hàng.
- **MỚI**: Có 1 đơn hàng duy nhất trong 90 ngày gần nhất.
- **NGỦ ĐÔNG**: Khách hàng không có đơn hàng nào trong 12 tháng gần nhất.