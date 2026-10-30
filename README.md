# Smart CRM Mekong Mobile - Luồng L1 (Hồ sơ Khách hàng & Phân khúc)

**Thông tin sinh viên:**
- **Họ và tên:** Châu Nguyễn Bảo Vy
- **MSSV:** 2374802010578
- **Lớp:** 71K29CNTT07
- **Track kỹ năng:** Data Analytics (DA)
- **Học phần:** Chuyên đề Tốt nghiệp 1 (HK1 2026-2027)
- **Luồng nghiệp vụ:** Luồng L1 - Hồ sơ khách hàng & Phân khúc (Mekong Mobile)
- **Phiên bản:** Bài tập 2 (Tag Release `v0.2`)
- **GitHub Repository:** https://github.com/chaunguyenbaovy/cdnt1-chaunguyenbaovy-l1

---

## 1. Mục tiêu hệ thống
Hệ thống Prototype Smart CRM hỗ trợ quản lý hồ sơ khách hàng cho chuỗi bán lẻ Mekong Mobile. Module tập trung xử lý các bài toán cốt lõi:
- **Xử lý trùng lặp (V1):** Chuẩn hóa SĐT (QT-02) và gộp trùng dữ liệu khách hàng theo SĐT bằng cơ chế UPSERT (`ON CONFLICT`).
- **Phân khúc khách hàng (V5):** Tự động tính tổng chi tiêu 12 tháng, tổng đơn hàng 12 tháng và gán nhãn phân khúc (VIP, REGULAR, NEW, DORMANT) theo quy tắc QT-12.
- **Bảo mật dữ liệu (QT-15):** Che 4 số giữa SĐT (`090****567`) trên giao diện báo cáo và tệp CSV xuất ra.

---

## 2. Yêu cầu môi trường
- Python 3.10+
- Môi trường ảo Python (`venv`)
- Các thư viện phụ thuộc: `pandas`, `sqlite3`, `pytest`, `streamlit`

---

## 3. Hướng dẫn chạy hệ thống End-to-End (Runbook)

Thực hiện lần lượt 4 lệnh sau tại thư mục gốc của dự án:

```powershell
# Bước 1: Kích hoạt môi trường ảo
venv\Scripts\activate

# Bước 2: Chạy Pipeline ETL & Nạp Kho dữ liệu DWH
python pipeline.py

# Bước 3: Chạy bộ kiểm thử tự động (Unit Tests)
pytest

# Bước 4: Mở giao diện Dashboard Streamlit
streamlit run app.py
```

---

## 4. Cấu trúc thư mục dự án
```text
cdnt1-chaunguyenbaovy-l1/
├── data/
│   └── raw/
│       └── customers_raw.csv        # Dữ liệu khách hàng thô ban đầu
├── docs/
│   ├── thay-doi-thiet-ke.md        # Nhật ký điều chỉnh thiết kế
│   └── ai-disclosure.md            # Bảng khai báo công cụ AI
├── tests/
│   └── test_pipeline.py            # Bộ 5 Unit Test Cases (Pytest)
├── app.py                          # Giao diện Dashboard Streamlit
├── dwh.db                          # CSDL Kho dữ liệu SQLite (Star Schema)
├── pipeline.py                     # Script Pipeline ETL & Nạp DWH
└── README.md                       # Tài liệu hướng dẫn chạy hệ thống
```

---

## 5. Quy tắc nghiệp vụ (Business Rules)

| Mã quy tắc | Tên quy tắc | Mô tả xử lý |
| :--- | :--- | :--- |
| **QT-02** | Chuẩn hóa SĐT | Loại bỏ ký tự đặc biệt, chuyển `+84` / `84` thành `0`, đảm bảo đúng 10 số. |
| **QT-12** | Phân khúc KH | Tính tổng chi tiêu và số đơn hàng 12 tháng gần nhất để gán nhãn: `VIP`, `REGULAR`, `NEW`, `DORMANT`. |
| **QT-15** | Bảo mật SĐT | Che 4 chữ số giữa: `090****567` (giữ 3 số đầu và 3 số cuối) khi hiển thị và xuất file. |

---

## 6. Trạng thái hiện tại
- [x] **Sprint 1 (Buổi 8):** Xây dựng Module cốt lõi ETL, làm sạch dữ liệu SĐT (QT-02).
- [x] **Sprint 2 (Buổi 10 – 12):** Nạp Kho dữ liệu Star Schema (`dwh.db`), hoàn thành bộ 5 Unit Test Pytest (`5 passed`), xây dựng Dashboard Streamlit (`app.py`) và tạo Tag Release `v0.2` nộp Bài tập 2.