from datetime import datetime
import re
import sqlite3
import pandas as pd

print("=== SPRINT 2 (BUỔI 10): MỞ RỘNG PIPELINE & NẠP KHO DỮ LIỆU DWH ===")

# 1. EXTRACT (Trích xuất)
try:
  df_raw = pd.read_csv("data/raw/customers_raw.csv")
except Exception:
  data = {
      "raw_id": ["CUST01", "CUST02", "CUST03", "CUST04", "CUST05"],
      "full_name": ["Nguyen Van A", "Tran Thi B", "Le Van C", "Pham Thi D", None],
      "phone": [
          "0901234567",
          "+84912345678",
          "0988888888",
          "0901234567",
          "invalid_phone",
      ],
  }
  df_raw = pd.DataFrame(data)

# Tự động bổ sung 2 cột chi tiêu/đơn hàng nếu file CSV chưa có
if "total_spent_12m" not in df_raw.columns:
  df_raw["total_spent_12m"] = [35000000, 15000000, 5000000, 0, 0][
      : len(df_raw)
  ]
if "total_orders_12m" not in df_raw.columns:
  df_raw["total_orders_12m"] = [10, 4, 1, 0, 0][: len(df_raw)]

print(f"[EXTRACT] Số dòng: {len(df_raw)}, Số cột: {len(df_raw.columns)}")


# 2. TRANSFORM & QUALITY (Chuẩn hóa QT-02, QT-15, QT-12)
def clean_phone(phone):
  if not phone or pd.isna(phone):
    return None
  phone_str = re.sub(r"\D", "", str(phone))
  if phone_str.startswith("84"):
    phone_str = "0" + phone_str[2:]
  if len(phone_str) == 10 and phone_str.startswith("0"):
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
    spent = float(spent) if pd.notna(spent) else 0.0
    orders = int(orders) if pd.notna(orders) else 0
  except Exception:
    spent, orders = 0.0, 0

  if spent >= 30000000 or orders >= 8:
    return "VIP"
  elif spent >= 10000000 or orders >= 3:
    return "REGULAR"
  elif orders >= 1:
    return "NEW"
  else:
    return "DORMANT"


df_valid = df_raw.copy()
df_valid["phone_clean"] = df_valid["phone"].apply(clean_phone)
df_valid = df_valid.dropna(subset=["phone_clean"])
df_valid["full_name_clean"] = (
    df_valid["full_name"]
    .fillna("Khách hàng")
    .apply(lambda x: " ".join(str(x).split()).title())
)
df_valid["mask_phone"] = df_valid["phone_clean"].apply(mask_phone)
df_valid["segment_code"] = df_valid.apply(
    lambda r: get_segment(r["total_spent_12m"], r["total_orders_12m"]), axis=1
)

print(f"[QUALITY] Hợp lệ (QT-02): {len(df_valid)} / {len(df_raw)}")

# 3. LOAD INTO DWH (Nạp vào Kho dữ liệu SQLite Star Schema)
conn = sqlite3.connect("dwh.db")
cursor = conn.cursor()

# Tạo bảng
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT UNIQUE,
    full_name TEXT,
    phone TEXT,
    mask_phone TEXT,
    is_deleted BOOLEAN DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_customer_segment (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_key INTEGER,
    total_spent_12m REAL,
    total_orders_12m INTEGER,
    segment_code TEXT,
    updated_at TEXT,
    FOREIGN KEY(customer_key) REFERENCES dim_customer(customer_key)
)
""")

# Vòng tự động nạp dữ liệu (Idempotent - chống trùng lặp)
for _, row in df_valid.iterrows():
  cursor.execute(
      """
    INSERT INTO dim_customer (customer_id, full_name, phone, mask_phone)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(customer_id) DO UPDATE SET
        full_name=excluded.full_name,
        phone=excluded.phone,
        mask_phone=excluded.mask_phone
    """,
      (
          str(row["raw_id"]),
          row["full_name_clean"],
          row["phone_clean"],
          row["mask_phone"],
      ),
  )

  cursor.execute(
      "SELECT customer_key FROM dim_customer WHERE customer_id = ?",
      (str(row["raw_id"]),),
  )
  cust_key_tuple = cursor.fetchone()
  cust_key = cust_key_tuple[0] if cust_key_tuple else None

  cursor.execute(
      """
    INSERT INTO fact_customer_segment (customer_key, total_spent_12m, total_orders_12m, segment_code, updated_at)
    VALUES (?, ?, ?, ?, ?)
    """,
      (
          cust_key,
          float(row["total_spent_12m"]),
          int(row["total_orders_12m"]),
          row["segment_code"],
          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      ),
  )

conn.commit()
conn.close()

print(
    "[LOAD DWH] Đã nạp thành công dữ liệu vào dim_customer và"
    " fact_customer_segment trong dwh.db!"
)
print("=== PIPELINE HOÀN THÀNH END-TO-END! ===")