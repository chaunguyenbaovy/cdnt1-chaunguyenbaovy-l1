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


def clean_name(name_str):
    if pd.isna(name_str):
        return None
    words = str(name_str).strip().split()
    return " ".join(words).title()


def run_pipeline():
    print("=== SPRINT 1 (BUOI 8): MODULE COT LOI DATA ETL - LUONG L1 ===")

    # 1. EXTRACT: Doc file du lieu nguon
    raw_dir = "data/raw"
    file_path = os.path.join(raw_dir, "customers_raw.csv")

    if not os.path.exists(file_path):
        os.makedirs(raw_dir, exist_ok=True)
        sample_data = {
            "raw_id": ["CUST01", "CUST02", "CUST03", "CUST04", "CUST05"],
            "full_name": ["nguyen van a", "Tran Thi B ", "Le   Van  C", "Pham Thi D", None],
            "phone": ["+84901234567", "0912345678", "84988888888", "0901234567", "invalid_123"],
            "address": ["HCM", "Ha Noi", "Can Tho", "HCM", "Da Nang"],
        }
        pd.DataFrame(sample_data).to_csv(file_path, index=False)
        print(f"[EXTRACT] Tao du lieu thu nghiem tai: {file_path}")

    df = pd.read_csv(file_path)
    print(f"[EXTRACT] Doc thanh cong {len(df)} ban ghi")

    # 2. TRANSFORM: Chuan hoa ten va SDT (QT-02)
    df["full_name_clean"] = df["full_name"].apply(clean_name)
    df["phone_clean"] = df["phone"].apply(clean_phone)

    # 3. QUALITY CHECK
    valid_df = df[df["phone_clean"].notna()].copy()
    reject_df = df[df["phone_clean"].isna()].copy()

    print(f"[QUALITY] Hop le (QT-02): {len(valid_df)} / {len(df)}")
    print(f"[QUALITY] Bi loai/Loi: {len(reject_df)}")

    # 4. LOAD: Xuat du lieu sang data/processed
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    valid_output_path = os.path.join(processed_dir, "customers_cleaned.csv")
    reject_output_path = os.path.join(processed_dir, "customers_rejected.csv")

    valid_df.to_csv(valid_output_path, index=False)
    reject_df.to_csv(reject_output_path, index=False)
    print(f"[LOAD] Da luu du lieu sach vao: {valid_output_path}")
    print(f"[LOAD] Da luu du lieu loi vao: {reject_output_path}")

    print("\n--- KET QUA MAU SAU KHI LAM SACH ---")
    print(valid_df[["raw_id", "full_name_clean", "phone_clean", "address"]])


if __name__ == "__main__":
    run_pipeline()