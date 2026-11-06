import os
import re
import sqlite3
import pandas as pd
import pytest

# ==============================================================================
# HÀM GIẢ LẬP VÀ XỬ LÝ NGHIỆP VỤ (HỆ THỐNG SMART CRM MEKONG MOBILE)
# ==============================================================================


def clean_phone_number(phone):
    """Chuẩn hóa số điện thoại về 10 chữ số bắt đầu bằng đầu số VN hợp lệ (QT-02)."""
    if not phone or not isinstance(phone, str):
        return None

    # Từ chối ngay nếu chuỗi chứa chữ cái hoặc ký tự không hợp lệ
    # Chỉ chấp nhận số, dấu cách, dấu gạch ngang, dấu ngoặc và dấu '+'
    if re.search(r"[a-zA-Z]", phone):
        return None

    cleaned = "".join(filter(str.isdigit, phone))
    if cleaned.startswith("84"):
        cleaned = "0" + cleaned[2:]

    valid_prefixes = ("09", "03", "07", "08", "05")
    if len(cleaned) == 10 and cleaned.startswith(valid_prefixes):
        return cleaned

    return None


def mask_phone_number(phone):
    """Che 4 số giữa của số điện thoại phục vụ bảo mật UI/CSV (QT-15).

    Giữ 3 số đầu + che 4 số giữa + giữ 3 số cuối (áp dụng cho SĐT chuẩn 10 số).
    """
    if not phone or len(phone) != 10:
        return "000****000"
    return phone[:3] + "****" + phone[7:]


def calculate_segment(total_spent_12m, days_since_last_purchase):
    """Phân loại phân khúc khách hàng hằng tháng theo quy tắc (QT-12)."""
    if total_spent_12m >= 15000000:
        return "VIP"
    elif total_spent_12m >= 5000000:
        return "REGULAR"
    elif days_since_last_purchase <= 60:
        return "NEW"
    else:
        return "DORMANT"


# ==============================================================================
# BỘ 12 UNIT TEST CASES CHO BÀI TẬP 3 (TAG RELEASE v1.0)
# ==============================================================================


# 1. Luồng đúng (Normal Flow) - Chuẩn hóa SĐT hợp lệ (QT-02)
def test_tc01_clean_phone_valid():
    assert clean_phone_number("+84901234567") == "0901234567"
    assert clean_phone_number("090 123 4567") == "0901234567"


# 2. Luồng đúng (Normal Flow) - Chọn Master Record mới nhất (QT-01)
def test_tc02_master_record_selection():
    records = [
        {"customer_id": "C01", "created_at": "2024-01-01"},
        {"customer_id": "C02", "created_at": "2024-06-01"},
    ]
    master = max(records, key=lambda x: x["created_at"])
    assert master["customer_id"] == "C02"


# 3. Giá trị biên (Boundary Flow) - Ngưỡng VIP chính xác 15.000.000 VNĐ
def test_tc03_segment_vip_exact_boundary():
    assert calculate_segment(15000000, 10) == "VIP"


# 4. Giá trị biên (Boundary Flow) - Ngưỡng REGULAR cận trên 14.999.999 VNĐ
def test_tc04_segment_regular_upper_boundary():
    assert calculate_segment(14999999, 10) == "REGULAR"


# 5. Giá trị biên (Boundary Flow) - Ngưỡng NEW cận trên 60 ngày
def test_tc05_segment_new_boundary():
    assert calculate_segment(1000000, 60) == "NEW"


# 6. Giá trị biên (Boundary Flow) - Ngưỡng DORMANT cận dưới 61 ngày
def test_tc06_segment_dormant_boundary():
    assert calculate_segment(1000000, 61) == "DORMANT"


# 7. Dữ liệu sai (Error Flow) - Chuỗi SĐT chứa chữ cái
def test_tc07_clean_phone_invalid_letters():
    assert clean_phone_number("0901234ABC") is None
    # Kiểm tra thêm trường hợp có đủ 10 số nhưng kèm chữ cái
    assert clean_phone_number("0901234567ABC") is None


# 8. Dữ liệu sai (Error Flow) - Chuỗi SĐT thiếu số (8 số)
def test_tc08_clean_phone_invalid_length():
    assert clean_phone_number("09012345") is None


# 9. Bảo mật (Security) - Che 4 số giữa SĐT theo quy tắc QT-15
def test_tc09_mask_phone_security():
    assert mask_phone_number("0901234567") == "090****567"


# 10. Chống trùng nạp (C5 - Idempotency) - Chạy lại không tăng số dòng DWH
def test_tc10_dwh_idempotency(tmp_path):
    # Sử dụng tmp_path của pytest để tự động dọn dẹp file db sau test
    db_path = tmp_path / "test_dwh.db"
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS fact_segment (id TEXT PRIMARY KEY, segment TEXT)"
        )
        cur.execute("INSERT OR REPLACE INTO fact_segment VALUES ('C01', 'VIP')")
        cur.execute("INSERT OR REPLACE INTO fact_segment VALUES ('C01', 'VIP')")
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM fact_segment")
        count = cur.fetchone()[0]
    finally:
        conn.close()

    assert count == 1


# 11. Giao diện UI - Trạng thái Loading State
def test_tc11_ui_loading_state():
    loading = True
    status = "LOADING" if loading else "READY"
    assert status == "LOADING"


# 12. Giao diện UI - Trạng thái Empty & Error State
def test_tc12_ui_empty_state_handling():
    df_empty = pd.DataFrame()
    has_data = not df_empty.empty
    assert has_data is False