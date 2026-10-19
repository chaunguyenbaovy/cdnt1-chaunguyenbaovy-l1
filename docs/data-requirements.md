# ĐẶC TẢ YÊU CẦU DỮ LIỆU & LƯỢC ĐỒ KHO DỮ LIỆU (TRACK DA)
**Họ tên:** Châu Nguyễn Bảo Vy | **MSSV:** 2374802010578 | **Track:** Data Analytics (DA)
**Bài toán / Luồng nghiệp vụ:** Luồng L1 - Hồ sơ khách hàng & Phân khúc (Smart CRM - Mekong Mobile)

---

## 1. Nguồn Dữ Liệu Đầu Vào (Data Sources)

| Tệp dữ liệu nguồn | Định dạng | Hệ thống nguồn / Xuất xứ | Khối lượng ước tính | Tần suất cập nhật | Vấn đề chất lượng ghi nhận |
| :--- | :---: | :--- | :---: | :---: | :--- |
| `customers_raw.csv` | CSV | Excel 24 cửa hàng, Zalo & sổ tay bảo hành | ~65.000 bản ghi | Hằng tháng (Batch ETL) | 18–22% trùng lặp SĐT (V1); SĐT chứa 84..., 090..., có khoảng trắng; tên chưa chuẩn hóa. |
| `orders_2024_2026.csv` | CSV | Lịch sử đơn hàng 26 tháng từ 24 cửa hàng | ~26.000 đơn hàng | Hằng ngày / Hằng tháng | Lẫn lộn 3 định dạng ngày tháng (DD/MM/YYYY, D-M-YY, YYYY.MM.DD). |
| `order_items.csv` | CSV | Dòng sản phẩm chi tiết theo đơn hàng | ~48.000 bản ghi | Hằng tháng | Một số dòng sai lệch tính toán thanh_tien so với so_luong x don_gia. |

---

## 2. Từ Điển Dữ Liệu Nguồn (`customers_raw.csv`)

| Tên cột thô | Kiểu dữ liệu SQL | Ý nghĩa nghiệp vụ | Giá trị hợp lệ / Ràng buộc | Tỷ lệ lỗi | Quy tắc xử lý ETL (Transformation) |
| :--- | :---: | :--- | :--- | :---: | :--- |
| `raw_id` | `VARCHAR(20)` | Mã ID khách hàng gốc | Chuỗi ký tự, Primary Key gốc | 0% | Giữ nguyên làm khóa gốc để phục vụ truy vết. |
| `full_name` | `VARCHAR(120)` | Họ và tên khách hàng | Chuỗi văn bản tiếng Việt | ~2% | Xóa khoảng trắng thừa, chuyển về Title Case. |
| `phone` | `VARCHAR(20)` | Số điện thoại liên hệ | Khóa định danh nghiệp vụ (QT-01) | ~3% | Áp dụng quy tắc QT-02: Chuẩn hóa về 10 chữ số bắt đầu bằng 0. |
| `address` | `VARCHAR(255)` | Địa chỉ giao hàng / liên hệ | Chuỗi văn bản | ~15% | Giữ nguyên NULL nếu thiếu, chuẩn hóa tên Tỉnh/Thành phố. |
| `created_at` | `VARCHAR(30)` | Ngày tạo hồ sơ gốc | Chuỗi ngày tháng | ~5% | Quy đổi về định dạng chuẩn ISO YYYY-MM-DD HH:mm:ss. |

---

## 3. Quy Tắc Chất Lượng Dữ Liệu (Data Quality Rules - DQ Rules)

1. **Tính đầy đủ (Completeness):**
   - Ngưỡng: Trường `phone` và `full_name` đạt **>= 95%** bản ghi không bị khuyết (`NOT NULL`).
   - Công thức: `Completeness Rate = (Số bản ghi có phone hợp lệ / Tổng số bản ghi) * 100%`.

2. **Tính duy nhất (Uniqueness - QT-01 & V1):**
   - Ngưỡng: **100%** số điện thoại trong bảng sạch `dim_customer` là duy nhất sau khi chuẩn hóa.
   - Xử lý gộp: Xác định và gộp tỷ lệ trùng lặp **18–22%** từ dữ liệu thô, giữ lại bản ghi có giao dịch mới nhất làm Master Record, gắn nhãn `is_deleted = true` cho hồ sơ phụ (QT-13).

3. **Tính nhất quán & Hợp lệ (Validity - QT-02):**
   - Ngưỡng: **100%** giá trị cột `phone` tuân thủ Regex 10 chữ số.
   - Ngưỡng: **100%** định dạng ngày tháng trong `orders` chuyển về chuẩn ISO YYYY-MM-DD.

---

## 4. Lược Đồ Kho Dữ Liệu (Data Warehouse Star Schema Specification)

### 4.1 Phát biểu Hạt Dữ liệu (GRAIN Statement)
> **GRAIN:** *"Mỗi dòng trong bảng `fact_customer_segment` ghi nhận trạng thái phân khúc khách hàng và tổng hợp số liệu chi tiêu / đơn hàng tích lũy trong 12 tháng gần nhất của đúng 1 Khách hàng tại 1 Cửa hàng trong 1 Kỳ báo cáo hằng tháng."*

### 4.2 Chi tiết Bảng Fact & Bảng Dimension (Có đầy đủ Kiểu dữ liệu & Khóa)

#### **A. Bảng Fact: `fact_customer_segment`**
| Tên cột | Kiểu dữ liệu | Loại khóa | Mô tả & Quy tắc nghiệp vụ |
| :--- | :---: | :---: | :--- |
| `customer_key` | `INT` | FK | Khóa ngoại liên kết bảng `dim_customer.customer_key`. |
| `store_key` | `INT` | FK | Khóa ngoại liên kết bảng `dim_store.store_key`. |
| `date_key` | `INT` | FK | Khóa ngoại liên kết bảng `dim_date.date_key` (dạng YYYYMM). |
| `total_spent_12m` | `DECIMAL(15,2)` | Metric | Tổng chi tiêu tích lũy trong 12 tháng gần nhất (VNĐ). |
| `total_orders_12m` | `INT` | Metric | Tổng số đơn hàng thành công trong 12 tháng gần nhất. |
| `segment_code` | `VARCHAR(20)` | Attribute | Mã phân khúc gán tự động (`VIP`, `REGULAR`, `NEW`, `DORMANT`) theo QT-12. |
| `updated_at` | `TIMESTAMP` | System | Thời điểm hệ thống chạy tiến trình Batch ETL phân khúc. |

#### **B. Bảng Dimension: `dim_customer`**
| Tên cột | Kiểu dữ liệu | Loại khóa | Mô tả & Quy tắc nghiệp vụ |
| :--- | :---: | :---: | :--- |
| `customer_key` | `INT` | PK | Khóa chính tự tăng (Surrogate Key). |
| `customer_id` | `VARCHAR(20)` | Business Key | Mã ID khách hàng duy nhất sau gộp trùng. |
| `full_name` | `VARCHAR(120)` | Attribute | Họ và tên khách hàng đã chuẩn hóa Title Case. |
| `phone` | `VARCHAR(20)` | Unique Key | Số điện thoại chuẩn hóa 10 chữ số (QT-02). |
| `mask_phone` | `VARCHAR(20)` | Attribute | Số điện thoại che 4 số giữa (`090****567`) phục vụ bảo mật QT-15. |
| `address` | `VARCHAR(255)` | Attribute | Địa chỉ giao hàng / Tỉnh Thành. |
| `is_deleted` | `BOOLEAN` | Attribute | Cờ xóa mềm gộp trùng (`true` = hồ sơ phụ bị ẩn theo QT-13). |

#### **C. Bảng Dimension: `dim_store`**
| Tên cột | Kiểu dữ liệu | Loại khóa | Mô tả & Quy tắc nghiệp vụ |
| :--- | :---: | :---: | :--- |
| `store_key` | `INT` | PK | Khóa chính tự tăng (Surrogate Key). |
| `store_id` | `VARCHAR(20)` | Business Key | Mã cửa hàng (24 cửa hàng Mekong Mobile). |
| `store_name` | `VARCHAR(100)` | Attribute | Tên cửa hàng chi nhánh. |
| `region` | `VARCHAR(50)` | Attribute | Khu vực địa lý (Miền Tây, TP.HCM...). |

#### **D. Bảng Dimension: `dim_date`**
| Tên cột | Kiểu dữ liệu | Loại khóa | Mô tả & Quy tắc nghiệp vụ |
| :--- | :---: | :---: | :--- |
| `date_key` | `INT` | PK | Khóa chính dạng số YYYYMM (Ví dụ: 202610). |
| `full_date` | `DATE` | Attribute | Ngày đầu tiên của kỳ tháng (2026-10-01). |
| `year` | `INT` | Attribute | Năm báo cáo (2026). |
| `quarter` | `INT` | Attribute | Quý báo cáo (1..4). |
| `month` | `INT` | Attribute | Tháng báo cáo (1..12). |
| `month_name` | `VARCHAR(20)` | Attribute | Tên tháng (October). |

---

## 5. Quy Tắc Phân Khúc Khách Hàng Tự Động (QT-12)

- **VIP:** Tổng chi tiêu 12 tháng >= 30.000.000 VNĐ **HOẶC** >= 8 đơn hàng.
- **THƯỜNG XUYÊN (REGULAR):** Tổng chi tiêu 12 tháng >= 10.000.000 VNĐ **HOẶC** >= 3 đơn hàng.
- **MỚI (NEW):** Có đúng 1 đơn hàng duy nhất trong 90 ngày gần nhất.
- **NGỦ ĐÔNG (DORMANT):** Khách hàng không có đơn hàng nào trong 12 tháng gần nhất.

---

## 6. Câu Hỏi Phân Tích & Mức Độ Chi Tiết (Analytics & Granularity)

| Mã CH | Câu hỏi phân tích nghiệp vụ | Mức độ chi tiết (Granularity) | Đơn vị sử dụng | Quy tắc nghiệp vụ áp dụng |
| :---: | :--- | :--- | :--- | :--- |
| **Q1** | Tỷ lệ hồ sơ khách hàng bị trùng lặp hiện tại là bao nhiêu % và đã làm sạch được bao nhiêu %? | Toàn công ty / Theo Cửa hàng | Marketing, Ban Giám Đốc | Matching SĐT (QT-01, V1, QT-13). |
| **Q2** | Tỷ lệ phân bổ và số lượng khách hàng theo 4 nhóm phân khúc tại từng cửa hàng là bao nhiêu? | Theo Cửa hàng / Theo Kỳ tháng | Quản lý cửa hàng, Marketing | Phân loại hằng tháng theo chi tiêu (QT-12). |
| **Q3** | Danh sách chi tiết khách hàng thuộc phân khúc mục tiêu để xuất file tiếp thị truyền thông? | Theo Phân khúc / Theo Cửa hàng | Nhân viên Marketing | Lọc & Xuất danh sách SMS che SĐT (QT-15, V5). |
