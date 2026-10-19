import os
import re
import pandas as pd


def clean_phone(phone_str):
    if pd.isna(phone_str):
        return None
    phone = re.sub(r"\D", "", str(phone_str))
    if phone.startswith("84") and len(phone) == 11:
        phone = "0" + phone[2:]
    return phone if len(phone) == 10 and phone.startswith("0") else None


def run_pipeline():
    print("=== SPRINT 1 (BUỔI 8): MODULE CỐT LÕI DATA ETL - LUỒNG L1 ===")

    # 1. Extract: Đọc file dữ liệu nguồn
    file_path = "data/raw/customers_raw.csv"
    if not os.path.exists(file_path):
        os.makedirs("data/raw", exist_ok=True)
        sample_data = {
            "raw_id": ["CUST01", "CUST02", "CUST03", "CUST04"],
            "full_name": ["nguyen van a", "Tran Thi B ", "Le Van C", "Pham Thi D"],
            "phone": ["+84901234567", "0912345678", "84988888888", "0901234567"],
            "address": ["HCM", "Ha Noi", "Can Tho", "HCM"],
        }
        pd.DataFrame(sample_data).to_csv(file_path, index=False)

    df = pd.read_csv(file_path)

    # --- ĐÚNG CHUẨN RUBRIC TRACK DA: In số dòng, số cột, số ô trống ---
    print(f"[EXTRACT] Số dòng: {df.shape[0]}")
    print(f"[EXTRACT] Số cột: {df.shape[1]}")
    print(f"[EXTRACT] Tổng số ô trống (null): {df.isna().sum().sum()}")

    # 2. Transform: Chuẩn hóa tên & SĐT (QT-02)
    df["full_name_clean"] = df["full_name"].astype(str).str.strip().str.title()
    df["phone_clean"] = df["phone"].apply(clean_phone)

    # 3. Quality Check
    valid_df = df[df["phone_clean"].notna()].copy()
    reject_df = df[df["phone_clean"].isna()].copy()

    print(f"[QUALITY] Hợp lệ (QT-02): {len(valid_df)} / {len(df)}")
    print(f"[QUALITY] Bị loại/Lỗi: {len(reject_df)}")

    print("\n--- KẾT QUẢ MẪU SAU KHI LÀM SẠCH ---")
    print(valid_df[["raw_id", "full_name_clean", "phone_clean"]])


if __name__ == "__main__":
    run_pipeline()