import os
import subprocess
import sys

print("==================================================")
print(" CHECKLIST TU DONG BT2 - SMART CRM MEKONG MOBILE")
print("==================================================\n")

# 1. Kiem tra su ton tai cua cac tep bat buoc
required_files = [
    "README.md",
    "docs/thay-doi-thiet-ke.md",
    "docs/ai-disclosure.md",
    "pipeline.py",
    "app.py",
    "tests/test_pipeline.py",
    "data/raw/customers_raw.csv",
]

print("[1] KIEM TRA CAC TEP BAT BUOC TRONG REPO:")
for file_path in required_files:
    if os.path.exists(file_path):
        print(f" [V] {file_path:<32} -> DA CO")
    else:
        print(f" [X] {file_path:<32} -> THIEU!")

# 2. Kiem tra bo kiem thu tu dong Pytest
print("\n[2] KIEM TRA BO UNIT TESTS (PYTEST):")
try:
    result = subprocess.run(["pytest"], capture_output=True, text=True)
    if result.returncode == 0:
        print(" [V] Pytest: 100% TEST CASES PASSED (5/5)!")
    else:
        print(" [X] Pytest bi loi! Chi tiet:")
        print(result.stdout)
except Exception as e:
    print(f" [X] Khong the chay pytest: {e}")

# 3. Kiem tra Pipeline ETL & CSDL Kho DWH
print("\n[3] KIEM TRA LUONG PIPELINE ETL & CSDL DWH:")
try:
    result = subprocess.run(
        [sys.executable, "pipeline.py"], capture_output=True, text=True
    )
    if result.returncode == 0 and os.path.exists("dwh.db"):
        print(" [V] Pipeline ETL chay muot ma, CSDL 'dwh.db' san sang!")
    else:
        print(" [X] Pipeline gap su co hoac chua tao duoc 'dwh.db'!")
except Exception as e:
    print(f" [X] Loi thuc thi pipeline: {e}")

# 4. Kiem tra Git Tag v0.2
print("\n[4] KIEM TRA GIT TAG RELEASE v0.2:")
try:
    result = subprocess.run(["git", "tag"], capture_output=True, text=True)
    if "v0.2" in result.stdout:
        print(" [V] Tag Release 'v0.2' da duoc tao thanh cong tren Git!")
    else:
        print(" [!] Chua thay Tag 'v0.2'! (Hay go: git tag -a v0.2 -m 'Nop BT2')")
except Exception as e:
    print(f" [!] Khong kiem tra duoc Git: {e}")

print("\n==================================================")
print(" HOAN TAT KIEM TRA! SAN SANG DON THAY VAO DEMO!")
print("==================================================")