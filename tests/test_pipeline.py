import pytest
import re

# Định nghĩa các hàm logic nghiệp vụ cần kiểm thử (DQ Rules & Business Rules)

def clean_phone(phone):
    if not phone:
        return None
    phone_str = re.sub(r'\D', '', str(phone))
    if phone_str.startswith('84'):
        phone_str = '0' + phone_str[2:]
    if len(phone_str) == 10 and phone_str.startswith('0'):
        return phone_str
    return None


def mask_phone(phone):
    # QT-15: Che 4 số giữa
    if phone and len(phone) == 10:
        return phone[:3] + "****" + phone[7:]
    return phone


def get_segment(spent, orders):
    # QT-12: Phân khúc tự động
    try:
        spent = float(spent) if spent is not None else 0.0
        orders = int(orders) if orders is not None else 0
    except Exception:
        spent, orders = 0.0, 0

    if spent >= 30000000 or orders >= 8:
        return 'VIP'
    elif spent >= 10000000 or orders >= 3:
        return 'REGULAR'
    elif orders >= 1:
        return 'NEW'
    else:
        return 'DORMANT'


# --- BỘ 5 UNIT TEST CASES ---

# Test 1: Kiểm tra chuẩn hóa SĐT từ +84 về dạng 10 số bắt đầu bằng 0 (QT-02)
def test_clean_phone_valid_qt02():
    assert clean_phone("+84901234567") == "0901234567"
    assert clean_phone("0912 345 678") == "0912345678"


# Test 2: Kiểm tra SĐT không hợp lệ (thiếu số / chứa chữ) bị loại bỏ
def test_clean_phone_invalid():
    assert clean_phone("12345") is None
    assert clean_phone("invalid_phone_number") is None


# Test 3: Kiểm tra quy tắc bảo mật che 4 số giữa SĐT (QT-15)
def test_mask_phone_qt15():
    assert mask_phone("0901234567") == "090****567"


# Test 4: Kiểm tra phân khúc tự động nhóm VIP (QT-12)
def test_segment_vip_qt12():
    assert get_segment(35000000, 5) == "VIP"
    assert get_segment(5000000, 10) == "VIP"


# Test 5: Kiểm tra phân khúc tự động nhóm DORMANT (QT-12)
def test_segment_dormant_qt12():
    assert get_segment(0, 0) == "DORMANT"